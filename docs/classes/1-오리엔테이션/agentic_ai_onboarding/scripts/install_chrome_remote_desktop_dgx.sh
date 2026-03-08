#!/usr/bin/env bash
# Install Chrome Remote Desktop + XFCE on Ubuntu/Debian (e.g. dgx-spark).
# NOTE: Google only provides amd64 .deb. On ARM64 (e.g. dgx-spark), this script exits with alternatives.
#
# Copy to server and run (from this repo root on your Mac):
#   scp docs/classes/1-오리엔테이션/agentic_ai_onboarding/scripts/install_chrome_remote_desktop_dgx.sh dgx-spark:~/
#   ssh dgx-spark 'chmod +x install_chrome_remote_desktop_dgx.sh && ./install_chrome_remote_desktop_dgx.sh'
#
# After this script, complete authorization at https://remotedesktop.google.com/headless

set -e

ARCH=$(dpkg --print-architecture 2>/dev/null || uname -m)
if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
  echo "This system is ARM64 ($ARCH). Google does not provide Chrome Remote Desktop for Linux ARM64 (amd64 only)."
  echo ""
  echo "Alternatives for remote desktop on dgx-spark:"
  echo "  - xrdp:  sudo apt install -y xrdp xorgxrdp; sudo systemctl enable --now xrdp"
  echo "  - VNC:   sudo apt install -y tigervnc-standalone-server tigervnc-common (then vncserver)"
  echo "  - Cursor/VS Code: Use Remote-SSH to edit and run; no full desktop needed."
  echo ""
  exit 1
fi

echo "[1/6] Updating apt and installing wget..."
sudo apt update
sudo apt-get install -y wget

echo "[2/6] Downloading Chrome Remote Desktop .deb (amd64)..."
sudo wget -q -O /tmp/chrome-remote-desktop.deb https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
test -s /tmp/chrome-remote-desktop.deb || { echo "Download failed."; exit 1; }

echo "[3/6] Installing Chrome Remote Desktop (and fixing dependencies)..."
sudo dpkg --install /tmp/chrome-remote-desktop.deb 2>/dev/null || true
sudo apt install -y --fix-broken
# Ensure CRD is fully installed (second pass in case deps were missing)
sudo dpkg -s chrome-remote-desktop >/dev/null 2>&1 || sudo dpkg --install /tmp/chrome-remote-desktop.deb
sudo apt install -y --fix-broken

echo "[4/6] Installing XFCE desktop (required for CRD headless session)..."
sudo DEBIAN_FRONTEND=noninteractive apt install -y xfce4 desktop-base

echo "[5/6] Configuring CRD to use XFCE session and xscreensaver..."
sudo bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'
sudo apt install -y xscreensaver

echo "[6/6] Group and user for Chrome Remote Desktop..."
if ! getent group chrome-remote-desktop >/dev/null 2>&1; then
  sudo groupadd -r chrome-remote-desktop
  echo "Created group chrome-remote-desktop."
fi
sudo usermod -a -G chrome-remote-desktop "$USER"

echo ""
if [[ -x /opt/google/chrome-remote-desktop/start-host ]]; then
  echo "=== Install complete ==="
  echo "start-host: /opt/google/chrome-remote-desktop/start-host (OK)"
  echo ""
  echo "Next steps:"
  echo "1. Log out and log back in (or run: newgrp chrome-remote-desktop)"
  echo "2. On your PC, open: https://remotedesktop.google.com/headless"
  echo "3. Sign in with Google, copy the Debian/Linux command, run it HERE on this server."
  echo "4. Set a 6+ digit PIN when prompted."
  echo "5. Connect from: https://remotedesktop.google.com/access"
else
  echo "=== WARNING: start-host not found ==="
  echo "Chrome Remote Desktop may not have installed correctly."
  echo "Check: ls -la /opt/google/chrome-remote-desktop/"
  exit 1
fi
echo ""
