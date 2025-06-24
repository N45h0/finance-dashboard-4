# server.py
# Este es el archivo que Gunicorn usará como punto de entrada.

from app import create_app

app = create_app()

# No es necesario nada más aquí.
# No llames a app.run(). Gunicorn se encarga de todo.
# Las rutas deben definirse dentro de tu 'create_app' o en los blueprints que importa.
