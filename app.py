from flask import Flask
from flask_cors import CORS
from src.config import init_db
from src.routes import (
    collaborators, types, projects, technos, relations,
    competences, project_history, imports,
    scoring, matrix, allocation, dashboard, cv_parser
)
import os

app = Flask(__name__)
CORS(app)

# Configuration pour les uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'json', 'pdf', 'txt', 'docx', 'doc'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Routes CRUD de base
app.register_blueprint(collaborators.bp)
app.register_blueprint(types.bp)
app.register_blueprint(projects.bp)
app.register_blueprint(technos.bp)
app.register_blueprint(relations.bp)
app.register_blueprint(competences.bp)
app.register_blueprint(project_history.bp)

# Routes d'import
app.register_blueprint(imports.bp)

# Routes MVP avancées
app.register_blueprint(scoring.bp)
app.register_blueprint(matrix.bp)
app.register_blueprint(allocation.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(cv_parser.bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
