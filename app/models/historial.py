from app import db

class Historial(db.Model):
    __tablename__ = 'historial'

    id = db.Column(db.Integer, primary_key=True)
    aplicante_id = db.Column(db.Integer, db.ForeignKey('aplicantes.id'), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    duracion_meses = db.Column(db.Integer)
    observaciones = db.Column(db.Text)

    # Relación opcional con el modelo Aplicante
    aplicante = db.relationship('Aplicante', backref='historiales')
