from flask import Blueprint, request, jsonify
from src.config import get_db_connection

bp = Blueprint('allocation', __name__)


@bp.route("/allocation/suggest", methods=["POST"])
def suggest_team():
    """
    Suggère les meilleurs développeurs pour un nouveau projet

    Body:
    {
        "technologies": ["React", "Node.js", "MongoDB"],
        "team_size": 3  // optionnel, par défaut top 5 par techno
    }

    Retourne:
    - Top développeurs par technologie
    - Score global d'adéquation
    - Gaps identifiés (aucun expert)
    """
    data = request.get_json()

    if not data or 'technologies' not in data:
        return jsonify({"error": "Le champ 'technologies' est requis"}), 400

    technologies = data.get('technologies', [])
    team_size = data.get('team_size', 5)

    if not technologies:
        return jsonify({"error": "Au moins une technologie est requise"}), 400

    conn = get_db_connection()

    suggestions = {}
    gaps = []

    for techno_name in technologies:
        # Récupérer les développeurs qui connaissent cette techno
        query = """
            SELECT
                c.id as collaborator_id,
                c.firstname,
                c.lastname,
                comp.niveau_declare,
                comp.niveau_calcule,
                t.name as techno_name
            FROM competence comp
            JOIN collaborator c ON comp.id_collaborator = c.id
            JOIN techno t ON comp.id_techno = t.id
            WHERE t.name = ?
            ORDER BY comp.niveau_calcule DESC
            LIMIT ?
        """

        results = conn.execute(query, (techno_name, team_size)).fetchall()

        if not results:
            gaps.append({
                'techno': techno_name,
                'reason': 'Aucun développeur ne possède cette compétence'
            })
            suggestions[techno_name] = []
        else:
            # Identifier si pas d'expert (niveau < 4)
            experts = [r for r in results if r['niveau_calcule'] and r['niveau_calcule'] >= 4]

            if not experts:
                gaps.append({
                    'techno': techno_name,
                    'reason': 'Aucun expert disponible (niveau < 4)',
                    'best_niveau': results[0]['niveau_calcule'] if results[0]['niveau_calcule'] else 0
                })

            suggestions[techno_name] = [
                {
                    'collaborator_id': r['collaborator_id'],
                    'name': f"{r['firstname']} {r['lastname']}",
                    'niveau_declare': r['niveau_declare'],
                    'niveau_calcule': r['niveau_calcule'],
                    'is_expert': r['niveau_calcule'] >= 4 if r['niveau_calcule'] else False
                }
                for r in results
            ]

    conn.close()

    # Calculer un score global d'équipe
    all_collaborators = {}

    for techno, devs in suggestions.items():
        for dev in devs:
            collab_id = dev['collaborator_id']
            if collab_id not in all_collaborators:
                all_collaborators[collab_id] = {
                    'collaborator_id': collab_id,
                    'name': dev['name'],
                    'technos': [],
                    'total_score': 0,
                    'avg_score': 0
                }

            all_collaborators[collab_id]['technos'].append({
                'techno': techno,
                'niveau': dev['niveau_calcule']
            })
            all_collaborators[collab_id]['total_score'] += dev['niveau_calcule'] if dev['niveau_calcule'] else 0

    # Calculer le score moyen et trier
    for collab_id, collab_data in all_collaborators.items():
        nb_technos = len(collab_data['technos'])
        collab_data['avg_score'] = round(collab_data['total_score'] / nb_technos, 2) if nb_technos > 0 else 0
        collab_data['nb_technos_matched'] = nb_technos
        collab_data['match_percentage'] = round((nb_technos / len(technologies)) * 100, 2)

    # Trier par nombre de technos matchées puis par score moyen
    best_fits = sorted(
        all_collaborators.values(),
        key=lambda x: (x['nb_technos_matched'], x['avg_score']),
        reverse=True
    )

    return jsonify({
        'suggestions_by_techno': suggestions,
        'best_overall_fits': best_fits[:team_size],
        'gaps': gaps,
        'total_technologies': len(technologies),
        'technologies_with_experts': len([t for t in technologies if t not in [g['techno'] for g in gaps]])
    }), 200


@bp.route("/allocation/capacity", methods=["GET"])
def get_team_capacity():
    """
    Vue agrégée de la capacité globale de l'équipe par technologie

    Query params:
    - niveau_min: niveau minimum à considérer (défaut: 3)
    """
    niveau_min = request.args.get('niveau_min', default=3, type=float)

    conn = get_db_connection()

    query = """
        SELECT
            t.name as techno,
            COUNT(DISTINCT comp.id_collaborator) as nb_collaborators,
            AVG(comp.niveau_calcule) as avg_niveau,
            MAX(comp.niveau_calcule) as max_niveau,
            MIN(comp.niveau_calcule) as min_niveau,
            SUM(CASE WHEN comp.niveau_calcule >= 4 THEN 1 ELSE 0 END) as nb_experts,
            SUM(CASE WHEN comp.niveau_calcule >= 2 AND comp.niveau_calcule < 4 THEN 1 ELSE 0 END) as nb_intermediaires,
            SUM(CASE WHEN comp.niveau_calcule < 2 THEN 1 ELSE 0 END) as nb_debutants
        FROM techno t
        LEFT JOIN competence comp ON t.id = comp.id_techno
        WHERE comp.niveau_calcule >= ?
        GROUP BY t.id, t.name
        ORDER BY nb_experts DESC, avg_niveau DESC
    """

    results = conn.execute(query, (niveau_min,)).fetchall()
    conn.close()

    capacity = []
    for row in results:
        capacity.append({
            'techno': row['techno'],
            'total_collaborators': row['nb_collaborators'],
            'avg_niveau': round(row['avg_niveau'], 2) if row['avg_niveau'] else 0,
            'max_niveau': row['max_niveau'],
            'min_niveau': row['min_niveau'],
            'nb_experts': row['nb_experts'],
            'nb_intermediaires': row['nb_intermediaires'],
            'nb_debutants': row['nb_debutants'],
            'capacity_level': 'high' if row['nb_experts'] >= 3 else 'medium' if row['nb_experts'] >= 1 else 'low'
        })

    return jsonify({
        'capacity': capacity,
        'total_technologies': len(capacity),
        'niveau_min_filter': niveau_min
    }), 200


@bp.route("/allocation/gaps", methods=["GET"])
def identify_gaps():
    """
    Identifie les gaps critiques de compétences
    Technologies maîtrisées par moins de 2 experts
    """
    conn = get_db_connection()

    query = """
        SELECT
            t.name as techno,
            COUNT(DISTINCT comp.id_collaborator) as total_collaborators,
            SUM(CASE WHEN comp.niveau_calcule >= 4 THEN 1 ELSE 0 END) as nb_experts,
            MAX(comp.niveau_calcule) as best_niveau
        FROM techno t
        LEFT JOIN competence comp ON t.id = comp.id_techno
        GROUP BY t.id, t.name
        HAVING nb_experts < 2
        ORDER BY nb_experts ASC, best_niveau ASC
    """

    results = conn.execute(query).fetchall()
    conn.close()

    gaps = []
    for row in results:
        risk_level = 'critical' if row['nb_experts'] == 0 else 'high' if row['nb_experts'] == 1 else 'medium'

        gaps.append({
            'techno': row['techno'],
            'nb_experts': row['nb_experts'],
            'total_collaborators': row['total_collaborators'],
            'best_niveau': row['best_niveau'] if row['best_niveau'] else 0,
            'risk_level': risk_level,
            'recommendation': self._get_recommendation(row['nb_experts'], row['best_niveau'])
        })

    return jsonify({
        'gaps': gaps,
        'total_gaps': len(gaps),
        'critical_gaps': len([g for g in gaps if g['risk_level'] == 'critical']),
        'high_risk_gaps': len([g for g in gaps if g['risk_level'] == 'high'])
    }), 200


def _get_recommendation(nb_experts, best_niveau):
    """Retourne une recommandation basée sur le nombre d'experts"""
    if nb_experts == 0:
        if best_niveau and best_niveau >= 3:
            return "Former les collaborateurs intermédiaires ou recruter un expert"
        else:
            return "Recruter un expert ou former l'équipe"
    elif nb_experts == 1:
        return "Risque de dépendance à une personne - former un second expert"
    else:
        return "Situation acceptable mais amélioration possible"
