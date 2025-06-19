# app/routes/panel.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('panel', __name__)

@bp.route('/admin/dashboard')
@login_required
def administrador_dashboard():
    if current_user.rol != 'ADMINISTRADOR':
        return "No autorizado", 403
    return render_template('panel_admin.html')

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
