import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import OperationalError  # Importar para manejar error de conexión

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Ruta base del paquete `app`
    
    # Directorios personalizados
    template_dir = os.path.abspath(os.path.join(base_dir, '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(base_dir, '..', 'static'))

    print("Directorio actual:", os.getcwd())
    print("Ruta absoluta de templates:", template_dir)
    print("Ruta absoluta de static:", static_dir)
    print("Contenido carpeta templates:", os.listdir(template_dir))

    # Crear app Flask con ruta a templates y static explícitas
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configuración desde archivo
    from config import Config
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # --- Aquí prueba la conexión a la base de datos ---
    with app.app_context():
        try:
            db.session.execute('SELECT 1')
            print("✅ Conexión a la base de datos exitosa")
        except OperationalError as e:
            print("❌ Error al conectar a la base de datos:", e)
    # ---------------------------------------------------

    # Configurar la vista de login por defecto
    login_manager.login_view = "auth.login"

    # Importar modelos para que SQLAlchemy los registre
    from app.models import usuario, aplicante

    # Ruta de inicio
    @app.route('/')
    def index():
        return render_template('index.html')

    # Registrar blueprints
    from app.routes import auth, aplicantes, panel
    app.register_blueprint(auth.bp)
    app.register_blueprint(aplicantes.bp)
    app.register_blueprint(panel.bp)

    return app

# Cargar usuario para Flask-Login
from app.models.usuario import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
