from flask import Blueprint, request, jsonify
from src.config import get_db_connection

bp = Blueprint('matrix', __name__)


def get_color_code(niveau):
    """
    Retourne le code couleur basé sur le niveau
    - Vert (4-5): Expert
    - Orange (2-3): Intermédiaire
    - Rouge (0-1): Débutant
    - Gris: Jamais utilisé (None)
    """
    if niveau is None or niveau == 0:
        return "gris"
    elif niveau >= 4:
        return "vert"
    elif niveau >= 2:
        return "orange"
    else:
        return "rouge"


@bp.route("/matrix/competences", methods=["GET"])
def get_competence_matrix():
    """
    Retourne la matrice de compétences
    Lignes = développeurs, Colonnes = technologies

    Query params:
    - techno: filtrer par nom de technologie (partiel)
    - niveau_min: filtrer par niveau minimum
    - collaborator: filtrer par nom de collaborateur (partiel)
    """
    techno_filter = request.args.get('techno', '').strip()
    niveau_min = request.args.get('niveau_min', type=float)
    collaborator_filter = request.args.get('collaborator', '').strip()

    conn = get_db_connection()

    # Construction de la requête avec filtres
    query = """
        SELECT
            c.id as collaborator_id,
            c.firstname,
            c.lastname,
            t.id as techno_id,
            t.name as techno_name,
            comp.niveau_declare,
            comp.niveau_calcule
        FROM collaborator c
        LEFT JOIN competence comp ON c.id = comp.id_collaborator
        LEFT JOIN techno t ON comp.id_techno = t.id
        WHERE 1=1
    """

    params = []

    if techno_filter:
        query += " AND t.name LIKE ?"
        params.append(f"%{techno_filter}%")

    if niveau_min is not None:
        query += " AND comp.niveau_calcule >= ?"
        params.append(niveau_min)

    if collaborator_filter:
        query += " AND (c.firstname LIKE ? OR c.lastname LIKE ?)"
        params.append(f"%{collaborator_filter}%")
        params.append(f"%{collaborator_filter}%")

    query += " ORDER BY c.lastname, c.firstname, t.name"

    results = conn.execute(query, params).fetchall()
    conn.close()

    # Organiser les données en matrice
    # Structure: {collaborator_id: {techno_name: {niveau, color}}}
    collaborators = {}
    all_technos = set()

    for row in results:
        collab_id = row['collaborator_id']
        collab_name = f"{row['firstname']} {row['lastname']}"

        if collab_id not in collaborators:
            collaborators[collab_id] = {
                'id': collab_id,
                'name': collab_name,
                'competences': {}
            }

        if row['techno_name']:
            all_technos.add(row['techno_name'])
            niveau = row['niveau_calcule'] if row['niveau_calcule'] else row['niveau_declare']

            collaborators[collab_id]['competences'][row['techno_name']] = {
                'niveau_declare': row['niveau_declare'],
                'niveau_calcule': row['niveau_calcule'],
                'niveau': niveau,
                'color': get_color_code(niveau)
            }

    # Convertir en format matrice (tableau)
    technos_list = sorted(list(all_technos))
    matrix = []

    for collab_id, collab_data in collaborators.items():
        row = {
            'collaborator_id': collab_data['id'],
            'collaborator_name': collab_data['name'],
            'competences': {}
        }

        for techno in technos_list:
            if techno in collab_data['competences']:
                row['competences'][techno] = collab_data['competences'][techno]
            else:
                row['competences'][techno] = {
                    'niveau_declare': None,
                    'niveau_calcule': None,
                    'niveau': None,
                    'color': 'gris'
                }

        matrix.append(row)

    return jsonify({
        'matrix': matrix,
        'technologies': technos_list,
        'total_collaborators': len(matrix),
        'total_technologies': len(technos_list),
        'filters': {
            'techno': techno_filter if techno_filter else None,
            'niveau_min': niveau_min,
            'collaborator': collaborator_filter if collaborator_filter else None
        }
    }), 200


@bp.route("/matrix/competences/simple", methods=["GET"])
def get_simple_matrix():
    """
    Retourne une matrice simplifiée (juste les niveaux)
    Format: [[nom, techno1, techno2, ...], [Jean Dupont, 4.5, 3.2, ...]]
    """
    techno_filter = request.args.get('techno', '').strip()
    niveau_min = request.args.get('niveau_min', type=float)
    collaborator_filter = request.args.get('collaborator', '').strip()

    conn = get_db_connection()

    query = """
        SELECT
            c.id as collaborator_id,
            c.firstname,
            c.lastname,
            t.name as techno_name,
            comp.niveau_calcule
        FROM collaborator c
        LEFT JOIN competence comp ON c.id = comp.id_collaborator
        LEFT JOIN techno t ON comp.id_techno = t.id
        WHERE 1=1
    """

    params = []

    if techno_filter:
        query += " AND t.name LIKE ?"
        params.append(f"%{techno_filter}%")

    if niveau_min is not None:
        query += " AND comp.niveau_calcule >= ?"
        params.append(niveau_min)

    if collaborator_filter:
        query += " AND (c.firstname LIKE ? OR c.lastname LIKE ?)"
        params.append(f"%{collaborator_filter}%")
        params.append(f"%{collaborator_filter}%")

    query += " ORDER BY c.lastname, c.firstname, t.name"

    results = conn.execute(query, params).fetchall()
    conn.close()

    # Organiser les données
    collaborators = {}
    all_technos = set()

    for row in results:
        collab_id = row['collaborator_id']
        collab_name = f"{row['firstname']} {row['lastname']}"

        if collab_id not in collaborators:
            collaborators[collab_id] = {
                'name': collab_name,
                'competences': {}
            }

        if row['techno_name']:
            all_technos.add(row['techno_name'])
            collaborators[collab_id]['competences'][row['techno_name']] = row['niveau_calcule']

    # Convertir en format tableau
    technos_list = sorted(list(all_technos))

    # En-tête
    headers = ['Collaborateur'] + technos_list

    # Lignes de données
    rows = []
    for collab_id, collab_data in collaborators.items():
        row = [collab_data['name']]
        for techno in technos_list:
            niveau = collab_data['competences'].get(techno, 0)
            row.append(niveau if niveau else 0)
        rows.append(row)

    return jsonify({
        'headers': headers,
        'rows': rows
    }), 200


@bp.route("/matrix/competences/heatmap", methods=["GET"])
def get_heatmap_data():
    """
    Retourne les données formatées pour une heatmap
    Format optimisé pour les librairies de visualisation
    """
    conn = get_db_connection()

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

    # Format pour heatmap (tableau d'objets)
    heatmap_data = []
    for row in results:
        heatmap_data.append({
            'collaborator': row['collaborator'],
            'techno': row['techno'],
            'niveau': row['niveau'] if row['niveau'] else 0,
            'color': get_color_code(row['niveau'])
        })

    return jsonify({
        'data': heatmap_data
    }), 200
