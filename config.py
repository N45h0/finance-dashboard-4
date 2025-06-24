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
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Configuración de correo (Gmail API)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', '')
    GOOGLE_TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', '')

    # Seguridad
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', '')

    """
    salt password:Tecnica de criptografia que añade cadena de caracteres aleatorios antes de aplicar una funcion hash
    """
