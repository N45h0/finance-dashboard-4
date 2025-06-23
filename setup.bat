@echo off
REM Verificar que estamos en la carpeta correcta
if not exist "requirements.txt" (
    echo Por favor, ejecuta este script desde la raiz del repositorio.
    exit /b 1
)

echo Activando el entorno virtual...
call venv\Scripts\activate.bat

echo Inicializando migraciones...
flask db init

echo Creando la migracion inicial...
flask db migrate -m "Migracion inicial"

echo Aplicando migraciones...
flask db upgrade

echo Iniciando la aplicacion...
python server.py
