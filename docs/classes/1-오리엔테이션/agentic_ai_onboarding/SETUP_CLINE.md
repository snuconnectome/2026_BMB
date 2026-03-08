# 2026 뇌마음행동: Cline(Agentic AI) 설치 및 설정 가이드 (요약본)

**뇌마음행동 과정 | 서울대학교 커넥톰연구실 (차지욱 교수)**  
**학습 목표**: AI 자체를 배우는 것이 아닌, 질문을 발굴하고 탐구하기 위한 **"Enabling Technology"**로서 Agentic AI(Cline) 설정하기.

> **처음 설치·사용하시나요?** 연결 테스트, Allow 승인, 첫 실습까지 한 번에 따라 하려면 **[Cline 스텝바이스텝 튜토리얼](CLINE_STEP_BY_STEP_TUTORIAL.md)**을 먼저 진행하세요. 이 문서는 설치·설정만 빠르게 참고할 때 쓰는 요약본입니다.

---

## 1. Cursor 설치

AI 코딩 및 에이전트 실행을 위한 텍스트 에디터인 Cursor를 설치합니다.

1. [https://www.cursor.com](https://www.cursor.com) 접속
2. 본인 OS에 맞는 버전 다운로드 (macOS / Windows) 후 설치
3. 초기 설정 완료 후 실행

## 2. Tailscale 설치

로컬 PC에서 연구실의 GPU 서버 리소스 및 API 게이트웨이(`dgx-spark`)에 안전하게 접속하기 위한 VPN 설정입니다.

1. [https://tailscale.com/download](https://tailscale.com/download) 접속 후 설치
2. 앱 실행 후 조교가 안내한 강의용 계정으로 로그인

## 3. Cline 확장(Extension) 설치

Cursor 내에서 실질적인 자율 에이전트 역할을 할 **Cline**을 설치합니다.

1. Cursor 좌측 사이드바에서 Extensions (확장) 아이콘 클릭
2. 검색창에 **`Cline`** 입력 (by saoudrizwan)
3. Install 클릭
4. 설치 완료 시 사이드바에 산 모양의 Cline 아이콘이 생깁니다.

## 4. API 서버 연결 설정 (LiteLLM)

수업에서 제공하는 고성능 모델(DeepSeek, Gemini 등)을 사용하기 위한 연결 설정입니다.

1. Cline 아이콘 클릭 후 상단의 톱니바퀴(설정) 아이콘 클릭
2. **API Provider**: `OpenAI Compatible` 선택
3. **Base URL**: `http://100.x.x.x:4000/v1` (조교 안내 참고)
4. **API Key**: 개인별로 부여받은 실습용 `sk-xxxxx` 키 입력
5. **Model ID**: `deepseek/deepseek-r1-distill-qwen-32b` (권장, 빠름) 또는 `deepseek/deepseek-v3.2`, `gemini/gemini-2.5-pro` 입력
6. **Save** 클릭

> **연결 테스트**: 채팅창에 `Hello, 연결 확인 부탁해` 라고 입력하여 응답이 오면 성공입니다!

## 주의사항

- **에이전트 승인**: Cline이 파일 시스템 접근(파일 쓰기/읽기) 또는 터미널 명령을 수행하려고 할 때 팝업이 뜹니다. 어떤 작업을 하려는지 인지한 후 **Allow**를 눌러 승인하세요.
- **데이터 보안**: 민감한 실제 환자 데이터나 개인정보를 프롬프트에 입력하지 마세요. 공개된 교재 내용이나 퍼블릭 데이터를 활용하세요.
- **맹신 금지**: AI를 활용해 도출한 요약, 파이프라인, 코드는 반드시 본인이 결과를 검증해야 합니다. 이 수업의 목표는 올바른 '질문'을 던지고, AI가 제대로 답했는지 '비판적으로 감사(Audit)'하는 역량을 기르는 것입니다.
