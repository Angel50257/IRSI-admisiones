from app import db

class Aplicante(db.Model):
    __tablename__ = 'aplicantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    documento = db.Column(db.String(50), unique=True, nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    universidad = db.Column(db.String(100))
    carrera = db.Column(db.String(100))
    ultimo_grado_academico = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='En curso')
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    anio_aplicacion = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())