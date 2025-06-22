from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.usuario import Usuario
from app.models.aplicante import Aplicante 
from app.models.historial import Historial
from app import db
from sqlalchemy import text
import datetime
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask import Response
from sqlalchemy import or_, func



bp = Blueprint('panel', __name__)

# Dashboard Admin
@bp.route('/admin/dashboard')
@login_required
def administrador_dashboard():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403
    return render_template('panel_admin.html')

# Ver usuarios
@bp.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    usuarios = Usuario.query.filter(Usuario.rol != 'ADMINISTRADOR').all()
    return render_template('admin_usuarios.html', usuarios=usuarios)


# Agregar usuario
@bp.route('/admin/usuarios/agregar', methods=['GET', 'POST'])
@login_required
def admin_agregar_usuario():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        rol = request.form.get('rol', '').strip()

        if not nombre_usuario or not contrasena or not rol:
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('admin_agregar_usuarios.html')

        if rol not in ['ASISTENTE', 'DIRECTOR', 'CONSULTA']:
            flash('Rol no válido', 'danger')
            return render_template('admin_agregar_usuarios.html')

        usuario_existente = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario_existente:
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('admin_agregar_usuarios.html')

        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            contrasena_hash=generate_password_hash(contrasena),
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('panel.admin_usuarios'))

    # GET
    return render_template('admin_agregar_usuarios.html')




#Editar Usuario
@bp.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_editar_usuario(id):
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario', '').strip()
        rol = request.form.get('rol', '').strip()

        # Validar campos
        if not nombre_usuario or not rol:
            flash('Nombre de usuario y rol son obligatorios', 'danger')
            return render_template('admin_editar_usuario.html', usuario=usuario)

        if rol not in ['ASISTENTE', 'DIRECTOR', 'CONSULTA']:
            flash('Rol no válido', 'danger')
            return render_template('admin_editar_usuario.html', usuario=usuario)

        # Verificar que el nuevo nombre_usuario no exista en otro registro
        usuario_existente = Usuario.query.filter(
            Usuario.nombre_usuario == nombre_usuario,
            Usuario.id != id
        ).first()
        if usuario_existente:
            flash('El nombre de usuario ya está en uso por otro usuario', 'danger')
            return render_template('admin_editar_usuario.html', usuario=usuario)

        # Actualizar
        usuario.nombre_usuario = nombre_usuario
        usuario.rol = rol
        db.session.commit()

        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('panel.admin_usuarios'))

    # GET: mostrar formulario con datos actuales
    return render_template('admin_editar_usuario.html', usuario=usuario)

# Eliminar Usuario
@bp.route('/admin/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def admin_eliminar_usuario(id):
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    usuario = Usuario.query.get_or_404(id)

    # Opcional: evitar que admin se borre a sí mismo
    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propio usuario.", "danger")
        return redirect(url_for('panel.admin_usuarios'))

    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('panel.admin_usuarios'))


# Ver Historial
@bp.route('/admin/aplicantes')
@login_required
def admin_aplicantes():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    aplicantes = Aplicante.query.order_by(Aplicante.fecha_registro.desc()).all()
    return render_template('admin_aplicantes.html', aplicantes=aplicantes)

# Editar historial
@bp.route('/admin/historial/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_editar_historial(id):
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    historial = Historial.query.get_or_404(id)

    if request.method == 'POST':
        fecha_evento = request.form.get('fecha_evento')
        motivo = request.form.get('motivo')
        duracion_meses = request.form.get('duracion_meses') or None
        observaciones = request.form.get('observaciones') or None

        try:
            # Actualizar historial
            historial.fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%dT%H:%M')
            historial.motivo = motivo
            historial.duracion_meses = int(duracion_meses) if duracion_meses else None
            historial.observaciones = observaciones

            # También actualizar el estado del aplicante
            aplicante = Aplicante.query.get(historial.aplicante_id)
            if aplicante:
                aplicante.estado = motivo


            db.session.commit()
            flash('Historial y estado del aplicante actualizados correctamente.', 'success')
            return redirect(url_for('panel.admin_ver_todos_historial'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar historial: {e}', 'danger')

    fecha_evento_str = historial.fecha_evento.strftime('%Y-%m-%dT%H:%M')
    return render_template('admin_editar_historial.html', historial=historial, fecha_evento_str=fecha_evento_str)





#Agregar historial por aplicante

@bp.route('/admin/historial/agregar/<int:aplicante_id>', methods=['GET', 'POST'])
@login_required
def registrar_historial(aplicante_id):
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    if request.method == 'GET':
        return render_template('admin_historial.html', aplicante_id=aplicante_id)

    # POST
    fecha_evento = request.form.get('fecha_evento')
    motivo = request.form.get('motivo')
    duracion_meses = request.form.get('duracion_meses') or None
    observaciones = request.form.get('observaciones') or None

    try:
        fecha_evento_dt = datetime.strptime(fecha_evento, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Formato de fecha inválido. Usa el selector de fecha.', 'danger')
        return redirect(url_for('panel.registrar_historial', aplicante_id=aplicante_id))

    try:
        # 1. Insertar en tabla historial
        sql_historial = text("""
            EXEC RegistrarHistorial 
                @AplicanteId=:aplicante_id,
                @FechaEvento=:fecha_evento,
                @Motivo=:motivo,
                @DuracionMeses=:duracion_meses,
                @Observaciones=:observaciones
        """)
        db.session.execute(sql_historial, {
            'aplicante_id': aplicante_id,
            'fecha_evento': fecha_evento_dt,
            'motivo': motivo,
            'duracion_meses': duracion_meses,
            'observaciones': observaciones
        })
        


        # 2. Actualizar el estado del aplicante directamente en la tabla
        sql_update_estado = text("""
            UPDATE aplicantes
            SET estado = :nuevo_estado
            WHERE id = :aplicante_id
        """)
        db.session.execute(sql_update_estado, {
            'nuevo_estado': motivo,
            'aplicante_id': aplicante_id
        })

        db.session.commit()

        flash('Evento agregado al historial y estado actualizado correctamente.', 'success')
        return redirect(url_for('panel.admin_aplicantes'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar historial: {e}', 'danger')
        print(f"Error al registrar historial: {e}")
        return redirect(url_for('panel.registrar_historial', aplicante_id=aplicante_id))



# Ver historial
@bp.route('/admin/historial')
@login_required
def admin_historial():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403
    return render_template('admin_historial.html')

############################################################
# ver historial

@bp.route('/admin/historial/todos')
@login_required
def admin_ver_todos_historial():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    historial = Historial.query.options(joinedload(Historial.aplicante)).order_by(Historial.fecha_evento.desc()).all()
    return render_template('admin_ver_todos_historial.html', historial=historial)



# Dashboards otros roles
@bp.route('/asistente/dashboard')
@login_required
def asistente_dashboard():
    if current_user.rol != 'ASISTENTE':
        return "No autorizado", 403
    return render_template('panel_asistente.html')

@bp.route('/director/dashboard')
@login_required
def director_dashboard():
    if current_user.rol != 'DIRECTOR':
        return "No autorizado", 403
    return render_template('panel_director.html')

@bp.route('/consulta/dashboard')
@login_required
def consulta_dashboard():
    if current_user.rol != 'CONSULTA':
        return "No autorizado", 403
    return render_template('panel_consulta.html')


#Agregar aplicante a historial por eventos
@bp.route('/admin/aplicantes/agregar_historial/<int:id>', methods=['POST'])
@login_required
def admin_agregar_historial_evento(id):
    if current_user.rol != 'ADMINISTRADOR':
        flash('No autorizado', 'danger')
        return redirect(url_for('panel.admin_aplicantes'))

    # Verificar si ya existe un evento para ese aplicante
    existe_evento = db.session.execute(
        "SELECT 1 FROM historial_eventos WHERE aplicante_id = :id AND evento = 'Aplicante agregado a historial'",
        {'id': id}
    ).first()

    if existe_evento:
        flash('El aplicante ya tiene un historial por evento registrado.', 'warning')
        return redirect(url_for('panel.admin_aplicantes'))

    try:
        # Actualizamos la tabla aplicantes para disparar el trigger (aunque no cambiemos valores)
        db.session.execute(
            "UPDATE aplicantes SET estado = estado WHERE id = :id", {'id': id}
        )
        db.session.commit()
        flash('Historial por evento agregado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar historial por evento: {e}', 'danger')

    return redirect(url_for('panel.admin_aplicantes'))






#Historial por eventos

@bp.route('/admin/historial_eventos')
@login_required
def admin_ver_historial_eventos():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    # Traemos todos los eventos, ordenados por fecha descendente
    eventos = db.session.execute(
        "SELECT he.id, he.evento, he.aplicante_id, he.fecha, a.nombre_completo "
        "FROM historial_eventos he "
        "LEFT JOIN aplicantes a ON he.aplicante_id = a.id "
        "ORDER BY he.fecha DESC"
    ).fetchall()

    return render_template('admin_ver_historial_eventos.html', eventos=eventos)

@bp.route("/filtrar_aplicantes")
def filtrar_aplicantes():
    if current_user.rol not in ['ADMINISTRADOR','ASISTENTE','CONSULTA','DIRECTOR']:
        return "No autorizado", 403
    q = request.args.get("q", "").lower()
    aplicantes = Aplicante.query.filter(
        or_(
            func.lower(Aplicante.nombre_completo).like(f"%{q}%"),
            func.lower(Aplicante.pais).like(f"%{q}%"),
            func.lower(Aplicante.estado).like(f"%{q}%"),
            func.lower(Aplicante.carrera).like(f"%{q}%")
        )
    ).all()

    # Renderizamos solo las filas de la tabla como string
    html = ""
    for a in aplicantes:
        html += f"""
        <tr>
            <td class="px-4 py-2">{a.id}</td>
            <td class="px-4 py-2">{a.nombre_completo}</td>
            <td class="px-4 py-2">{a.documento}</td>
            <td class="px-4 py-2">{a.pais}</td>
            <td class="px-4 py-2">{a.carrera or '-'}</td>
            <td class="px-4 py-2">{a.universidad or '-'}</td>
            <td class="px-4 py-2">{a.estado}</td>
            <td class="px-4 py-2">{a.anio_aplicacion}</td>
            <td class="px-4 py-2 space-y-1">
                <a href="/admin/historial/agregar/{a.id}" class="block text-sm text-blue-600 hover:underline">
                Agregar a historial
                </a>
            </td>
        </tr>
        """
    if not aplicantes:
        html = '<tr><td colspan="9" class="text-center text-gray-500 py-4">No hay coincidencias.</td></tr>'
    
    return Response(html, mimetype='text/html')

@bp.route('/consulta/aplicantes')
@login_required
def consulta_aplicantes():
    if current_user.rol != 'CONSULTA':
        return "No autorizado", 403

    aplicantes = Aplicante.query.order_by(Aplicante.fecha_registro.desc()).all()
    return render_template('consulta_aplicantes.html', aplicantes=aplicantes)

# Vista de solo lectura para el rol DIRECTOR
@bp.route('/director/aplicantes')
@login_required
def director_aplicantes():
    if current_user.rol != 'DIRECTOR':
        return "No autorizado", 403

    aplicantes = Aplicante.query.order_by(Aplicante.fecha_registro.desc()).all()
    return render_template('consulta_aplicantes_director.html', aplicantes=aplicantes)
