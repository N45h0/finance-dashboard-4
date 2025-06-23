#!/bin/bash
# Verificar que estamos en la carpeta correcta
if [ ! -f "requirements.txt" ]; then
  echo "Por favor, ejecuta este script desde la raíz del repositorio."
  exit 1
fi

echo "Activando el entorno virtual..."
# Detectar el sistema operativo
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

echo "Inicializando migraciones..."
flask db init

echo "Creando la migración inicial..."
flask db migrate -m "Migración inicial"

echo "Aplicando migraciones..."
flask db upgrade

echo "Iniciando la aplicación..."
python server.py