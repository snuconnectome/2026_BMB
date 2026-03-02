# 2026 Brain-Mind-Behavior (BMB) 코스 가이드라인 🧠

환영합니다! 이 저장소는 2026년 서울대학교 "뇌-마음-행동 (Brain, Mind, and Behavior)" 코스의 에이전트 기반 인공지능(AI) 코스 시스템을 포함하고 있습니다.
처음 오셨더라도 걱정하지 마세요. 이 문서를 차근차근 따라가시면 쉽게 시스템에 온보딩하실 수 있습니다.

## 🌟 프로젝트 소개

본 코스는 전통적인 일방향 강의에서 벗어나, 학생과 AI 에이전트가 함께 문제를 해결하며 학습하는 "체험형/에이전틱(Agentic)" 학습을 지향합니다.
이를 위해 여러 가지 AI 툴과 시스템이 구축되어 있습니다.

## ⚙️ 주요 툴킷 및 기능 요약

이 저장소에는 코스 운영과 과제 진행을 돕는 여러 AI 에이전트가 준비되어 있습니다.

- **콘텐츠 생성기 (Content Generator)**: 매주 주간 챌린지 및 학습 자료의 초안을 생성합니다.
- **eTL 평가기 (eTL Evaluator)**: 학생들이 eTL에 올린 기여도를 분석하고 프롬프트 오딧(Prompt Audit)을 도와줍니다.
- **벡터 데이터베이스 (Vector DB)**: RAG(Retrieval-Augmented Generation) 시스템을 위해 코스 관련 문서와 지식을 임베딩하고 검색 가능한 형태로 관리합니다.
- **AI-CoScientist (동료 연구자 AI)**: 학생들의 아이디어를 발전시키기 위해 시뮬레이션 기반 피드백을 제공합니다.

---

## 📚 쉽게 따라하는 NotebookLM 연동 방법 (필수!)

본 코스는 구글의 **NotebookLM**을 지식 베이스로 활용합니다.
로컬 환경의 에이전트들이 NotebookLM에 저장된 강의 노트와 논문들을 읽고 대답할 수 있도록 MCP(Model Context Protocol) 기반으로 연동해야 합니다.

### 1단계: 필수 프로그램 설치

시스템을 원활하게 사용하기 위해서는 아래의 요구사항이 설치되어 있어야 합니다.

- **Python 3.10 이상**: Python이 없다면 [공식 홈페이지](https://www.python.org/)에서 설치해주세요.
- **Git**: 저장소를 클론(Clone)하기 위해 필요합니다.

### 2단계: NotebookLM CLI 툴 설치

터미널(또는 명령 프롬프트)을 열고, 다음 명령어를 입력하여 NotebookLM 연동 툴을 설치합니다.

```bash
pip install notebooklm-mcp-cli
```

*주의: 파이썬 버전 충돌이 발생할 경우, 가상 환경(Virtual/Conda Environment)을 생성한 후 설치하시는 것을 권장합니다.*

### 3단계: 인증 및 설정

NotebookLM에 접근하려면 인증이 필요합니다. 터미널에 다음을 입력하여 로그인합니다.

```bash
notebooklm-mcp-cli login
```

브라우저 창이 열리면 구글 계정으로 로그인해주세요. 그 후 사용할 특정 Notebook의 ID를 환경 변수로 연결하여 에이전트들이 해당 노트의 정보를 참고하도록 설정하면 준비 완료입니다!

---

## 🚀 코스 코드베이스 시작하기

개발 환경을 로컬에 맞추기 위한 첫 걸음입니다.

**1. 저장소 클론 및 이동**

```bash
git clone https://github.com/[사용자명]/2026_BMB.git
cd 2026_BMB
```

**2. 필요 패키지 설치**

```bash
pip install -r requirements.txt
```

**3. 스크립트 실행 예시**
각종 스크립트들은 `scripts/` 와 `agents/` 폴더 내에 위치해 있습니다. 예를 들어, 데이터베이스를 새로 빌드하려면 아래와 같이 실행합니다.

```bash
python scripts/build_vector_db.py
```

## 🚀 2026 Vector DB SOTA 업그레이드 To-Do

현재 로컬 프로토타입 상태인 Vector DB 파이프라인을 2026년 기준 최고의 성능을 위해 NVIDIA DGX-Spark 환경으로 마이그레이션하고 고도화하는 작업 목록입니다. 상세한 계획은 [docs/VectorDB_Improvement_Plan.md](docs/VectorDB_Improvement_Plan.md)를 참조하세요.

- [ ] 구조화된 데이터(엑셀표) 및 마크다운 논리적 청킹 로직 구현 (Semantic Chunking)
- [ ] 고해상도 임베딩 모델(예: OpenAI, Upstage, 또는 DGX GPU 활용 OSS)로 교체
- [ ] Qdrant 등 하이브리드 검색 지원 Vector DB 인프라 구축
- [ ] DGX-Spark의 멀티 GPU와 다중 워커(Multi-processing)를 활용한 초고속 파이프라인 구현

---

## ❓ 자주 묻는 질문 (FAQ)

- **Q. Agentic AI란 무엇인가요?**
  A. 단순히 질문에 답만 해주는 챗봇이 아니라, 스스로 계획을 세우고 도구를 사용하며 목표를 이뤄나가는 주도적인 AI입니다.

- **Q. 코딩을 전혀 모르면 수업을 못 듣나요?**
  A. 아닙니다! 본 가이드라인에서 제공하는 명령어들만 그대로 복사/붙여넣기 하시면 작동되도록 구성되어 있습니다. 코딩보다는 "좋은 질문(프롬프트)을 던지는 능력"이 훨씬 중요합니다.

어려운 점이 있으시면 언제든지 이슈(Issue)를 남겨주시거나 조교진에게 문의해주세요. 즐거운 탐구의 시간이 되시길 바랍니다! 🎉
