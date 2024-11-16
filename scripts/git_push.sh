#!/bin/bash

# Verifica si se proporcionó un comentario como argumento
if [ -z "$1" ]; then
  echo "Error: No se proporcionó un comentario para el commit."
  echo "Uso: ./git_push.sh \"comentario del commit\""
  exit 1
fi

# Ejecutar los comandos de Git
echo "Añadiendo cambios al área de preparación..."
git add .

echo "Realizando commit con el mensaje: $1"
git commit -m "$1"

echo "Subiendo cambios al repositorio remoto..."
git push origin main

echo "¡Cambios subidos con éxito!"
