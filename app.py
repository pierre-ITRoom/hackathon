from flask import Flask
from flask_cors import CORS
from src.config import init_db
from src.routes import collaborators, types, projects, technos, relations

app = Flask(__name__)
CORS(app)

app.register_blueprint(collaborators.bp)
app.register_blueprint(types.bp)
app.register_blueprint(projects.bp)
app.register_blueprint(technos.bp)
app.register_blueprint(relations.bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
