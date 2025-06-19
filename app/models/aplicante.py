# app/models/aplicante.py
from app import db

class Aplicante(db.Model):
    __tablename__ = 'aplicantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    documento = db.Column(db.String(50), unique=True)
    pais = db.Column(db.String(50))
    universidad = db.Column(db.String(100))
    carrera = db.Column(db.String(100))
    ultimo_grado_academico = db.Column(db.String(100)) 
    estado = db.Column(db.String(20))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    anio_aplicacion = db.Column(db.Integer)
    observaciones = db.Column(db.Text)
