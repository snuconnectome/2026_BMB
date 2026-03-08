# 2026 뇌마음행동: Cursor + Tailscale + LiteLLM 설정 가이드 (Cline 없이)

**뇌마음행동 과정 | 서울대학교 커넥톰연구실 (차지욱 교수)**

**학습 목표**: Cline 확장 없이 **Cursor(무료)** 와 수업용 **Tailnet + LiteLLM** 만으로 AI 채팅·코드 보조를 사용할 수 있도록 설정하기.

---

## 이 가이드가 필요한 경우

- Cline 확장 없이 **Cursor 기본 기능**만으로 수업용 API를 쓰고 싶을 때
- Tailscale(tailnet)으로 접속하는 **LiteLLM 프록시**(수업 서버)를 Cursor에 연결할 때

수업에서 제공하는 **동일한 API 서버**(dgx-spark:4000, LiteLLM)를 쓰며, **Cursor 내장 채팅/작성**에서 바로 사용합니다.

---

## Step 1: Cursor 설치 및 (무료) 가입

1. [https://www.cursor.com](https://www.cursor.com) 접속
2. 본인 OS에 맞는 버전 다운로드 (macOS / Windows) 후 설치
3. 실행 후 **이메일 또는 GitHub로 무료 계정** 생성·로그인 (Pro 구독 불필요)
4. 초기 설정은 기본값으로 두고 넘어가도 됩니다.

---

## Step 2: Tailscale 가입 및 연결 (초대 링크 사용)

수업용 LiteLLM 서버는 **Tailscale tailnet 안**에 있으므로, 먼저 tailnet에 참가해야 합니다.

### 2-1. 초대 링크로 가입하기

1. **조교가 안내한 Tailscale 초대 링크**를 클릭합니다.  
   - 2026 BMB 수업용 초대 링크: <https://login.tailscale.com/admin/invite/7bQW8eSYp4dqBkr6Mdq121>  
   (eTL 등에서 별도 링크를 배포한 경우 해당 링크를 사용하세요.)
2. 브라우저에서 **Sign in with Google** / **Microsoft** / **GitHub** / **Apple** 또는 이메일로 가입·로그인합니다.
3. 화면 안내에 따라 **Join** / **Accept**로 수업용 tailnet 참가를 완료합니다.

### 2-2. Tailscale 앱 설치 및 로그인

4. [https://tailscale.com/download](https://tailscale.com/download) 에서 본인 OS용 앱을 다운로드 후 설치합니다.
5. **Tailscale 앱**을 실행하고, 2-1에서 사용한 **같은 계정**으로 로그인합니다.
6. 연결 상태가 **녹색(Connected)** 인지 확인합니다. 이 상태여야 Cursor에서 수업용 API에 접속할 수 있습니다.

---

## Step 3: Cursor에서 수업용 API(LiteLLM) 연결

Cursor **기본 설정**에서 수업용 LiteLLM 서버를 OpenAI 호환 API로 등록합니다.

1. Cursor에서 **Settings**(⌘+, / Ctrl+,)를 엽니다.
2. **Models** 또는 **Features** → **API Keys** / **OpenAI** 관련 메뉴로 이동합니다.
3. **Use custom API** / **OpenAI-compatible API** / **Override OpenAI base URL** 같은 옵션을 켭니다.
4. 아래 값을 **조교 안내**에 맞게 입력합니다.

| 항목 | 입력 값 | 비고 |
|------|----------|------|
| **Base URL** | `http://100.92.111.86:4000/v1` | 조교가 안내한 tailnet IP가 다르면 해당 주소로 변경 (예: `http://100.x.x.x:4000/v1`) |
| **API Key** | `sk-xxxxx` | 개인별로 부여받은 수업용 API 키 |
| **Model** (또는 Model ID) | `deepseek/deepseek-r1-distill-qwen-32b` (권장) 또는 `deepseek/deepseek-v3.2`, `deepseek/deepseek-r1` | LiteLLM에서 지원하는 모델명 그대로 |

5. **Save** 또는 **Verify** 후 설정을 닫습니다.

> **참고**: Cursor 버전에 따라 메뉴 이름이 **Cursor Settings → Models**, **Features → OpenAI**, **Custom API** 등으로 다를 수 있습니다. "OpenAI", "Custom", "Base URL" 관련 항목을 찾아 동일하게 넣으면 됩니다.

---

## Step 4: 연결 테스트

1. Cursor에서 **채팅** 또는 **Composer** 패널을 엽니다.
2. "Hello, 연결 확인 부탁해" 처럼 짧은 메시지를 입력해 전송합니다.
3. 몇 초 안에 AI 응답이 오면 **연결 성공**입니다.

### 연결이 안 될 때

- **Tailscale**: 앱이 실행 중이고 **Connected** 인지 확인합니다. 끊겨 있으면 Base URL로 접속되지 않습니다.
- **Base URL**: `http://` 로 시작하고, **포트 4000**, 경로 **/v1** 이 포함되어 있는지 확인합니다. (예: `http://100.92.111.86:4000/v1`)
- **API Key**: 조교가 준 키를 그대로 붙여넣고, 앞뒤 공백·줄바꿈이 없는지 확인합니다.
- **방화벽/회사 네트워크**: 일부 환경에서는 Tailscale 또는 해당 포트가 막혀 있을 수 있습니다.

---

## 사용 가능한 모델 (LiteLLM 기준)

수업 서버(LiteLLM)에서 사용할 수 있는 모델 예시는 아래와 같습니다. Cursor **Model** 선택에서 동일한 이름을 사용하면 됩니다.

| 모델 ID | 비고 |
|---------|------|
| `deepseek/deepseek-r1-distill-qwen-32b` | 권장, 응답이 빠름 |
| `deepseek/deepseek-v3.2` | 고품질 |
| `deepseek/deepseek-r1` | R1 (429 시 v3.2로 자동 전환) |
| `google/gemini-2.5-flash`, `google/gemini-2.5-pro` | 조교 안내 시 사용 |

---

## 주의사항

- **API 키**는 개인별로 발급된 것이므로 다른 사람과 공유하지 마세요.
- **민감한 개인정보**(피험자 정보, 연락처 등)는 Cursor 채팅에 입력하지 마세요.
- AI가 생성한 코드·요약은 **반드시 본인이 검증**해야 합니다. 수업 목표는 올바른 질문을 던지고, AI 출력을 비판적으로 검토하는 역량을 기르는 것입니다.

---

## 다음 단계

- **Cline도 함께 쓰고 싶을 때**: [Cline 스텝바이스텝 튜토리얼](CLINE_STEP_BY_STEP_TUTORIAL.md)에서 Cline 확장 설치 후, 동일한 Base URL·API Key·Model로 Cline만 추가 설정하면 됩니다.
- **설치만 빠르게 참고**: [SETUP_CLINE.md](SETUP_CLINE.md) 의 API 서버 연결 부분(Base URL, API Key, Model ID)만 따라 해도 동일한 수업용 API를 쓸 수 있습니다.
