#!/bin/bash

# Verificar si se pasó un mensaje de commit
if [ -z "$1" ]; then
  echo "Error: Debes proporcionar un mensaje para el commit."
  exit 1
fi

# Verificar si hay cambios sin confirmar
if ! git diff-index --quiet HEAD --; then
  echo "Tienes cambios sin confirmar. Guardándolos temporalmente..."
  git stash
fi

echo "Descargando los últimos cambios del repositorio remoto..."
git pull origin main --rebase
if [ $? -ne 0 ]; then
  echo "Error: No se pudo completar el pull. Resuelve conflictos manualmente y vuelve a intentarlo."
  exit 1
fi

if git stash list | grep -q "stash@{0}"; then
  echo "Aplicando cambios guardados..."
  git stash pop
fi

echo "Añadiendo cambios al área de preparación..."
git add .

echo "Realizando commit con el mensaje: $1"
git commit -m "$1"
if [ $? -ne 0 ]; then
  echo "Error: No se pudo realizar el commit. Asegúrate de que hay cambios que confirmar."
  exit 1
fi

echo "Subiendo cambios al repositorio remoto..."
git push origin main
if [ $? -ne 0 ]; then
  echo "Error: No se pudo realizar el push. Asegúrate de que no hay conflictos pendientes."
  exit 1
fi

echo "¡Cambios subidos con éxito!"

