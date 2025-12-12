from flask import Blueprint, request, jsonify
from src.config import get_db_connection
from src.models import competence_model, project_history_model
import datetime
from dateutil import parser as date_parser

bp = Blueprint('scoring', __name__)


def calculate_score_for_competence(id_collaborator, id_techno, niveau_declare):
    """
    Calcule le niveau_calcule basé sur l'historique des projets

    Formule: Score = (niveau_déclaré × 0.3) + (score_projets × 0.4) + (ancienneté_bonus × 0.3)
    - score_projets basé sur le nombre de projets (max 5)
    - ancienneté_bonus = max(0, 5 - mois_depuis_dernière_utilisation/12)
    """
    conn = get_db_connection()

    # Récupérer l'historique des projets pour ce collaborateur et cette techno
    history = conn.execute("""
        SELECT date_fin, duree_mois
        FROM project_techno_history
        WHERE id_collaborator = ? AND id_techno = ?
    """, (id_collaborator, id_techno)).fetchall()

    conn.close()

    if not history:
        # Pas d'historique, retourner le niveau déclaré
        return float(niveau_declare)

    # 1. Calculer le score basé sur le nombre de projets (max 5 pour obtenir 5/5)
    nb_projets = len(history)
    score_projets = min(5.0, nb_projets)  # 1 projet = 1 point, max 5

    # 2. Calculer le bonus d'ancienneté basé sur la date de fin la plus récente
    dates_fin = []
    for h in history:
        if h['date_fin']:
            try:
                # Parser la date (format YYYY-MM ou YYYY-MM-DD)
                if len(h['date_fin']) == 7:  # YYYY-MM
                    date_fin = datetime.datetime.strptime(h['date_fin'], '%Y-%m')
                else:
                    date_fin = date_parser.parse(h['date_fin'])
                dates_fin.append(date_fin)
            except:
                pass

    if dates_fin:
        # Dernière utilisation
        derniere_utilisation = max(dates_fin)
        now = datetime.datetime.now()

        # Calculer les mois écoulés
        mois_ecoules = (now.year - derniere_utilisation.year) * 12 + (now.month - derniere_utilisation.month)

        # Bonus d'ancienneté (pénalité si >12 mois)
        anciennete_bonus = max(0, 5 - mois_ecoules / 12.0)
    else:
        # Pas de date de fin, on considère que c'est récent
        anciennete_bonus = 5.0

    # 3. Calcul final
    score = (niveau_declare * 0.3) + (score_projets * 0.4) + (anciennete_bonus * 0.3)

    # Borner entre 1 et 5
    score = max(1.0, min(5.0, score))

    return round(score, 2)


@bp.route("/scoring/calculate", methods=["POST"])
def calculate_all_scores():
    """
    Recalcule tous les scores automatiquement pour toutes les compétences
    """
    conn = get_db_connection()

    # Récupérer toutes les compétences
    competences = conn.execute("SELECT * FROM competence").fetchall()

    updated = 0
    errors = []

    for comp in competences:
        try:
            id_collaborator = comp['id_collaborator']
            id_techno = comp['id_techno']
            niveau_declare = comp['niveau_declare']

            # Calculer le nouveau score
            niveau_calcule = calculate_score_for_competence(id_collaborator, id_techno, niveau_declare)

            # Mettre à jour
            conn.execute(
                "UPDATE competence SET niveau_calcule = ?, date_upd = ? WHERE id = ?",
                (niveau_calcule, datetime.datetime.now(), comp['id'])
            )
            updated += 1

        except Exception as e:
            errors.append(f"Compétence {comp['id']}: {str(e)}")

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Recalcul terminé",
        "updated": updated,
        "errors": errors
    }), 200


@bp.route("/scoring/calculate/collaborator/<int:id_collaborator>", methods=["POST"])
def calculate_scores_for_collaborator(id_collaborator):
    """
    Recalcule les scores pour un collaborateur spécifique
    """
    conn = get_db_connection()

    # Récupérer les compétences du collaborateur
    competences = conn.execute(
        "SELECT * FROM competence WHERE id_collaborator = ?",
        (id_collaborator,)
    ).fetchall()

    if not competences:
        conn.close()
        return jsonify({"error": "Aucune compétence trouvée pour ce collaborateur"}), 404

    updated = 0
    errors = []

    for comp in competences:
        try:
            id_techno = comp['id_techno']
            niveau_declare = comp['niveau_declare']

            # Calculer le nouveau score
            niveau_calcule = calculate_score_for_competence(id_collaborator, id_techno, niveau_declare)

            # Mettre à jour
            conn.execute(
                "UPDATE competence SET niveau_calcule = ?, date_upd = ? WHERE id = ?",
                (niveau_calcule, datetime.datetime.now(), comp['id'])
            )
            updated += 1

        except Exception as e:
            errors.append(f"Compétence {comp['id']}: {str(e)}")

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Scores recalculés pour le collaborateur {id_collaborator}",
        "updated": updated,
        "errors": errors
    }), 200


@bp.route("/scoring/calculate/competence/<int:id_competence>", methods=["POST"])
def calculate_score_for_single_competence(id_competence):
    """
    Recalcule le score pour une compétence spécifique
    """
    conn = get_db_connection()

    comp = conn.execute(
        "SELECT * FROM competence WHERE id = ?",
        (id_competence,)
    ).fetchone()

    if not comp:
        conn.close()
        return jsonify({"error": "Compétence non trouvée"}), 404

    try:
        id_collaborator = comp['id_collaborator']
        id_techno = comp['id_techno']
        niveau_declare = comp['niveau_declare']

        # Calculer le nouveau score
        niveau_calcule = calculate_score_for_competence(id_collaborator, id_techno, niveau_declare)

        # Mettre à jour
        conn.execute(
            "UPDATE competence SET niveau_calcule = ?, date_upd = ? WHERE id = ?",
            (niveau_calcule, datetime.datetime.now(), comp['id'])
        )
        conn.commit()

        # Récupérer la compétence mise à jour
        updated_comp = conn.execute(
            "SELECT * FROM competence WHERE id = ?",
            (id_competence,)
        ).fetchone()

        conn.close()

        return jsonify({
            "message": "Score recalculé",
            "competence": dict(updated_comp)
        }), 200

    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400


@bp.route("/scoring/parameters", methods=["GET"])
def get_scoring_parameters():
    """
    Retourne les paramètres de l'algorithme de scoring
    """
    return jsonify({
        "algorithm": "weighted_score",
        "formula": "Score = (niveau_déclaré × 0.3) + (score_projets × 0.4) + (ancienneté_bonus × 0.3)",
        "parameters": {
            "niveau_declare_weight": 0.3,
            "nb_projets_weight": 0.4,
            "anciennete_weight": 0.3,
            "max_score": 5.0,
            "min_score": 1.0,
            "penalite_anciennete_mois": 12,
            "score_par_projet": 1.0,
            "max_projets_score": 5.0
        },
        "description": {
            "niveau_declare": "Niveau déclaré initial par le collaborateur",
            "score_projets": "Basé sur le nombre de projets (1 projet = 1 point, max 5)",
            "anciennete_bonus": "Pénalité si dernière utilisation > 12 mois. Formule: max(0, 5 - mois_écoulés/12)"
        }
    }), 200
