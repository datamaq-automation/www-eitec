#!/bin/bash
set -e

# Script de bootstrap para ejecutar EN EL VPS como root.
# No ejecutar en la máquina de desarrollo local.

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: este script debe ejecutarse como root en el VPS."
    echo "En tu máquina local no tenés permisos para crear usuarios del sistema."
    exit 1
fi

# Cargar configuración desde .env.deploy si existe; usar defaults seguros si no.
if [ -f "scripts/.env.deploy" ]; then
    source scripts/.env.deploy
fi

APP_USER="${DEPLOY_SSH_USER:-datamaq}"
APP_DIR="${DEPLOY_REMOTE_DIR:-/var/www/datamaq}"
SERVICE="${DEPLOY_SERVICE_NAME:-datamaq.service}"

echo "==> Configuración: usuario=$APP_USER, directorio=$APP_DIR, servicio=$SERVICE"

echo "==> Creando usuario $APP_USER..."
if id "$APP_USER" &>/dev/null; then
    echo "El usuario $APP_USER ya existe. Asegurando shell y home..."
    usermod -s /bin/bash "$APP_USER"
else
    # Usuario normal con home y shell bash, sin contraseña (login solo por SSH key).
    adduser --disabled-password --gecos "" --home "$APP_DIR" "$APP_USER"
fi

echo "==> Asegurando permisos de $APP_DIR..."
mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "==> Configurando sudoers para reiniciar el servicio..."
cat > "/etc/sudoers.d/$APP_USER-deploy" <<EOF
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart $SERVICE
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl is-active $SERVICE
$APP_USER ALL=(ALL) NOPASSWD: /bin/systemctl status $SERVICE
EOF
chmod 440 "/etc/sudoers.d/$APP_USER-deploy"

echo "==> Configurando servicio $SERVICE..."
if [ -f "/etc/systemd/system/$SERVICE" ]; then
    sed -i "s|^User=.*|User=$APP_USER|" "/etc/systemd/system/$SERVICE"
    sed -i "s|^Group=.*|Group=$APP_USER|" "/etc/systemd/system/$SERVICE"
    sed -i "s|^WorkingDirectory=.*|WorkingDirectory=$APP_DIR|" "/etc/systemd/system/$SERVICE"
    sed -i "s|^ExecStart=.*|ExecStart=$APP_DIR/.venv/bin/python3 -m uvicorn src.infrastructure.fastapi.app:app --host 127.0.0.1 --port 8000|" "/etc/systemd/system/$SERVICE"
    sed -i "s|^EnvironmentFile=.*|EnvironmentFile=$APP_DIR/.env|" "/etc/systemd/system/$SERVICE"
    systemctl daemon-reload
    systemctl restart "$SERVICE"
else
    echo "ADVERTENCIA: No se encontró /etc/systemd/system/$SERVICE"
    echo "Creá el archivo manualmente según docs/CD.md"
fi

echo "==> Configuración completada."
echo "Verificá que el servicio esté activo con: sudo systemctl is-active $SERVICE"
echo ""
echo "Para habilitar deploy por SSH, agregá la clave pública del desarrollador a:"
echo "  $APP_DIR/.ssh/authorized_keys"
