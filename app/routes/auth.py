# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario
from app import db
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(nombre_usuario=request.form['username']).first()
        if usuario and check_password_hash(usuario.contrasena_hash, request.form['password']):
            login_user(usuario)
            return redirect(url_for(f"panel.{usuario.rol.lower()}_dashboard"))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
