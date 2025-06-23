"""
Archivo despliegue
"""

from app import create_app, db
from flask_migrate import Migrate

app = create_app()  # aplicacion
migrate = Migrate(app, db)  # inicializar Flask-Migrate

if __name__=="__main__":
    app.run(debug=True)