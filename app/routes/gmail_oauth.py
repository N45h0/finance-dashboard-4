from flask import Blueprint, redirect, url_for, session, request, current_app, flash, render_template_string
from google_auth_oauthlib.flow import Flow
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import pickle

bp_gmail_oauth = Blueprint('gmail_oauth', __name__)

@bp_gmail_oauth.route('/authorize')
def authorize():
    # Configuración de la ruta de redirección
    redirect_uri = url_for('gmail_oauth.callback', _external=True)
    flow = Flow.from_client_secrets_file(
        current_app.config['GOOGLE_CREDENTIALS_PATH'],
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        redirect_uri=redirect_uri
    )
    authorization_url, state = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@bp_gmail_oauth.route('/callback')
def callback():
    state = session.get('state')
    redirect_uri = url_for('gmail_oauth.callback', _external=True)
    flow = Flow.from_client_secrets_file(
        current_app.config['GOOGLE_CREDENTIALS_PATH'],
        scopes=['https://www.googleapis.com/auth/gmail.send'],
        state=state,
        redirect_uri=redirect_uri
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    # Guardar el token en el archivo configurado
    token_path = current_app.config['GOOGLE_TOKEN_PATH']
    with open(token_path, 'wb') as token:
        pickle.dump(credentials, token)
    flash('¡Autenticación exitosa! Ya puedes enviar correos con Gmail API.', 'success')
    return render_template_string('<h2>Autenticación exitosa</h2><p>Ya puedes cerrar esta ventana.</p>')
