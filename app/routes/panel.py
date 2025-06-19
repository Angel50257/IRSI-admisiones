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


# Ver Aplicante
@bp.route('/admin/aplicantes')
@login_required
def admin_aplicantes():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403

    aplicantes = Aplicante.query.order_by(Aplicante.fecha_registro.desc()).all()
    return render_template('admin_aplicantes.html', aplicantes=aplicantes)


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

    print(f"Debug: {fecha_evento=}, {motivo=}, {duracion_meses=}, {observaciones=}")

    # Convertir fecha_evento a datetime para SQL Server
    try:
        fecha_evento_dt = datetime.strptime(fecha_evento, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Formato de fecha inválido. Usa el selector de fecha.', 'danger')
        return redirect(url_for('panel.registrar_historial', aplicante_id=aplicante_id))

    try:
        
        sql = text("""
            EXEC RegistrarHistorial 
                @AplicanteId=:aplicante_id,
                @FechaEvento=:fecha_evento,
                @Motivo=:motivo,
                @DuracionMeses=:duracion_meses,
                @Observaciones=:observaciones
        """)

        db.session.execute(sql, {
            'aplicante_id': aplicante_id,
            'fecha_evento': fecha_evento_dt,
            'motivo': motivo,
            'duracion_meses': duracion_meses,
            'observaciones': observaciones
        })
        db.session.commit()

        flash('Evento agregado al historial correctamente.', 'success')
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
