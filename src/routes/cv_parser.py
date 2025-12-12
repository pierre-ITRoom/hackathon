from flask import Blueprint, request, jsonify
import re
import io

bp = Blueprint('cv_parser', __name__)

# Liste de technologies communes à détecter
COMMON_TECHNOLOGIES = [
    # Langages
    'Python', 'JavaScript', 'Java', 'C#', 'C++', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
    'Kotlin', 'TypeScript', 'Scala', 'R', 'Perl', 'Shell', 'Bash', 'PowerShell',

    # Frameworks Web
    'React', 'Angular', 'Vue', 'Svelte', 'Next.js', 'Nuxt.js', 'Django', 'Flask',
    'FastAPI', 'Express', 'Node.js', 'Spring', 'Spring Boot', 'Laravel', 'Symfony',
    'Rails', 'ASP.NET', '.NET', 'Blazor',

    # Bases de données
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server',
    'MariaDB', 'Cassandra', 'DynamoDB', 'Firebase', 'Elasticsearch', 'Neo4j',

    # DevOps & Cloud
    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Jenkins', 'GitLab CI', 'GitHub Actions',
    'Terraform', 'Ansible', 'Chef', 'Puppet', 'Nginx', 'Apache',

    # Mobile
    'React Native', 'Flutter', 'Ionic', 'Xamarin', 'Android', 'iOS',

    # Outils & Autres
    'Git', 'Linux', 'GraphQL', 'REST', 'gRPC', 'Kafka', 'RabbitMQ', 'Selenium',
    'Jest', 'Pytest', 'JUnit', 'Webpack', 'Vite', 'Babel', 'SASS', 'LESS',
    'Tailwind', 'Bootstrap', 'Material-UI', 'Redux', 'Vuex', 'MobX',

    # Data Science & ML
    'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib',
    'Jupyter', 'Keras', 'OpenCV',

    # CMS & E-commerce
    'WordPress', 'Drupal', 'Joomla', 'Magento', 'Shopify', 'WooCommerce',

    # Méthodologies
    'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD'
]


def extract_text_from_txt(file_stream):
    """Extrait le texte d'un fichier texte"""
    try:
        content = file_stream.read().decode('utf-8')
        return content
    except UnicodeDecodeError:
        # Essayer avec un autre encodage
        file_stream.seek(0)
        content = file_stream.read().decode('latin-1')
        return content


def extract_text_from_pdf(file_stream):
    """Extrait le texte d'un fichier PDF"""
    try:
        import pdfplumber
        pdf_file = io.BytesIO(file_stream.read())
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        raise Exception("pdfplumber n'est pas installé. Installez-le avec: pip install pdfplumber")
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")


def extract_text_from_docx(file_stream):
    """Extrait le texte d'un fichier Word"""
    try:
        from docx import Document
        doc_file = io.BytesIO(file_stream.read())
        doc = Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        raise Exception("python-docx n'est pas installé. Installez-le avec: pip install python-docx")
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du document Word: {str(e)}")


def detect_technologies(text, custom_technologies=None):
    """
    Détecte les technologies dans un texte
    Retourne un dictionnaire {technologie: nombre_occurrences}
    """
    technologies_to_detect = COMMON_TECHNOLOGIES.copy()

    if custom_technologies:
        technologies_to_detect.extend(custom_technologies)

    detected = {}

    # Normaliser le texte
    text_lower = text.lower()

    for tech in technologies_to_detect:
        # Recherche insensible à la casse avec word boundaries
        pattern = r'\b' + re.escape(tech.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)

        if matches:
            detected[tech] = len(matches)

    return detected


def estimate_niveau(occurrences, text_length):
    """
    Estime un niveau de compétence basé sur le nombre d'occurrences
    et la longueur du texte

    Heuristique simple:
    - 1-2 occurrences: niveau 2
    - 3-5 occurrences: niveau 3
    - 6-10 occurrences: niveau 4
    - >10 occurrences: niveau 5
    """
    if occurrences >= 10:
        return 5
    elif occurrences >= 6:
        return 4
    elif occurrences >= 3:
        return 3
    elif occurrences >= 1:
        return 2
    else:
        return 1


@bp.route("/cv/parse", methods=["POST"])
def parse_cv():
    """
    Parse un CV et extrait les technologies

    Form data:
    - file: fichier CV (PDF, TXT, DOCX)
    - custom_technologies: liste optionnelle de technologies supplémentaires (JSON array)
    - collaborator_name: nom du collaborateur (optionnel, pour contexte)

    Retourne:
    - Liste des technologies détectées avec niveau estimé
    """
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    # Récupérer les paramètres optionnels
    custom_technologies = request.form.get('custom_technologies')
    if custom_technologies:
        try:
            import json
            custom_technologies = json.loads(custom_technologies)
        except:
            custom_technologies = None

    collaborator_name = request.form.get('collaborator_name', 'Inconnu')

    # Détecter le type de fichier
    filename = file.filename.lower()

    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file.stream)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file.stream)
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            text = extract_text_from_docx(file.stream)
        else:
            return jsonify({
                "error": "Format de fichier non supporté. Formats acceptés: PDF, TXT, DOCX"
            }), 400

        # Détecter les technologies
        detected_technologies = detect_technologies(text, custom_technologies)

        if not detected_technologies:
            return jsonify({
                "message": "Aucune technologie détectée dans le CV",
                "collaborator": collaborator_name,
                "technologies": [],
                "text_preview": text[:500] if len(text) > 500 else text
            }), 200

        # Estimer les niveaux
        text_length = len(text)
        technologies_with_niveau = []

        for tech, occurrences in detected_technologies.items():
            niveau = estimate_niveau(occurrences, text_length)
            technologies_with_niveau.append({
                'technologie': tech,
                'occurrences': occurrences,
                'niveau_estime': niveau
            })

        # Trier par nombre d'occurrences (décroissant)
        technologies_with_niveau.sort(key=lambda x: x['occurrences'], reverse=True)

        return jsonify({
            "message": "CV analysé avec succès",
            "collaborator": collaborator_name,
            "total_technologies_detected": len(technologies_with_niveau),
            "technologies": technologies_with_niveau,
            "text_length": text_length,
            "text_preview": text[:500] if len(text) > 500 else text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/cv/parse-and-import", methods=["POST"])
def parse_and_import_cv():
    """
    Parse un CV et importe automatiquement les compétences dans la base

    Form data:
    - file: fichier CV
    - firstname: prénom du collaborateur (requis)
    - lastname: nom du collaborateur (requis)
    - custom_technologies: liste optionnelle de technologies supplémentaires
    - auto_create_collaborator: créer le collaborateur s'il n'existe pas (défaut: true)
    """
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files['file']
    firstname = request.form.get('firstname', '').strip()
    lastname = request.form.get('lastname', '').strip()

    if not firstname or not lastname:
        return jsonify({"error": "firstname et lastname sont requis"}), 400

    # Parser le CV
    custom_technologies = request.form.get('custom_technologies')
    if custom_technologies:
        try:
            import json
            custom_technologies = json.loads(custom_technologies)
        except:
            custom_technologies = None

    filename = file.filename.lower()

    try:
        # Extraire le texte
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file.stream)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file.stream)
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            text = extract_text_from_docx(file.stream)
        else:
            return jsonify({
                "error": "Format de fichier non supporté. Formats acceptés: PDF, TXT, DOCX"
            }), 400

        # Détecter les technologies
        detected_technologies = detect_technologies(text, custom_technologies)

        if not detected_technologies:
            return jsonify({
                "message": "Aucune technologie détectée",
                "created": 0,
                "technologies": []
            }), 200

        # Importer dans la base de données
        from src.routes.imports import get_or_create_collaborator, get_or_create_techno
        from src.models import competence_model

        # Créer ou récupérer le collaborateur
        id_collaborator = get_or_create_collaborator(firstname, lastname)

        created = 0
        updated = 0
        errors = []
        text_length = len(text)

        for tech, occurrences in detected_technologies.items():
            try:
                niveau_estime = estimate_niveau(occurrences, text_length)
                id_techno = get_or_create_techno(tech)

                # Vérifier si la compétence existe
                existing = competence_model.get_by_collaborator_techno(id_collaborator, id_techno)

                if existing:
                    # Ne pas écraser si le niveau existant est meilleur
                    if existing['niveau_declare'] < niveau_estime:
                        competence_model.update(existing['id'], {
                            'niveau_declare': niveau_estime,
                            'niveau_calcule': niveau_estime
                        })
                        updated += 1
                else:
                    competence_model.create({
                        'id_collaborator': id_collaborator,
                        'id_techno': id_techno,
                        'niveau_declare': niveau_estime,
                        'niveau_calcule': niveau_estime
                    })
                    created += 1

            except Exception as e:
                errors.append(f"{tech}: {str(e)}")

        return jsonify({
            "message": "CV importé avec succès",
            "collaborator": f"{firstname} {lastname}",
            "collaborator_id": id_collaborator,
            "created": created,
            "updated": updated,
            "total_technologies_detected": len(detected_technologies),
            "errors": errors
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/cv/supported-technologies", methods=["GET"])
def get_supported_technologies():
    """
    Retourne la liste des technologies détectables automatiquement
    """
    return jsonify({
        "total": len(COMMON_TECHNOLOGIES),
        "technologies": sorted(COMMON_TECHNOLOGIES)
    }), 200
