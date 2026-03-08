# Cursor + 수업용 DeepSeek 설정

수업용 API(LiteLLM)를 Cursor에서 쓰려면 아래 순서대로 하면 됩니다.

---

## 0. Gmail 계정 제출 (NotebookLM 셋업용 — 수업 전 필수)

수업 후반부(Phase 3)에서 Google **NotebookLM**을 사용하여 팟캐스트를 제작합니다. NotebookLM은 **Google 계정(Gmail)**으로만 로그인할 수 있으므로, 아래 폼을 통해 본인의 Gmail 주소를 사전에 제출해 주세요.

> **📋 제출 폼:** [Gmail 수집용 Google Form](https://docs.google.com/forms/d/e/1FAIpQLSdkMMgJm5QJOwsCm9bCUpBnXrTMbfyBWQsDWfnn2bPcXY12Ww/viewform?usp=publish-editor)

- 학교 이메일(`@snu.ac.kr`)이 아닌 **개인 Gmail 주소**를 제출하세요.
- Gmail이 없으면 [accounts.google.com](https://accounts.google.com)에서 무료로 생성할 수 있습니다.
- 수업 당일 NotebookLM에 바로 로그인할 수 있도록, 제출한 Gmail 계정의 비밀번호를 기억해 두세요.

---

## 1. Cursor 설치 (이미 있으면 생략)

1. [cursor.com](https://www.cursor.com) 접속 → 본인 OS용 **다운로드**
2. 설치 후 실행 → **이메일 또는 GitHub**로 무료 계정 생성·로그인

---

## 2. Custom model 선택 후 값 입력

1. **Settings** (⌘+, / Ctrl+,) 열기 → **Models** 또는 **Features** → **API Keys** / **OpenAI** 로 이동
2. 모델 옵션에서 **Custom model** (또는 **OpenAI-compatible** / **Use custom API**) 을 선택
3. 아래 값을 입력합니다.

| 항목 | 입력 |
|------|------|
| **OpenAI API Key** | ON 으로 두고, 조교가 준 **개인 API 키** (`sk-...`) 붙여넣기 |
| **Override OpenAI Base URL** | ON 으로 두고, `https://cadgily-unobstinate-breana.ngrok-free.dev/v1` |
| **Model** | `deepseek/deepseek-v3.2` 또는 `deepseek/deepseek-r1-distill-qwen-32b` |

1. **Save** / **Verify** 후 설정 창 닫기.

---

## 3. 확인

Cursor 채팅에서 짧은 메시지(예: "안녕") 보내서 응답이 오면 성공입니다.

- **401** → API 키 확인 (오타·공백 없이)
- **연결 실패** → Base URL 끝에 `/v1` 있는지, 조교에게 ngrok 켜져 있는지 문의

---

## (조교용) 학생별 API 키 표

아래 표에서 **본인 이름**에 해당하는 **key** 값을 Cursor 설정의 **OpenAI API Key** 란에 넣으면 됩니다.  
조교는 이 문서를 배포할 때, 필요 시 학생별로 본인 행만 안내해도 됩니다.

| 이름 | key |
|------|-----|
| 강찬우 | sk-JzNNJmCOvEdtWBnHkjwmnw |
| 고수민 | sk-FzmBe9VkL_VC8N-lXiSvvg |
| 곽수현 | sk-DqBg8amaxv60otzxzc4SWA |
| 김도현 | sk-tDcdkEP91_W7t6nZqHYFZw |
| 김연아 | sk-GU2h6SkSRbnKtbbbRWuwuQ |
| 김혜인 | sk-KKLZYPdKGGn9-A4Jlwdznw |
| 민형준 | sk-172lzDHCOCawzH90sGP8-Q |
| 박서영 | sk-arwiK21qB3KjhmDfsXPE5g |
| 박윤수 | sk-NjnkAaMheLbabKXc8fXXQg |
| 박주혜 | sk-FPmY_cbQBDTi7OJYiLKANg |
| 박지오 | sk-K1HtHw0akPsZNnqgUHZyYQ |
| 봉채윤 | sk-SmylihmiYkxNPOo_GSTT4g |
| 서예원 | sk-A_abWzv3zLLjJPUBnuvjmQ |
| 서지현 | sk-706SojgUPcb56z_U2f96Eg |
| 송지호 | sk-a9AB-jCbfYk7UmtSCN-7gQ |
| 신혜원 | sk-Rvw1Ed4kMUDPAeZhomlqCg |
| 심규섭 | sk-9ndPnb8hWRsOgO2nI_-vOQ |
| 안제섭 | sk-vfLOi1vr-AtP9SmvxKWcpw |
| 엄지윤 | sk-t4A_WeJphQIfZp6L0OyYGA |
| 오종건 | sk-8qv4CDEofzmzxa86E99kOQ |
| 유예림 | sk-vt6tnUnlTMoAKBFGEFu4TA |
| 이규민 | sk-mDAG4OaRB4ej2yN8VUNO1g |
| 이나영 | sk-ekqwgQ002kNZ8pPrnSPFGg |
| 이다희 | sk-1X7Z5GUUOiYck_MV1HM3dg |
| 이서연 | sk-3jX4td6RpWebMd_4YXwb7g |
| 이승현 | sk-yxsATuYJgenmsRd5r0dnhw |
| 임준원 | sk-n0FZ_RcNmfrCsbdSPW2wJw |
| 정유현 | sk-Z15qd4ZsEyH4rSUrDfqljA |
| 조성우 | sk-HPAlxjoqQnSvjG--UqFXOA |
| 차지욱 | sk-gK_85yaGzmodUWWGbkhulw |
| 한강희 | sk-7sqg8rM3KOkhLgcW8N9Wog |
| 황현기 | sk-e2Y0ds8GpkW_-11Y4QGd0w |
| (예비 1) | sk-Epsb0XPmobuZjad9nDyHoQ |
| (예비 2) | sk-sLl2ryvm5IXniBbkS6ylzA |
| (예비 3) | sk-qLR-w8mBblli3wgAv4P0NQ |
