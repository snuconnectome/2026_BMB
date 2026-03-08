#!/usr/bin/env bash
# Headless 서버에서 가상 디스플레이(Xvfb) + XFCE를 띄워 TeamViewer가 블랙 화면 없이 보이도록 설정.
# dgx-spark 등 모니터 없이 사용하는 서버에서 실행.
#
# 복사 후 실행 (로컬에서):
#   scp docs/classes/1-오리엔테이션/agentic_ai_onboarding/scripts/setup_headless_xfce_for_teamviewer.sh dgx-spark:~/
#   ssh dgx-spark 'chmod +x setup_headless_xfce_for_teamviewer.sh && ./setup_headless_xfce_for_teamviewer.sh'
#
# 서비스 시작: sudo systemctl start xfce-xvfb@$USER
# 부팅 시 자동: sudo systemctl enable xfce-xvfb@$USER

set -e

USER_NAME="${SUDO_USER:-$USER}"
USER_HOME=$(getent passwd "$USER_NAME" | cut -d: -f6)
SERVICE_NAME="xfce-xvfb@${USER_NAME}.service"
SCRIPT_PATH="/usr/local/bin/start-xfce-on-xvfb.sh"

echo "[1/5] Installing Xvfb and XFCE..."
sudo apt update
sudo apt install -y xvfb xfce4 xfce4-goodies dbus-x11

echo "[2/5] Creating startup script for virtual display :99..."
sudo tee "$SCRIPT_PATH" << 'SCRIPT'
#!/bin/bash
# Xvfb on :99, then start XFCE so TeamViewer has a desktop to show.
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 -ac &
XVFB_PID=$!
sleep 3
if ! kill -0 $XVFB_PID 2>/dev/null; then
  echo "Xvfb failed to start." >&2
  exit 1
fi
exec startxfce4
SCRIPT
sudo chmod +x "$SCRIPT_PATH"

echo "[3/5] Creating systemd user service (runs as $USER_NAME)..."
sudo tee "/etc/systemd/system/xfce-xvfb@.service" << 'UNIT'
[Unit]
Description=XFCE on Xvfb (virtual display) for user %i
After=network.target

[Service]
Type=simple
User=%i
Environment=DISPLAY=:99
Environment=HOME=/home/%i
Environment=USER=%i
Environment=LOGNAME=%i
ExecStart=/usr/local/bin/start-xfce-on-xvfb.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

echo "[4/5] Adding TeamViewer to XFCE autostart (so it runs on display :99)..."
mkdir -p "$USER_HOME/.config/autostart"
cat > "$USER_HOME/.config/autostart/teamviewer.desktop" << 'AUTOSTART'
[Desktop Entry]
Type=Application
Name=TeamViewer
Exec=env DISPLAY=:99 teamviewer
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
AUTOSTART
chown -R "$USER_NAME:$USER_NAME" "$USER_HOME/.config/autostart" 2>/dev/null || true

echo "[5/5] Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME" || true

echo ""
echo "=== Setup complete ==="
echo "Service: $SERVICE_NAME"
echo "Display :99 now runs XFCE; TeamViewer is in autostart for that session."
echo "Check: sudo systemctl status $SERVICE_NAME"
echo ""
echo "If still black: wait 30s for XFCE to fully start, then reconnect TeamViewer."
echo "Restart: sudo systemctl restart $SERVICE_NAME"
echo ""
