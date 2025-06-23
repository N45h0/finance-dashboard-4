# Finance Dashboard

## Descripción
Finance Dashboard es una aplicación web que te permite gestionar tus finanzas personales. Con ella podrás llevar el control de ingresos, gastos, servicios, préstamos y generar informes financieros.

## Características
- Gestión de cuentas bancarias
- Registro de ingresos y gastos
- Control de servicios y pagos
- Administración de préstamos
- Informes financieros

## Requisitos
- **Python 3.8+**
- **MySQL** (puedes usar XAMPP para un entorno local)

## Instalación y Configuración

### 1. Clonar el Repositorio
Clona el repositorio privado en tu cuenta personal de GitHub:
```bash
git clone https://github.com/N45h0/finance-dashboard-3.git
cd FinanceDashboard
```

### 2. Crear y Activar el Entorno Virtual
Crea y activa un entorno virtual para aislar las dependencias:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
Instala las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Copia el archivo `.env.example` a `.env` y edítalo con tus datos reales:
```bash
# En Linux/Mac:
cp .env.example .env
# En Windows:
copy .env.example .env
```
Edita `.env` para poner tus credenciales de base de datos, claves secretas y rutas de credenciales de Google.

### 5. Configurar Credenciales de Google
- Descarga tu archivo `client_secret_XXXX.json` desde Google Cloud Console y colócalo en la raíz del proyecto.
- Asegúrate de que el nombre y la ruta coincidan con lo especificado en `.env`.
- Este archivo está en `.gitignore` y **no debe subirse al repositorio**.

### 6. Inicializar la Base de Datos y Migraciones
Puedes usar el script automático:
```bash
# En Windows:
setup.bat
# En Linux/Mac:
./setup.sh
```
O manualmente:
```bash
flask db init
flask db migrate -m "Migración inicial"
flask db upgrade
```

### 7. Ejecutar la Aplicación
```bash
python server.py
```
La aplicación estará disponible en `http://localhost:5000`.

## Recomendaciones de Seguridad y Buenas Prácticas
- Nunca subas archivos de credenciales ni `.env` a git.
- Cambia las claves secretas y salts antes de producción.
- Revisa y actualiza `.gitignore` para proteger información sensible.
- Sube el proyecto a un repositorio privado en tu cuenta personal de GitHub antes de producción.

## Personalización y Desarrollo
- Puedes personalizar el favicon reemplazando el archivo `app/static/favicon.ico`.
- Se recomienda usar Visual Studio Code por su terminal integrada, control de versiones y extensiones útiles para Python y Flask.

## Despliegue en Producción
1. Verifica que `.env` y los archivos de credenciales **no estén en el repositorio**.
2. Configura las variables de entorno y credenciales en el servidor de producción.
3. Realiza migraciones y ejecuta la aplicación como en local.

## Despliegue en Hosting Compartido con DirectAdmin (sin SSH)

### 1. Preparar el Proyecto para Subir
- **No subas**: carpetas `venv/`, `env/`, `__pycache__/`, archivos `.pyc`, `.env`, archivos de credenciales sensibles (`client_secret*.json`, `token.pickle`), ni nada listado en `.gitignore`.
- **Sí sube**: todo el código fuente, carpetas `app/`, `requirements.txt`, `config.py`, `server.py`, archivos de migración si los tienes, y archivos estáticos/plantillas.
- **Recomendado**: Comprime solo lo necesario en un `.zip` (ver ejemplo abajo).

#### Ejemplo de estructura a comprimir:
```
app/
config.py
requirements.txt
server.py
setup.sh
setup.bat
README.md
.env.example
migrations/ (si existe)
static/ (si existe)
templates/ (si existe)
```

### 2. Subir y Descomprimir el Proyecto
- Usa el administrador de archivos de DirectAdmin para subir el `.zip` a la carpeta de tu app Python (usualmente fuera de `public_html`).
- Descomprime el archivo desde el panel.

### 3. Crear la Aplicación Python en DirectAdmin
- Ve a "Setup Python App" en el panel.
- Elige la versión de Python (3.8+ recomendado).
- Define la ruta donde subiste el proyecto.
- En "Application startup file" pon: `passenger_wsgi.py`
- En "Application entry point" pon: `app`

### 4. Crear el archivo WSGI
Crea un archivo llamado `passenger_wsgi.py` en la raíz del proyecto con este contenido:
```python
from app import create_app
app = create_app()
```

### 5. Instalar Dependencias
- En el panel de la app Python, usa la opción para instalar paquetes desde `requirements.txt`.

### 6. Configurar Variables de Entorno
- En el panel, agrega manualmente las variables de entorno que estaban en tu `.env` (por ejemplo: `SECRET_KEY`, `DATABASE_URL`, etc.).

### 7. Configurar la Base de Datos
- Crea la base de datos y usuario desde DirectAdmin.
- Actualiza la variable `DATABASE_URL` con los datos reales.

### 8. Migraciones y Archivos Estáticos
- Si no tienes SSH, ejecuta migraciones localmente y sube la base de datos migrada, o pide soporte al hosting para ejecutar comandos.
- Asegúrate de que los archivos estáticos y plantillas estén en las carpetas correctas.

### 9. Probar la Aplicación
- Accede a tu dominio/subdominio y verifica que la app funcione correctamente.

#### Notas de Seguridad
- Nunca subas `.env` ni archivos de credenciales reales.
- Cambia las claves secretas y salts antes de producción.
- Usa un repositorio privado para tu código fuente.

## Contacto
Para dudas o soporte, contacta al desarrollador principal.