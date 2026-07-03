#!/bin/bash
set -e

# Cargar configuración desde .env.deploy
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
else
    echo "Error: scripts/.env.deploy no encontrado."
    echo "Copiá scripts/.env.deploy.example a scripts/.env.deploy y completá los valores."
    exit 1
fi

# Validaciones mínimas
if [ -z "$DEPLOY_SSH_HOST" ] || [ -z "$DEPLOY_SSH_PORT" ] || [ -z "$DEPLOY_SSH_USER" ] || [ -z "$DEPLOY_SERVICE_NAME" ]; then
    echo "Error: faltan variables en scripts/.env.deploy."
    echo "Copiá scripts/.env.deploy.example a scripts/.env.deploy y completá los valores."
    exit 1
fi

echo "Consultando logs remotos en $DEPLOY_SSH_HOST..."

SERVICE="${DEPLOY_SERVICE_NAME:-datamaq.service}"
ssh -p "$DEPLOY_SSH_PORT" "$DEPLOY_SSH_USER@$DEPLOY_SSH_HOST" "journalctl -u $SERVICE -n 20 --no-pager"
