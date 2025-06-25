"""
Rutas publicas
"""

from flask import Blueprint, render_template, redirect, request, flash, url_for, session, current_app
from flask_login import login_user
from ..forms.form_user import FormularioInicio, FormularioRegistro
from ..controllers.user_controller import UserController
from ..models.user import User
from ..extra_functions.notification_funct import send_gmail, send_gmail_confirmation
from ..extra_functions.token import genera_token
from ..extra_functions.public_decorator import no_enter
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

public_bp = Blueprint('public', __name__) 

@public_bp.route('/registro', methods=["GET", "POST"])
@no_enter
def registro():
    registro = FormularioRegistro()

    if request.method == "GET":
        return render_template("public/register.html", registro=registro)  
    
    elif request.method == "POST":
        if registro.validate_on_submit():
            email = registro.email.data
            usuario_email = User().get_by_email(email)
            # Evitar que se dupliquen emails
            if usuario_email:
                flash(f"Ese correo ya está registrado", "error")
                return redirect(url_for('public.registro'))
            else:
                # Si no hay duplicados se crea usuario y se abre sesión
                nombre = registro.nombre.data
                email = registro.email.data
                clave = registro.clave.data
                UserController().create_user(nombre, email, clave)
                user = User().get_by_email(email)
                login_user(user)
                send_gmail(email)
                token = genera_token(user.email)
                send_gmail_confirmation(token)
                return redirect(url_for('auth_bp.home'))
        
        flash(f"Las claves deben ser iguales", "error")
        return redirect(url_for('public.registro'))
        
@public_bp.route('/iniciar', methods=["GET", "POST"])
@no_enter
def inicio_sesion():
    login = FormularioInicio()
    
    if request.method == "GET":
        return render_template("public/login.html", login=login)
    
    if request.method == "POST":
        if login.validate_on_submit():
            email = login.email.data
            user = User().get_by_email(email)
            
            if user is None:
                flash("Usuario no registrado", "error")
                return redirect(url_for('public.inicio_sesion'))
            
            if user.check_password(login.clave.data):
                login_user(user)
                # Redirigir a la página que el usuario intentaba acceder originalmente
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('auth_bp.home'))
            
            flash("Clave incorrecta", "error")
            return redirect(url_for('public.inicio_sesion'))
        
        # Si el formulario no es válido
        flash("Por favor, verifica los datos ingresados", "error")
        return redirect(url_for('public.inicio_sesion'))

@public_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('public.login_google_callback', _external=True)
    flow = Flow.from_client_secrets_file(
        current_app.config['GOOGLE_CREDENTIALS_PATH'],
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=redirect_uri
    )
    authorization_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@public_bp.route('/login/google/callback')
def login_google_callback():
    state = session.get('state')
    redirect_uri = url_for('public.login_google_callback', _external=True)
    flow = Flow.from_client_secrets_file(
        current_app.config['GOOGLE_CREDENTIALS_PATH'],
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        state=state,
        redirect_uri=redirect_uri
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = google_requests.Request()
    id_info = id_token.verify_oauth2_token(credentials._id_token, request_session, flow.client_config['client_id'])
    email = id_info.get('email')
    name = id_info.get('name') or email.split('@')[0]
    user = User.get_by_email(email)
    if not user:
        # Registrar usuario si no existe
        from werkzeug.security import generate_password_hash
        user = User(username=name, email=email, password_hash=generate_password_hash(os.urandom(16).hex()), email_conf=True)
        from app import db
        db.session.add(user)
        db.session.commit()
    else:
        # Si el usuario ya existe y no tiene email_conf, lo marcamos como confirmado
        if not user.email_conf:
            user.email_conf = True
            from app import db
            db.session.commit()
    login_user(user)
    return redirect(url_for('auth_bp.home'))

