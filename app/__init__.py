from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from sqlalchemy import create_engine, text
import secrets
from flask import g, request, after_this_request

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = None

def create_app():
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Configuración de codificación global
    import sys
    import locale
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        print("Locale 'es_ES.UTF-8' not supported, continuing with default locale.")
    
    # Cargar configuración
    app.config.from_object(Config)

    
    # Configurar la URI de la base de datos
    #app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_base
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'public.inicio_sesion'  # Ruta al endpoint de inicio de sesión
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Importar modelos para la migración
    from app.models import (
        user, account, income, loan, service,
        service_payment, loan_payment, scheduled_incomes,
        emailmessage
    )
    
    # Configurar el cargador de usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return user.User().get_by_id(int(user_id))    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.create_functions import create_functions_bp
    from app.routes.update_functions import update_functions_bp
    from app.routes.extra_functions import extra_functions_bp
    from app.routes.public import public_bp
    from app.routes.gmail_oauth import bp_gmail_oauth

    app.register_blueprint(auth_bp)
    app.register_blueprint(create_functions_bp)
    app.register_blueprint(update_functions_bp)
    app.register_blueprint(extra_functions_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(bp_gmail_oauth)

    # --- CSP y Nonce ---
    @app.before_request
    def set_csp_nonce():
        g.csp_nonce = secrets.token_urlsafe(16)

    @app.context_processor
    def inject_csp_nonce():
        return {'csp_nonce': getattr(g, 'csp_nonce', '')}

    @app.after_request
    def set_csp_header(response):
        nonce = getattr(g, 'csp_nonce', '')
        csp = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://accounts.google.com https://apis.google.com https://cdn.jsdelivr.net 'sha256-LnIcMTTMRZTNS6HkTiExB0sk5mPuVe0yVzmaBz8GaIY='; "
            f"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            f"font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            f"img-src 'self' data: https://*.googleusercontent.com; "
            f"connect-src 'self' https://accounts.google.com https://oauth2.googleapis.com; "
            f"frame-src https://accounts.google.com;"
        )
        response.headers['Content-Security-Policy'] = csp
        return response

    return app
