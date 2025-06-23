from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from sqlalchemy import create_engine, text

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
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    
    # Cargar configuración
    app.config.from_object(Config)
      # Obtener la configuración de la base de datos desde las variables de entorno
    db_uri_base = Config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(db_uri_base.rsplit('/', 1)[0])
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS " + db_uri_base.rsplit('/', 1)[1]))
    
    # Configurar la URI de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_base
    
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

    return app
