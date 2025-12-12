#!/usr/bin/env python3
"""
Script de génération de fixtures massives pour tester l'API
"""
import requests
import random
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

# Données de base
FIRSTNAMES = [
    "Jean", "Sophie", "Luc", "Marie", "Thomas", "Emma", "Pierre", "Julie",
    "Antoine", "Laura", "Nicolas", "Camille", "Alexandre", "Léa", "Maxime",
    "Charlotte", "Hugo", "Chloé", "Lucas", "Manon", "Nathan", "Pauline",
    "Louis", "Sarah", "Gabriel", "Lucie", "Arthur", "Clara", "Theo", "Zoé"
]

LASTNAMES = [
    "Dupont", "Martin", "Bernard", "Durand", "Petit", "Moreau", "Laurent",
    "Leroy", "Simon", "Michel", "Garcia", "David", "Bertrand", "Roux",
    "Vincent", "Fournier", "Morel", "Girard", "Andre", "Lefebvre",
    "Mercier", "Blanc", "Robin", "Lambert", "Bonnet", "François", "Martinez",
    "Legrand", "Garnier", "Faure"
]

TECHNOLOGIES = [
    # Langages
    "Python", "JavaScript", "Java", "C#", "C++", "PHP", "Ruby", "Go", "Rust",
    "Swift", "Kotlin", "TypeScript", "Scala", "R", "Perl", "Shell", "Bash",

    # Frameworks Web
    "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js", "Django",
    "Flask", "FastAPI", "Express.js", "Node.js", "Spring", "Spring Boot",
    "Laravel", "Symfony", "Rails", "ASP.NET", ".NET Core", "Blazor",

    # Bases de données
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "SQL Server",
    "MariaDB", "Cassandra", "DynamoDB", "Firebase", "Elasticsearch", "Neo4j",

    # DevOps & Cloud
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Jenkins", "GitLab CI",
    "GitHub Actions", "Terraform", "Ansible", "Chef", "Puppet", "Nginx", "Apache",

    # Mobile
    "React Native", "Flutter", "Ionic", "Xamarin", "Android SDK", "iOS SDK",

    # Outils
    "Git", "Linux", "GraphQL", "REST API", "gRPC", "Kafka", "RabbitMQ",
    "Selenium", "Jest", "Pytest", "JUnit", "Webpack", "Vite", "Babel",
    "SASS", "LESS", "Tailwind CSS", "Bootstrap", "Material-UI", "Redux",
    "Vuex", "MobX",

    # Data Science & ML
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
    "Jupyter", "Keras", "OpenCV"
]

TYPES = [
    "Frontend", "Backend", "Full Stack", "DevOps", "Mobile", "Data Science",
    "Database", "Cloud", "Testing", "Design"
]

PROJECT_NAMES = [
    "Site E-commerce", "Application Mobile", "API REST Enterprise", "Dashboard Analytics",
    "Plateforme SaaS", "Application Desktop", "Système de Gestion", "Portail Client",
    "Application IoT", "Plateforme de Formation", "Outil de Monitoring", "CRM Interne",
    "Application de Réservation", "Système de Paiement", "Plateforme de Streaming",
    "Application de Messagerie", "Outil de Collaboration", "Système de Ticketing",
    "Application de Santé", "Plateforme d'Apprentissage", "Outil de Productivité",
    "Application de Livraison", "Système de Facturation", "Plateforme de Blog",
    "Application de Fitness", "Système de Workflow", "Plateforme E-learning",
    "Application de Logistique", "Système RH", "Plateforme Marketing"
]


def create_collaborators(n=30):
    """Crée n collaborateurs"""
    print(f"\n🔧 Création de {n} collaborateurs...")
    created = []

    for i in range(n):
        firstname = random.choice(FIRSTNAMES)
        lastname = random.choice(LASTNAMES)

        response = requests.post(f"{BASE_URL}/collaborators", json={
            "firstname": firstname,
            "lastname": lastname
        })

        if response.status_code == 201:
            data = response.json()
            created.append(data['id'])
            print(f"  ✅ {firstname} {lastname} (ID: {data['id']})")
        else:
            print(f"  ❌ Erreur: {response.text}")

    print(f"✅ {len(created)} collaborateurs créés")
    return created


def create_types(types=TYPES):
    """Crée les types"""
    print(f"\n🔧 Création de {len(types)} types...")
    created = []

    for type_name in types:
        response = requests.post(f"{BASE_URL}/types", json={
            "name": type_name
        })

        if response.status_code == 201:
            data = response.json()
            created.append(data['id'])
            print(f"  ✅ {type_name} (ID: {data['id']})")

    print(f"✅ {len(created)} types créés")
    return created


def create_technologies(technologies=TECHNOLOGIES):
    """Crée les technologies"""
    print(f"\n🔧 Création de {len(technologies)} technologies...")
    created = []

    for techno_name in technologies:
        response = requests.post(f"{BASE_URL}/technos", json={
            "name": techno_name
        })

        if response.status_code == 201:
            data = response.json()
            created.append(data['id'])
            print(f"  ✅ {techno_name} (ID: {data['id']})")

    print(f"✅ {len(created)} technologies créées")
    return created


def create_projects(n=30):
    """Crée n projets"""
    print(f"\n🔧 Création de {n} projets...")
    created = []

    for i in range(n):
        # Date aléatoire dans les 2 dernières années
        months_ago = random.randint(1, 24)
        date_fin = datetime.now() - timedelta(days=months_ago * 30)
        duree = random.randint(2, 18)

        project_name = random.choice(PROJECT_NAMES)
        if i > 0:
            project_name = f"{project_name} v{random.randint(1, 5)}"

        response = requests.post(f"{BASE_URL}/projects", json={
            "name": project_name,
            "date_fin": date_fin.strftime("%Y-%m"),
            "duree_mois": duree
        })

        if response.status_code == 201:
            data = response.json()
            created.append(data['id'])
            print(f"  ✅ {project_name} (ID: {data['id']}, {duree} mois)")

    print(f"✅ {len(created)} projets créés")
    return created


def create_competences(collaborator_ids, techno_ids, n=200):
    """Crée n compétences aléatoires"""
    print(f"\n🔧 Création de {n} compétences...")
    created = 0

    # Chaque collaborateur a entre 5 et 15 compétences
    for collab_id in collaborator_ids:
        nb_competences = random.randint(5, 15)
        selected_technos = random.sample(techno_ids, min(nb_competences, len(techno_ids)))

        for techno_id in selected_technos:
            niveau = random.randint(1, 5)

            response = requests.post(f"{BASE_URL}/competences", json={
                "id_collaborator": collab_id,
                "id_techno": techno_id,
                "niveau_declare": niveau,
                "niveau_calcule": niveau
            })

            if response.status_code == 201:
                created += 1
                if created % 20 == 0:
                    print(f"  ✅ {created} compétences créées...")

    print(f"✅ {created} compétences créées")
    return created


def create_project_history(project_ids, collaborator_ids, techno_ids, n=300):
    """Crée n entrées d'historique de projet"""
    print(f"\n🔧 Création de {n} entrées d'historique...")
    created = 0

    for project_id in project_ids:
        # Chaque projet a entre 2 et 5 développeurs
        nb_devs = random.randint(2, 5)
        selected_devs = random.sample(collaborator_ids, min(nb_devs, len(collaborator_ids)))

        # Chaque projet utilise entre 3 et 8 technologies
        nb_technos = random.randint(3, 8)
        selected_technos = random.sample(techno_ids, min(nb_technos, len(techno_ids)))

        # Obtenir les infos du projet
        project = requests.get(f"{BASE_URL}/projects/{project_id}").json()
        date_fin = project.get('date_fin')
        duree_mois = project.get('duree_mois', random.randint(3, 12))

        for dev_id in selected_devs:
            for techno_id in selected_technos:
                response = requests.post(f"{BASE_URL}/project_history", json={
                    "id_project": project_id,
                    "id_techno": techno_id,
                    "id_collaborator": dev_id,
                    "date_fin": date_fin,
                    "duree_mois": duree_mois
                })

                if response.status_code == 201:
                    created += 1
                    if created % 50 == 0:
                        print(f"  ✅ {created} entrées d'historique créées...")

    print(f"✅ {created} entrées d'historique créées")
    return created


def create_relations(techno_ids, type_ids, project_ids, collaborator_ids):
    """Crée les relations entre entités"""
    print(f"\n🔧 Création des relations...")
    created = {"techno_type": 0, "techno_project": 0, "collaborator_project": 0}

    # Techno ↔ Type
    for techno_id in techno_ids:
        # Chaque techno appartient à 1-3 types
        nb_types = random.randint(1, 3)
        selected_types = random.sample(type_ids, min(nb_types, len(type_ids)))

        for type_id in selected_types:
            response = requests.post(f"{BASE_URL}/techno_type", json={
                "id_techno": techno_id,
                "id_type": type_id
            })
            if response.status_code == 201:
                created["techno_type"] += 1

    # Techno ↔ Project
    for project_id in project_ids:
        nb_technos = random.randint(3, 8)
        selected_technos = random.sample(techno_ids, min(nb_technos, len(techno_ids)))

        for techno_id in selected_technos:
            response = requests.post(f"{BASE_URL}/techno_project", json={
                "id_techno": techno_id,
                "id_project": project_id
            })
            if response.status_code == 201:
                created["techno_project"] += 1

    # Collaborator ↔ Project
    for project_id in project_ids:
        nb_devs = random.randint(2, 5)
        selected_devs = random.sample(collaborator_ids, min(nb_devs, len(collaborator_ids)))

        for dev_id in selected_devs:
            response = requests.post(f"{BASE_URL}/collaborator_project", json={
                "id_collaborator": dev_id,
                "id_project": project_id
            })
            if response.status_code == 201:
                created["collaborator_project"] += 1

    print(f"✅ Relations créées: {created}")
    return created


def main():
    print("=" * 80)
    print("🚀 GÉNÉRATION DE FIXTURES MASSIVES")
    print("=" * 80)

    # Vérifier que l'API est accessible
    try:
        response = requests.get(f"{BASE_URL}/collaborators")
        if response.status_code != 200:
            print("❌ L'API n'est pas accessible. Assurez-vous que Flask est lancé.")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion à l'API: {e}")
        print("Assurez-vous que l'application Flask est lancée (python app.py)")
        return

    # Générer les fixtures
    collaborator_ids = create_collaborators(30)
    type_ids = create_types(TYPES)
    techno_ids = create_technologies(TECHNOLOGIES)
    project_ids = create_projects(30)

    # Créer les compétences
    create_competences(collaborator_ids, techno_ids)

    # Créer l'historique des projets
    create_project_history(project_ids, collaborator_ids, techno_ids)

    # Créer les relations
    create_relations(techno_ids, type_ids, project_ids, collaborator_ids)

    print("\n" + "=" * 80)
    print("✅ GÉNÉRATION TERMINÉE !")
    print("=" * 80)
    print("\n📊 Récapitulatif:")
    print(f"  - {len(collaborator_ids)} collaborateurs")
    print(f"  - {len(type_ids)} types")
    print(f"  - {len(techno_ids)} technologies")
    print(f"  - {len(project_ids)} projets")
    print("\n🎯 Prochaines étapes:")
    print("  1. Calculer les scores: curl -X POST http://localhost:5000/scoring/calculate")
    print("  2. Voir le dashboard: curl http://localhost:5000/dashboard/overview")
    print("  3. Voir la matrice: curl http://localhost:5000/matrix/competences")
    print("\n")


if __name__ == "__main__":
    main()
