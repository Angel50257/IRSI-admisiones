# app/routes/aplicantes.py
from flask import Blueprint, request, jsonify, render_template, send_file
from sqlalchemy import text
from app import db
import pandas as pd
from io import BytesIO
from app.models.aplicante import Aplicante
from flask_login import login_required, current_user
import io

bp = Blueprint('aplicantes', __name__, url_prefix='/aplicantes')

@bp.route('/crear', methods=['GET', 'POST'])
def crear_aplicante():
    if request.method == 'GET':
        return render_template('crear_aplicante.html')
    
    # POST: detectar si el contenido es JSON o form tradicional
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    try:
        stmt = text("""
            EXEC InsertarAplicante
                @NombreCompleto=:nombre,
                @FechaNacimiento=:fecha_nacimiento,
                @Documento=:documento,
                @Pais=:pais,
                @Universidad=:universidad,
                @Carrera=:carrera,
                @UltimoGradoAcademico=:grado,
                @Estado=:estado,
                @Email=:email,
                @Telefono=:telefono,
                @AnioAplicacion=:anio,
                @Observaciones=:obs
        """)

        db.session.execute(stmt, {
            'nombre': data.get('nombre_completo'),
            'fecha_nacimiento': data.get('fecha_nacimiento'),
            'documento': data.get('documento'),
            'pais': data.get('pais'),
            'universidad': data.get('universidad'),
            'carrera': data.get('carrera'),
            'grado': data.get('ultimo_grado_academico'), 
            'estado': data.get('estado', 'En curso'),
            'email': data.get('email'),
            'telefono': data.get('telefono'),
            'anio': data.get('anio_aplicacion'),
            'obs': data.get('observaciones')
        })

        db.session.commit()
        return jsonify({"mensaje": "Aplicante creado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar el aplicante: " + str(e)}), 400

@bp.route('/exportar_excel')
@login_required
def exportar_excel():
    aplicantes = Aplicante.query.all()

    data = [{
        'Nombre': a.nombre_completo,
        'Nacimiento': a.fecha_nacimiento,
        'Documento': a.documento,
        'País': a.pais,
        'Universidad': a.universidad,
        'Carrera': a.carrera,
        'Grado Académico': a.ultimo_grado_academico,
        'Email': a.email,
        'Teléfono': a.telefono,
        'Año Aplicación': a.anio_aplicacion,
        'Estado': a.estado,
        'Fecha Registro': a.fecha_registro,
        'Observaciones': a.observaciones,
    } for a in aplicantes]

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Aplicantes')

    output.seek(0)
    return send_file(
        output,
        download_name="aplicantes.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )