"""
    Funciones de notificación usando la API de Gmail
"""

from flask_login import current_user
from flask import render_template, current_app, url_for
from app.models.importaciones import User, Email_message
from app.extra_functions.gmail_service import send_email as gmail_send_email
import random
import logging
import sys
from flask_apscheduler import APScheduler

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inicializar el scheduler
scheduler = APScheduler()

def send_email(to_email, subject, template_name, **template_args):
    """
    Función base para enviar correos electrónicos usando la API de Gmail
    """
    try:
        # Validar parámetros
        if not to_email or not subject or not template_name:
            raise ValueError("Email, subject y template son requeridos")

        # Renderizar el template con los argumentos proporcionados
        html = render_template(template_name, **template_args)
        
        # Enviar correo usando la API de Gmail
        if gmail_send_email(to_email, subject, html):
            # Guardar en la base de datos
            email_message = Email_message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=to_email,
                html_body=html
            )
            email_message.save()
            logger.info(f"Correo enviado exitosamente a {to_email}")
            return True
        else:
            logger.error(f"Error al enviar correo a {to_email}")
            return False
            
    except Exception as e:
        logger.error(f"Error general en send_email: {str(e)}")
        return False

def send_gmail_confirmation(token):
    """
    Envía la plantilla para confirmar tu correo con el token de seguridad
    """
    user = User().get_by_id(current_user.id)
    confirm_url = url_for('extra_functions.confirm_email', token=token, _external=True)
    return send_email(
        to_email=current_user.email,
        subject="Confirmacion de correo",  # Sin tilde para evitar problemas
        template_name="extra_functions/mailconfirmation.html",
        username=user.username,
        confirm_url=confirm_url
    )

def send_changepassword_request(token, user=None):
    """
    Envía correo para cambio de contraseña
    """
    if user is None:
        user = User().get_by_id(current_user.id)
    return send_email(
        to_email=user.email,
        subject="Cambio de contraseña",
        template_name="extra_functions/change_password/mail_message.html",
        username=user.username,
        token=token,
        form=None  # El formulario se manejará en la plantilla
    )

def send_changeemail_request(token):
    """
    Envía correo para cambio de email
    """
    user = User().get_by_id(current_user.id)
    return send_email(
        to_email=current_user.email,
        subject="Cambio de correo electrónico",
        template_name="extra_functions/change_email/mail_message.html",
        username=user.username,
        token=token,
        form=None  # El formulario se manejará en la plantilla
    )

def send_gmail(recipient):
    """
    Envía un mensaje de bienvenida al correo
    """
    user = User().get_by_id(current_user.id)
    return send_email(
        to_email=recipient,
        subject="¡Bienvenido/a!",
        template_name="extra_functions/mail.html",
        username=user.username
    )

def daily_email():
    """
    Envía un mensaje diario a las 9:00 AM a todos los usuarios
    """
    try:
        # Obtener todos los usuarios
        users = User().get_all()
        if not users:
            logger.warning("No hay usuarios para enviar correos diarios")
            return

        # Obtener mensajes disponibles y elegir uno al azar
        messages = Email_message().get_all()
        if not messages:
            logger.warning("No hay mensajes disponibles para enviar")
            return

        message_elected = random.choice(messages).template_name

        # Enviar a cada usuario
        for user in users:
            try:
                send_email(
                    to_email=user.email,
                    subject="Mensaje informativo diario",
                    template_name=f"extra_functions/messages_dialy/{message_elected}"
                )
            except Exception as e:
                logger.error(f"Error enviando correo diario a {user.email}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error en daily_email: {str(e)}")

# Configurar el trabajo programado
scheduler.add_job(
    id="daily_email_job",
    func=daily_email,
    trigger="cron",
    hour=9,
    minute=0
)

# El scheduler se iniciará cuando la aplicación Flask lo inicie