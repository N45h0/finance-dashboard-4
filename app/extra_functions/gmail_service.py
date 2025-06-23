import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from flask import current_app
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'client_secret_746869307344-lsub4po2puj9ehtiqqs40mvtv0hl37p1.apps.googleusercontent.com.json')

def get_gmail_service():
    """
    Obtiene o crea el servicio de Gmail autenticado.
    """
    creds = None
    
    # Cargar credenciales existentes si están disponibles
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            try:
                creds = pickle.load(token)
            except Exception as e:
                logger.error(f"Error al cargar el token: {e}")
    
    # Si no hay credenciales válidas, solicitar al usuario que inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Error al refrescar el token: {e}")
                creds = None
        
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Guardar las credenciales para la próxima ejecución
                with open(TOKEN_PATH, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                logger.error(f"Error en el flujo de autenticación: {e}")
                raise
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Error al construir el servicio de Gmail: {e}")
        raise

def send_email(to, subject, html_content):
    """
    Envía un correo usando la API de Gmail.
    
    Args:
        to (str): Dirección de correo del destinatario
        subject (str): Asunto del correo
        html_content (str): Contenido HTML del correo
    """
    try:
        service = get_gmail_service()
        
        message = MIMEText(html_content, 'html', 'utf-8')
        message['to'] = to
        message['subject'] = subject
        message['from'] = current_app.config['MAIL_DEFAULT_SENDER']
        
        # Codificar el mensaje para la API de Gmail
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        message_body = {'raw': raw_message}
        
        # Enviar el mensaje
        sent_message = service.users().messages().send(userId='me', body=message_body).execute()
        logger.info(f"Mensaje enviado exitosamente. Message Id: {sent_message['id']}")
        return True
        
    except Exception as e:
        logger.error(f"Error al enviar el correo: {e}")
        return False
