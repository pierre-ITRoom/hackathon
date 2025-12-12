from flask import Blueprint, request, jsonify
from src.config import get_db_connection

bp = Blueprint('dashboard', __name__)


@bp.route("/dashboard/overview", methods=["GET"])
def get_dashboard_overview():
    """
    Vue globale du dashboard avec toutes les métriques principales
    """
    conn = get_db_connection()

    # Statistiques générales
    stats = {}

    # Nombre total de collaborateurs
    stats['total_collaborators'] = conn.execute("SELECT COUNT(*) as count FROM collaborator").fetchone()['count']

    # Nombre total de technologies
    stats['total_technologies'] = conn.execute("SELECT COUNT(*) as count FROM techno").fetchone()['count']

    # Nombre total de compétences
    stats['total_competences'] = conn.execute("SELECT COUNT(*) as count FROM competence").fetchone()['count']

    # Nombre total de projets
    stats['total_projects'] = conn.execute("SELECT COUNT(*) as count FROM project").fetchone()['count']

    # Niveau moyen des compétences
    avg_niveau = conn.execute("SELECT AVG(niveau_calcule) as avg FROM competence").fetchone()['avg']
    stats['avg_niveau'] = round(avg_niveau, 2) if avg_niveau else 0

    conn.close()

    return jsonify({
        'stats': stats
    }), 200


@bp.route("/dashboard/top-technologies", methods=["GET"])
def get_top_technologies():
    """
    Top 10 (ou N) technologies maîtrisées par l'équipe
    Basé sur le nombre d'experts et le niveau moyen

    Query params:
    - limit: nombre de technologies à retourner (défaut: 10)
    """
    limit = request.args.get('limit', default=10, type=int)

    conn = get_db_connection()

    query = """
        SELECT
            t.name as techno,
            COUNT(DISTINCT comp.id_collaborator) as nb_collaborators,
            AVG(comp.niveau_calcule) as avg_niveau,
            SUM(CASE WHEN comp.niveau_calcule >= 4 THEN 1 ELSE 0 END) as nb_experts,
            MAX(comp.niveau_calcule) as max_niveau
        FROM techno t
        JOIN competence comp ON t.id = comp.id_techno
        GROUP BY t.id, t.name
        ORDER BY nb_experts DESC, avg_niveau DESC
        LIMIT ?
    """

    results = conn.execute(query, (limit,)).fetchall()
    conn.close()

    top_technologies = []
    for row in results:
        top_technologies.append({
            'techno': row['techno'],
            'nb_collaborators': row['nb_collaborators'],
            'avg_niveau': round(row['avg_niveau'], 2) if row['avg_niveau'] else 0,
            'nb_experts': row['nb_experts'],
            'max_niveau': row['max_niveau']
        })

    return jsonify({
        'top_technologies': top_technologies,
        'limit': limit
    }), 200


@bp.route("/dashboard/at-risk-technologies", methods=["GET"])
def get_at_risk_technologies():
    """
    Technologies à risque: maîtrisées par moins de 2 experts

    Query params:
    - threshold: nombre minimum d'experts (défaut: 2)
    """
    threshold = request.args.get('threshold', default=2, type=int)

    conn = get_db_connection()

    query = """
        SELECT
            t.name as techno,
            COUNT(DISTINCT comp.id_collaborator) as nb_collaborators,
            SUM(CASE WHEN comp.niveau_calcule >= 4 THEN 1 ELSE 0 END) as nb_experts,
            AVG(comp.niveau_calcule) as avg_niveau,
            MAX(comp.niveau_calcule) as best_niveau
        FROM techno t
        JOIN competence comp ON t.id = comp.id_techno
        GROUP BY t.id, t.name
        HAVING nb_experts < ?
        ORDER BY nb_experts ASC, best_niveau DESC
    """

    results = conn.execute(query, (threshold,)).fetchall()
    conn.close()

    at_risk = []
    for row in results:
        risk_level = 'critical' if row['nb_experts'] == 0 else 'high' if row['nb_experts'] == 1 else 'medium'

        at_risk.append({
            'techno': row['techno'],
            'nb_collaborators': row['nb_collaborators'],
            'nb_experts': row['nb_experts'],
            'avg_niveau': round(row['avg_niveau'], 2) if row['avg_niveau'] else 0,
            'best_niveau': row['best_niveau'] if row['best_niveau'] else 0,
            'risk_level': risk_level
        })

    return jsonify({
        'at_risk_technologies': at_risk,
        'total': len(at_risk),
        'threshold': threshold,
        'critical': len([t for t in at_risk if t['risk_level'] == 'critical']),
        'high': len([t for t in at_risk if t['risk_level'] == 'high'])
    }), 200


@bp.route("/dashboard/collaborator/<int:id_collaborator>/radar", methods=["GET"])
def get_collaborator_radar(id_collaborator):
    """
    Graphique radar du profil de compétences d'un développeur
    Retourne les données formatées pour un graphique radar

    Retourne toutes les compétences du collaborateur
    """
    conn = get_db_connection()

    # Vérifier que le collaborateur existe
    collab = conn.execute(
        "SELECT * FROM collaborator WHERE id = ?",
        (id_collaborator,)
    ).fetchone()

    if not collab:
        conn.close()
        return jsonify({"error": "Collaborateur non trouvé"}), 404

    # Récupérer toutes ses compétences
    query = """
        SELECT
            t.name as techno,
            comp.niveau_declare,
            comp.niveau_calcule
        FROM competence comp
        JOIN techno t ON comp.id_techno = t.id
        WHERE comp.id_collaborator = ?
        ORDER BY comp.niveau_calcule DESC
    """

    results = conn.execute(query, (id_collaborator,)).fetchall()
    conn.close()

    if not results:
        return jsonify({
            "collaborator": {
                "id": collab['id'],
                "name": f"{collab['firstname']} {collab['lastname']}"
            },
            "radar_data": [],
            "message": "Aucune compétence trouvée pour ce collaborateur"
        }), 200

    # Format pour graphique radar
    radar_data = []
    for row in results:
        radar_data.append({
            'techno': row['techno'],
            'niveau_declare': row['niveau_declare'],
            'niveau_calcule': row['niveau_calcule'] if row['niveau_calcule'] else row['niveau_declare']
        })

    return jsonify({
        'collaborator': {
            'id': collab['id'],
            'name': f"{collab['firstname']} {collab['lastname']}"
        },
        'radar_data': radar_data,
        'total_competences': len(radar_data)
    }), 200


@bp.route("/dashboard/heatmap", methods=["GET"])
def get_global_heatmap():
    """
    Heatmap globale des compétences par technologie
    Agrégation de toutes les compétences pour visualisation

    Query params:
    - top_n: limiter aux N technologies les plus utilisées (optionnel)
    """
    top_n = request.args.get('top_n', type=int)

    conn = get_db_connection()

    if top_n:
        # Récupérer les top N technologies
        query = """
            SELECT
                t.name as techno,
                COUNT(DISTINCT comp.id_collaborator) as nb_users
            FROM techno t
            JOIN competence comp ON t.id = comp.id_techno
            GROUP BY t.id, t.name
            ORDER BY nb_users DESC
            LIMIT ?
        """
        top_technos = conn.execute(query, (top_n,)).fetchall()
        techno_names = [t['techno'] for t in top_technos]

        # Filtrer les données de la heatmap
        placeholders = ','.join(['?'] * len(techno_names))
        query = f"""
            SELECT
                c.firstname || ' ' || c.lastname as collaborator,
                t.name as techno,
                comp.niveau_calcule as niveau
            FROM competence comp
            JOIN collaborator c ON comp.id_collaborator = c.id
            JOIN techno t ON comp.id_techno = t.id
            WHERE t.name IN ({placeholders})
            ORDER BY c.lastname, c.firstname, t.name
        """
        results = conn.execute(query, techno_names).fetchall()
    else:
        # Toutes les compétences
        query = """
            SELECT
                c.firstname || ' ' || c.lastname as collaborator,
                t.name as techno,
                comp.niveau_calcule as niveau
            FROM competence comp
            JOIN collaborator c ON comp.id_collaborator = c.id
            JOIN techno t ON comp.id_techno = t.id
            ORDER BY c.lastname, c.firstname, t.name
        """
        results = conn.execute(query).fetchall()

    conn.close()

    # Format pour heatmap
    heatmap_data = []
    for row in results:
        heatmap_data.append({
            'collaborator': row['collaborator'],
            'techno': row['techno'],
            'niveau': row['niveau'] if row['niveau'] else 0
        })

    return jsonify({
        'heatmap_data': heatmap_data,
        'total_points': len(heatmap_data),
        'top_n_filter': top_n
    }), 200


@bp.route("/dashboard/statistics", methods=["GET"])
def get_detailed_statistics():
    """
    Statistiques détaillées pour le dashboard
    """
    conn = get_db_connection()

    stats = {}

    # Distribution des niveaux
    niveau_distribution = conn.execute("""
        SELECT
            CASE
                WHEN niveau_calcule >= 4 THEN 'Expert (4-5)'
                WHEN niveau_calcule >= 2 THEN 'Intermédiaire (2-3)'
                ELSE 'Débutant (0-1)'
            END as category,
            COUNT(*) as count
        FROM competence
        GROUP BY category
    """).fetchall()

    stats['niveau_distribution'] = [
        {'category': row['category'], 'count': row['count']}
        for row in niveau_distribution
    ]

    # Technologies les plus demandées (dans les projets)
    top_project_technos = conn.execute("""
        SELECT
            t.name as techno,
            COUNT(DISTINCT pth.id_project) as nb_projects
        FROM project_techno_history pth
        JOIN techno t ON pth.id_techno = t.id
        GROUP BY t.id, t.name
        ORDER BY nb_projects DESC
        LIMIT 10
    """).fetchall()

    stats['top_project_technos'] = [
        {'techno': row['techno'], 'nb_projects': row['nb_projects']}
        for row in top_project_technos
    ]

    # Collaborateurs les plus polyvalents
    top_polyvalent = conn.execute("""
        SELECT
            c.firstname || ' ' || c.lastname as name,
            COUNT(DISTINCT comp.id_techno) as nb_technos,
            AVG(comp.niveau_calcule) as avg_niveau
        FROM collaborator c
        JOIN competence comp ON c.id = comp.id_collaborator
        GROUP BY c.id, name
        ORDER BY nb_technos DESC, avg_niveau DESC
        LIMIT 10
    """).fetchall()

    stats['top_polyvalent'] = [
        {
            'name': row['name'],
            'nb_technos': row['nb_technos'],
            'avg_niveau': round(row['avg_niveau'], 2) if row['avg_niveau'] else 0
        }
        for row in top_polyvalent
    ]

    conn.close()

    return jsonify(stats), 200
