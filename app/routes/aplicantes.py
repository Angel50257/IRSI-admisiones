# app/routes/aplicantes.py
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import text
from app import db

bp = Blueprint('aplicantes', __name__, url_prefix='/aplicantes')

@bp.route('/crear', methods=['POST'])
def crear_aplicante():
    data = request.get_json()

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
            'nombre': data['nombre_completo'],
            'fecha_nacimiento': data['fecha_nacimiento'],
            'documento': data['documento'],
            'pais': data['pais'],
            'universidad': data.get('universidad'),
            'carrera': data.get('carrera'),
            'grado': data.get('ultimo_grado_academico'), 
            'estado': data.get('estado', 'En curso'),
            'email': data.get('email'),
            'telefono': data.get('telefono'),
            'anio': data['anio_aplicacion'],
            'obs': data.get('observaciones')
        })

        db.session.commit()
        return jsonify({"mensaje": "Aplicante creado correctamente"}), 201

    except Exception as e:
        db.session.rollback()

        # Verificar si el error es por duplicado de documento
        if "Ya existe un aplicante con este documento" in str(e):
            return jsonify({"error": "Este documento ya está registrado. No se puede duplicar."}), 409

        # Otro error
        return jsonify({"error": "Error al guardar el aplicante: " + str(e)}), 400

    
@bp.route('/formulario', methods=['GET'])
def mostrar_formulario():
    return render_template('crear_aplicante.html')
