"""
Archivo de configuracion:\n
-mail \n
-base de datos\n
-etc\n
"""


import os 
from dotenv import load_dotenv 
 
load_dotenv() 
 
class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY', 'financeapp2025secretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:@localhost/finance')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Configuración de correo (Gmail API)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'yourfincancedashboardp@gmail.com')
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'PCclient_secret_746869307344-lsub4po2puj9ehtiqqs40mvtv0hl37p1.apps.googleusercontent.com.json')
    GOOGLE_TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', 'token.pickle')

    # Seguridad
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', '7de597aaaf91575c36cf235f99b49d28')

    """
    salt password:Tecnica de criptografia que añade cadena de caracteres aleatorios antes de aplicar una funcion hash
    """
