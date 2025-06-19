from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = Usuario(
        nombre_usuario='admin',
        contrasena_hash=generate_password_hash('1234'),
        rol='ADMINISTRADOR'
    )
    db.session.add(admin)
    db.session.commit()
    print("Usuario administrador creado.")
