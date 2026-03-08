# dgx-spark에 Chrome Remote Desktop 설치 및 설정

**뇌마음행동 과정 | 서울대학교 커넥톰연구실 (차지욱 교수)**

dgx-spark(헤드리스 서버)에 Chrome Remote Desktop(CRD)을 설치하면, 로컬 PC의 Chrome 브라우저나 CRD 앱으로 **GUI 원격 데스크톱**에 접속할 수 있습니다. SSH만으로는 불편한 GUI 작업(예: 브라우저, 일부 도구)에 유용합니다.

---

## ⚠️ dgx-spark가 ARM64인 경우

**Google은 Linux용 Chrome Remote Desktop을 amd64만 제공합니다.** dgx-spark가 **ARM64(aarch64)** 이면 CRD .deb를 설치할 수 없습니다. 이 경우 아래 **대안**을 사용하세요.

| 대안 | 설명 |
|------|------|
| **xrdp** | RDP 프로토콜. Windows 원격 데스크톱 또는 Remmina 등으로 접속. `sudo apt install -y xrdp xorgxrdp` 후 `sudo systemctl enable --now xrdp` |
| **TigerVNC** | VNC 서버. RealVNC/Remmina 등 VNC 클라이언트로 접속. `sudo apt install -y tigervnc-standalone-server` 후 `vncserver` 실행 |
| **Cursor / VS Code Remote-SSH** | 전체 데스크톱 대신 에디터만 원격. 이미 Tailscale + SSH로 접속 중이라면 코드 편집·실행은 Remote-SSH로 가능 |

---

## TeamViewer 블랙 화면 해결 (헤드리스 / 모니터 없음)

TeamViewer로 접속은 되는데 **화면이 계속 검은 경우**: 원격 쪽에 **실제로 떠 있는 GUI 세션이 없어서** 그렇습니다. 가상 디스플레이(Xvfb)에서 XFCE를 띄우고, TeamViewer가 그 세션에서 실행되도록 하면 됩니다.

**한 번에 설정 (스크립트):**

```bash
# 로컬에서 스크립트 복사
scp docs/classes/1-오리엔테이션/agentic_ai_onboarding/scripts/setup_headless_xfce_for_teamviewer.sh dgx-spark:~/

# dgx-spark에서 실행 (sudo 비밀번호 입력)
ssh dgx-spark
chmod +x setup_headless_xfce_for_teamviewer.sh
sudo ./setup_headless_xfce_for_teamviewer.sh
```

스크립트가 하는 일: **Xvfb(:99) + XFCE** 설치·실행, **systemd 서비스** 등록(부팅 시 자동), **TeamViewer를 XFCE autostart**에 넣어서 가상 세션에서 실행.  
완료 후 30초 정도 기다렸다가 TeamViewer로 다시 접속해 보세요. 여전히 검으면 `sudo systemctl restart xfce-xvfb@$(whoami)` 후 재접속.

---

## 사전 요구사항

- **dgx-spark** SSH 접속 가능 (예: `ssh dgx-spark`)
- **sudo** 권한이 있는 **비-root 사용자**로 로그인
- **Google 계정** (원격 접속 권한 연결용)
- 서버 **아키텍처: amd64** (ARM64에서는 CRD 불가 → 위 대안 사용)
- 서버 OS: Ubuntu 20.04/22.04 또는 Debian 계열 (DGX는 보통 Ubuntu 기반)

---

## Step 1: 패키지 설치 (서버에서 실행)

dgx-spark에 SSH 접속한 뒤, 아래 중 한 가지 방법으로 진행합니다.

### 방법 A: 자동 스크립트 사용

1. 이 레포에서 스크립트를 서버로 복사합니다.

   ```bash
   scp docs/classes/1-오리엔테이션/agentic_ai_onboarding/scripts/install_chrome_remote_desktop_dgx.sh dgx-spark:~/
   ```

2. 서버에서 실행 (sudo 비밀번호 입력 필요).

   ```bash
   ssh dgx-spark
   chmod +x install_chrome_remote_desktop_dgx.sh
   ./install_chrome_remote_desktop_dgx.sh
   ```

### 방법 B: 수동 명령어

SSH로 dgx-spark 접속 후 순서대로 실행합니다.

```bash
# 1) Chrome Remote Desktop 설치
sudo apt update
sudo apt-get install -y wget
sudo wget -q -O /tmp/chrome-remote-desktop.deb https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
sudo dpkg --install /tmp/chrome-remote-desktop.deb || true
sudo apt install -y --fix-broken

# 2) 경량 데스크톱 환경 (XFCE) 설치 (CRD는 X 세션 필요)
sudo DEBIAN_FRONTEND=noninteractive apt install -y xfce4 desktop-base

# 3) CRD가 XFCE 세션을 쓰도록 설정
sudo bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'

# 4) XFCE 기본 화면잠금(Light Locker)이 CRD와 충돌할 수 있으므로 XScreenSaver 사용
sudo apt install -y xscreensaver

# 5) 현재 사용자를 chrome-remote-desktop 그룹에 추가 (로그아웃 후 재로그인 시 적용)
sudo usermod -a -G chrome-remote-desktop $USER
```

**그룹 적용**: `usermod` 후에는 **한 번 로그아웃했다가 다시 SSH로 접속**하거나, `newgrp chrome-remote-desktop` 후 Step 2를 진행합니다.

---

## Step 2: Google 계정으로 CRD 권한 연결 (한 번만 수행)

이 단계는 **dgx-spark 서버가 아닌, 본인 PC의 Chrome 브라우저**에서 진행합니다.

1. **로컬 PC**에서 Chrome으로 **[https://remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)** 접속
2. **Google 계정으로 로그인**
3. 화면 안내에 따라 **Linux → Debian**용 **명령어**를 확인합니다.  
   형태는 대략 다음과 같습니다:

   ```text
   DISPLAY= /opt/google/chrome-remote-desktop/start-host \
     --code="4/xxxxxxxxxxxxxxxxxxxxxxxx" \
     --redirect-url="https://remotedesktop.google.com/_/oauthredirect" \
     --name=$(hostname)
   ```

4. 위 **명령어 전체를 복사**한 뒤, **dgx-spark SSH 터미널**에 붙여넣어 실행합니다.
5. 안내가 나오면:
   - **PIN**: 6자리 이상 숫자 입력 (이후 원격 접속 시 사용)
   - **컴퓨터 이름**: 원하는 이름 입력 또는 Enter로 기본값(`hostname`) 사용
6. `Host ready to receive connections.` 메시지가 나오면 설정 완료입니다.

> **주의**: `--code=` 값은 **몇 분 안에 한 번만** 사용 가능하므로, 명령어를 받은 뒤 빠르게 서버에서 실행하세요.

---

## Step 3: 원격 접속하기

1. **로컬 PC**에서 Chrome으로 **[https://remotedesktop.google.com/access](https://remotedesktop.google.com/access)** 접속 (또는 Chrome Remote Desktop 앱 사용)
2. 같은 Google 계정으로 로그인
3. 목록에 **dgx-spark(또는 Step 2에서 지정한 이름)** 가 보이면 선택
4. Step 2에서 설정한 **PIN** 입력 후 접속

이후에는 서버를 재부팅해도 CRD 서비스가 자동으로 올라오며, 브라우저에서 계속 접속할 수 있습니다.

---

## 서비스 제어 (참고)

- 재시작: `sudo /etc/init.d/chrome-remote-desktop restart`
- 중지: `sudo /etc/init.d/chrome-remote-desktop stop`
- 상태: `sudo /etc/init.d/chrome-remote-desktop status`

접속 권한(기기 연결 해제)은 [remotedesktop.google.com/access](https://remotedesktop.google.com/access)에서 해당 PC 옆 삭제(휴지통) 아이콘으로 해제할 수 있습니다.

---

## 트러블슈팅

| 현상 | 확인/조치 |
|------|-----------|
| `start-host` 실행 시 권한 오류 | `sudo usermod -a -G chrome-remote-desktop $USER` 후 **재로그인** 또는 `newgrp chrome-remote-desktop` |
| 화면이 검은색/잠금 | XScreenSaver 등 화면보호기 잠금 해제; 필요 시 XFCE 설정에서 화면 잠금 비활성화 |
| 목록에 PC가 안 보임 | Step 2의 명령을 **같은 Google 계정**으로 실행했는지, 그리고 `Host ready to receive connections.`까지 나왔는지 확인 |
| 네트워크/방화벽 | CRD는 Google 서버 경유이므로, 서버에서 인터넷(HTTPS)만 나가면 됨. 사내 방화벽에서 outbound 443 차단 여부 확인 |

---

## 요약

1. **서버(dgx-spark)**: CRD + XFCE 설치 → `chrome-remote-desktop` 그룹 추가 → 재로그인  
2. **로컬 PC**: [remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)에서 명령어 복사 → 서버 터미널에 붙여넣어 실행 → PIN·이름 설정  
3. **접속**: [remotedesktop.google.com/access](https://remotedesktop.google.com/access)에서 해당 PC 선택 후 PIN 입력

이렇게 하면 dgx-spark에 Chrome Remote Desktop이 설치·설정되어, 어디서든 Chrome으로 GUI 원격 접속할 수 있습니다.
