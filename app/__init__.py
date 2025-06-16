from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Redirección por defecto si no hay login
    login_manager.login_view = "auth.login"

    # Importar modelos para que SQLAlchemy los registre
    from app.models import usuario, aplicante

    # Importar y registrar Blueprints
    from app.routes import auth, aplicantes, panel
    app.register_blueprint(auth.bp)
    app.register_blueprint(aplicantes.bp)
    app.register_blueprint(panel.bp)

    return app

# Flask-Login loader
from app.models.usuario import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
