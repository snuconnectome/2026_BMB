# 2026 뇌마음행동: Cline(Agentic AI) 스텝바이스텝 튜토리얼

**뇌마음행동 과정 | 서울대학교 커넥톰연구실 (차지욱 교수)**

**학습 목표**: 질문을 발굴하고 탐구하기 위한 **"Enabling Technology"**로서 Cline을 설치하고, 설정한 뒤 첫 실습(논문 검색·요약 파이프라인)까지 한 흐름으로 완료하기.

---

## Step 1: Cursor 설치 및 로그인

AI 코딩 및 에이전트 실행을 위한 에디터인 **Cursor**를 설치합니다.

1. [https://www.cursor.com](https://www.cursor.com) 접속
2. 본인 OS에 맞는 버전 다운로드 (macOS / Windows) 후 설치
3. 설치 후 실행하면 **계정 생성/로그인** 안내가 나옵니다. 이메일 또는 GitHub로 가입·로그인하여 Cursor 사용을 활성화합니다.
4. 초기 설정(테마, 키 바인딩 등)은 기본값으로 두고 넘어가도 됩니다.

---

## Step 2: Tailscale 가입 및 연결 (초대 링크 사용)

로컬 PC에서 수업용 API 서버(`dgx-spark`)에 안전하게 접속하기 위한 VPN입니다. **API를 사용하려면 Tailscale 연결이 선행되어야 합니다.** 조교가 eTL 또는 공지로 배포한 **초대 링크 한 번**으로 가입하면 됩니다.

### 2-1. 초대 링크로 가입하기

1. **조교가 안내한 Tailscale 초대 링크**를 클릭합니다.  
   - 2026 BMB 수업용 초대 링크: <https://login.tailscale.com/admin/invite/7bQW8eSYp4dqBkr6Mdq121>  
   (eTL 등에서 별도 링크를 배포한 경우 해당 링크를 사용하세요.)
2. 브라우저에서 Tailscale 로그인 페이지가 열리면, **Sign in with Google** / **Microsoft** / **GitHub** / **Apple** 중 하나를 선택하거나, 이메일로 가입합니다. **처음 사용하는 경우** 같은 화면에서 계정을 만들면 됩니다.
3. 로그인(또는 가입)이 끝나면 **수업용 tailnet에 자동으로 참가**한 상태가 됩니다. 화면 안내가 나오면 "Join" 또는 "Accept"를 눌러 참가를 완료합니다.

### 2-2. Tailscale 앱 설치 및 로그인

4. 본인 PC에 Tailscale 앱이 없다면 [https://tailscale.com/download](https://tailscale.com/download) 에서 **본인 OS(macOS/Windows)** 에 맞는 앱을 다운로드 후 설치합니다.
5. 설치한 **Tailscale 앱**을 실행하고, **2-1에서 사용한 것과 같은 계정**(Google/이메일 등)으로 로그인합니다.
6. 앱에서 연결 상태가 **녹색(Connected)** 인지 확인합니다. 이 상태여야 Cline에서 수업용 API(Base URL)에 접속할 수 있습니다.

> **요약**: 초대 링크 클릭 → 브라우저에서 로그인(또는 가입) → tailnet 참가 → Tailscale 앱 설치·실행 후 같은 계정으로 로그인 → Connected 확인.

---

## Step 3: Cline 확장(Extension) 설치

Cursor 안에서 자율 에이전트 역할을 하는 **Cline**을 설치합니다.

1. Cursor **좌측 사이드바**에서 **Extensions(확장)** 아이콘 클릭 (네 개의 사각형 모양)
2. 검색창에 **`Cline`** 입력 → **by saoudrizwan** 항목 선택
3. **Install** 클릭
4. 설치가 끝나면 사이드바에 **산 모양 아이콘**이 생깁니다. 이 아이콘이 Cline 패널을 엽니다.

---

## Step 4: Cline API 설정 (조교에게 받을 값)

수업에서 제공하는 고성능 모델(DeepSeek, Gemini 등)을 쓰기 위한 연결 설정입니다.

1. 사이드바에서 **Cline 아이콘** 클릭 → Cline 패널이 열리면 **상단 톱니바퀴(설정)** 클릭
2. 아래 항목을 **조교 안내 또는 강의 자료**에서 받은 값으로 입력합니다.

| 항목 | 입력 예시 | 비고 |
|------|-----------|------|
| **API Provider** | `OpenAI Compatible` | 드롭다운에서 선택 |
| **Base URL** | `http://100.x.x.x:4000/v1` | 조교가 안내한 실제 IP·포트로 교체 |
| **API Key** | `sk-xxxxx` | 개인별 실습용 키 |
| **Model ID** | `deepseek/deepseek-r1-distill-qwen-32b` (권장, 빠름) 또는 `deepseek/deepseek-v3.2`, `gemini/gemini-2.5-pro` | 안내된 모델명 그대로 |

3. **Save** 클릭 후 설정 창을 닫습니다.

> **직접 OpenRouter 등을 쓰는 경우**: Base URL·API Key·Model ID를 해당 서비스 값으로 넣고, 연결 실패 시 [Step 5 트러블슈팅](#연결-테스트-실패-시-점검-목록)의 OpenRouter 항목을 참고하세요.

---

## Step 5: 연결 테스트

설정이 끝났다면 **채팅으로 연결 여부**를 확인합니다.

1. Cline 패널에서 **맨 아래 채팅 입력창**에 다음을 입력합니다.  
   `Hello, 연결 확인 부탁해`
2. **Enter** 또는 전송 버튼으로 보냅니다.
3. 몇 초 안에 AI 응답이 **채팅 영역 위쪽**에 뜨면 **연결 성공**입니다.

### 연결 테스트 실패 시 점검 목록

- **Tailscale**: 앱이 실행 중이고 상태가 **Connected**인지 확인. 끊겨 있으면 Base URL로 접속되지 않습니다.
- **Base URL / API Key**: 주소, 포트, 키를 **다시 한 번 확인**. 오타, 공백, 줄바꿈이 들어가 있지 않은지 봅니다.
- **OpenRouter 사용 시 404 에러**: "No endpoints found matching your data policy (Paid model training)" 이 나오면 [OpenRouter Privacy 설정](https://openrouter.ai/settings/privacy)에서 **"Enable paid endpoints that may train on inputs"** 를 켜야 해당 모델을 쓸 수 있습니다.
- **방화벽/회사 네트워크**: 특정 환경에서는 VPN 또는 API 주소가 차단될 수 있습니다. 다른 네트워크에서 한 번 시도해 보세요.

---

## Step 6: 첫 에이전트 액션 — Allow(승인) 경험하기

Cline은 **파일 생성·수정, 터미널 명령** 등을 할 수 있습니다. 처음 그런 동작을 하면 **승인 팝업**이 뜹니다.

1. Cline 채팅창에 아래처럼 입력해 봅니다.  
   `현재 열려 있는 프로젝트 루트에 test_hello.txt 파일을 만들고 "Cline 연결 성공" 이라고 한 줄 써줘.`
2. Cline이 파일 쓰기나 터미널 명령을 시도하면 **Allow / Deny** 버튼이 있는 **팝업**이 뜹니다.
3. **어떤 작업을 하려는지** 내용을 읽은 뒤, 진행하려면 **Allow**를 눌러 승인합니다.
4. 승인 후 Cline이 파일을 만들고, 채팅으로 결과를 알려줍니다.  
   → 이 경험으로 "에이전트가 내 PC에서 실제로 행동한다"는 것을 확인할 수 있습니다.

> **주의**: 민감한 데이터가 있는 폴더를 열어둔 상태에서는, Cline이 제안하는 명령/파일 경로를 꼼꼼히 확인한 뒤 허용하세요.

---

## Step 7: 실습 파이프라인 — 논문 검색·요약 자동화

ChatGPT와 달리, Cline은 **로컬에 폴더를 만들고, 논문을 검색·다운로드·요약해 저장**할 수 있습니다. 아래 프롬프트를 **본인 주제로 바꿔서** 실행해 보세요.

1. Cline 채팅창에 아래 블록을 **복사한 뒤**, `"..."` 부분만 본인의 관심 주제로 수정합니다.
2. 붙여넣기 후 **Enter**로 전송합니다.
3. Cline이 단계별로 진행하면서 **폴더 생성, 검색, 파일 저장** 등을 제안할 때마다 **Allow**로 승인합니다.

```text
나는 뇌마음행동 수업을 듣는 학생이야.
"명상이 Default Mode Network에 미치는 영향"에 대한 최신 연구가 궁금해.
다음 작업을 자동화해줘:
1. 프로젝트 루트에 'my_bmb_research' 폴더를 만들어.
2. 2024~2026년 출판된 관련 논문 10편을 검색해. (PubMed 또는 arXiv)
3. 논문 PDF 또는 초록 텍스트를 다운로드해서 'papers' 하위 폴더에 저장해.
4. 논문의 제목, 저자, 핵심 결론을 'metadata.csv'로 정리해.
5. 10편의 연구를 종합하여 내가 가진 질문에 대한 1페이지 분량의 마크다운 요약 보고서('summary_report.md')를 작성해.
```

4. 완료 후 `my_bmb_research/summary_report.md` 등을 열어 결과를 확인하고, **후속 질문**을 Cline에게 던져 보세요.  
   예: *"요약 보고서를 보니 A와 B 개념이 상충해. A를 지지하는 fMRI 분석 파이프라인을 Nilearn으로 짜줄 수 있어?"*

---

## 주의사항

- **에이전트 승인**: 파일 접근·터미널 명령 시 나오는 **Allow**를 무조건 누르기보다, **무슨 작업인지 확인한 뒤** 허용하세요.
- **데이터 보안**: 실제 환자 데이터·개인정보는 프롬프트에 넣지 마세요. 공개된 교재·퍼블릭 데이터만 활용하세요.
- **맹신 금지**: AI가 만든 요약·코드·파이프라인은 **본인이 반드시 검증**해야 합니다. 이 수업의 목표는 올바른 '질문'을 던지고, AI 출력을 **비판적으로 감사(Audit)**하는 역량을 기르는 것입니다.

---

## 다음 단계

- **상세 실습 예시·후속 질문**: [CLINE_PRACTICE_GUIDE.md](CLINE_PRACTICE_GUIDE.md) 참고.
- **설치만 빠르게 참고**: [SETUP_CLINE.md](SETUP_CLINE.md) (요약본).
