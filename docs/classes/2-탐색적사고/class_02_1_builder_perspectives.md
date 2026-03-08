# 2주차 도입부: 4인의 빌더가 말하는 에이전틱 AI 리터러시

**용도:** 2주차 실습 도입부 슬라이드 (~15분, 5장)
**톤:** 교수가 3인칭으로 전문가를 소개하는 형식. 실제 발언 기반, 출처 명시.

---

## 슬라이드 1: 도입 — "코딩이 아니라 질문이다" (~2분)

### 오늘의 네 사람

| 이름 | 소속 |
|------|------|
| **Andrej Karpathy** | 전 Tesla AI 디렉터, OpenAI 창립 멤버 |
| **Jensen Huang** | NVIDIA CEO |
| **Sam Altman** | OpenAI CEO |
| **Elon Musk** | Tesla·SpaceX·xAI·Neuralink CEO |

> 이 네 사람은 교육자가 아니라 **기술 사업가**입니다. 그들의 발언에는 자사 기술에 대한 낙관이 깔려 있습니다. 오늘은 그 낙관 속에서 **우리 수업의 철학과 겹치는 지점**만 골라 듣겠습니다 — 비판적으로.

### 프레임

> AI를 **만드는** 사람들이 공통적으로 하는 말이 있습니다.
> "코딩을 배워라"가 아니라, **"질문하는 법을 바꿔라"**입니다.

### 1주차 복습 연결

지난 시간 부자키의 핵심 명제를 기억하세요:

- 뇌는 세상을 기록하기 위해서가 아니라 **행동하기 위해** 진화했습니다 (Action Machine).
- 학습은 예측 오류(Prediction Error)가 발생할 때만 일어납니다.

오늘 이 네 사람은 **같은 원리를 기술의 언어로** 말합니다.

---

## 슬라이드 2: Karpathy — "가장 뜨거운 프로그래밍 언어는 영어다" (~4분)

### 핵심 인용

> "The hottest new programming language is English."
>
> — Karpathy (2023.1.24), X/Twitter

### LLM의 본질

카파시는 여러 강연에서 LLM의 한계를 반복적으로 강조합니다. AI 커뮤니티에서 널리 쓰이는 비유를 빌리면, LLM은 **"맥락이 부족한 똑똑한 인턴"**과 같습니다.

- 인턴에게 "알아서 해"라고 하면 결과물이 엉망입니다.
- 좋은 결과물 = 좋은 지시 = **좋은 질문**.

### 프롬프트 엔지니어링의 핵심 원칙

카파시는 "State of GPT" 강연(2023.5, Microsoft Build)과 이후 강연들에서 효과적인 프롬프팅의 구성 요소를 설명합니다. 이를 정리하면 네 가지 원칙으로 요약됩니다:

| 원칙 | 핵심 | 예시 |
|------|------|------|
| **1. 페르소나 부여** | "You are a leading expert on this topic" — AI의 출력 분포를 조건화 | "너는 노벨상 수상 신경과학자이자 철저한 문헌 고증주의자야" |
| **2. 맥락의 극대화** | 대상 독자, 목적, 출력 형태를 명시적으로 제한 | "학부 1학년 대상, 마크다운 형식, 인용구 포함" |
| **3. 사고의 연쇄 (Chain of Thought)** | "Models need tokens to think" — 추론 과정을 텍스트로 풀어내도록 지시 | "바로 대답하지 말고 단계별로 설명 논리를 먼저 기획해 봐" |
| **4. 구조적 표현 (Show, Don't Tell)** | 원하는 결과물의 템플릿을 함께 제공 | 출력 형식을 하단에 예시로 제시 |

> *(이 4원칙의 상세 설명과 실습 예시는 실습 가이드 `class_02_agentic_workflows_claude.md`를 참조하세요.)*

### Inside-Out 연결

페르소나를 부여하고 맥락을 제공하는 행위는 **Good-enough Brain이 가설을 생성하는 과정을 비유적으로 반영**합니다.

- 여러분이 AI에게 역할과 맥락을 설정하는 순간, **"답은 아마 이런 방향일 것이다"**라는 기대를 이미 형성하고 있는 겁니다.
- AI의 출력이 그 기대와 어긋날 때 → 예측 오류 → 후속 질문 → Precision Brain 가동.

**출처:** Karpathy (2023.1.24) X/Twitter; Karpathy (2023.5) "State of GPT," Microsoft Build; Karpathy (2023.11) "Intro to Large Language Models," YouTube.

---

## 슬라이드 3: Jensen Huang — "모든 사람이 프로그래머다" (~3분)

### 핵심 인용

> "It is our job to create computing technology such that nobody has to program. And that the programming language is human. Everybody in the world is now a programmer. This is the miracle of artificial intelligence."
>
> — Huang (2024.2), World Government Summit, Dubai

### 핵심 메시지

젠슨 황이 말하는 것은 단순한 접근성의 확대가 아닙니다.

**여러분의 전공 지식(뇌과학, 심리학)이 곧 프로그래밍 언어입니다.**

- C++를 배울 필요가 없습니다. 편도체의 공포 조건화 회로를 정확히 기술할 수 있는 능력 — 그것이 코드입니다.
- 도메인 전문성이 깊을수록, AI에게 내릴 수 있는 지시의 정밀도가 올라갑니다.

### BMB 예시

Cursor에 다음과 같이 입력하면 실제로 동작합니다:

```
"편도체의 공포 조건화 회로(조건 자극 → 시상 → 외측 편도체 → 중심 편도체 → 공포 반응)를
단계별로 시각화하는 인터랙티브 웹앱을 만들어 줘"
```

코딩을 한 줄도 모르는 뇌과학 전공자가 이 문장을 쓸 수 있는 이유는, **도메인 지식이 있기 때문**입니다.

### Inside-Out 연결

AI에게 명령하는 **행동(Action)이 먼저**이고, 코딩에 대한 이해는 그 결과로 따라옵니다.

- 1주차의 핵심: "행동이 지각을 앞선다 (Action precedes Perception)"
- Cursor에서 명령 → 결과 확인 → 예상과 다른 부분 발견 → 수정 → 더 깊은 이해

**출처:** Huang (2024.2) World Government Summit keynote, Dubai — "Who Will Shape the Future of AI?" 세션.

---

## 슬라이드 4: Altman + Musk — "가능성의 확장과 판단의 책임" (~4분)

### Altman: 가능성의 확장

> "We can imagine a world where all of us have access to help with almost any cognitive task, providing a great force multiplier for human ingenuity and creativity."
>
> — Altman (2023.2), "Planning for AGI and beyond," OpenAI Blog

**과거와 현재의 비교:**

| 과거 | 현재 |
|------|------|
| 논문 100편의 초록 분류 = 연구팀 + 수주 | AI 보조로 초벌 분류 가능 (단, 검증은 여러분의 몫) |
| 데이터 시각화 = 프로그래밍 수업 수강 필요 | 자연어로 지시하면 초안 생성 가능 (단, 정확성 확인 필수) |
| 새로운 분야 진입 = 수년의 기초 학습 | 도메인 지식 + AI로 진입 장벽 감소 (단, 깊이는 별개의 문제) |

연구, 공직, 사업, 창작 — 무엇을 꿈꾸든 진입 장벽이 낮아지고 있습니다.

**단, 중요한 전제가 있습니다:** AI는 그럴듯하게 틀릴 수 있습니다(Hallucination). 진입 장벽이 낮아진다는 것은 "검증 없이 써도 된다"는 뜻이 아닙니다. 오히려 **검증 능력 — 즉 여러분의 도메인 전문성 — 이 더욱 중요해집니다.**

### Musk: 판단의 책임

머스크가 자주 인용하는 사고법은 **제1원리 사고(First Principles Thinking)**입니다. 이는 아리스토텔레스 이래 과학적 탐구의 기본 방법론으로, 기존 관행이나 유추에 기대지 않고 근본 원리까지 해체한 뒤 거기서부터 다시 조립하는 것을 뜻합니다.

> "I think it's important to reason from first principles rather than by analogy. [...] First principles is kind of a physics way of looking at the world [...] you boil things down to the most fundamental truths and say, 'okay, what are we sure is true?' and then reason up from there."
>
> — Musk, Kevin Rose Foundation 인터뷰 (2012); Vance (2015) *Elon Musk* 전기 p.354에서 재인용

**AI 시대에 이것이 왜 중요한가:**

- AI의 결과를 검증 없이 수용하는 것 = 1주차의 **멍게(Tunicate)**.
  - 멍게는 정착하여 더 이상 움직일 필요가 없어지면 자신의 뇌(신경계)를 소화시킵니다.
  - **행동을 멈추면 뇌가 불필요해집니다.** AI가 대신 생각해 주는 것에 안주하면, 여러분의 Precision Brain은 가동을 멈춥니다.

### 교차점

Altman과 Musk를 함께 놓으면 하나의 원리가 보입니다:

- AI는 가능성을 확장합니다 (Altman).
- 그러나 **"왜?"를 멈추지 않아야** 그 확장이 의미가 있습니다 (Musk).
- "왜?"를 묻는 행위는 예측 오류를 능동적으로 찾는 행위이며, 이는 Precision Brain을 가동시키는 조건과 유사합니다.

**출처:** Altman (2023.2) "Planning for AGI and beyond," OpenAI Blog; Musk (2012) Kevin Rose Foundation 인터뷰; Vance (2015) *Elon Musk,* HarperCollins, p.354.

---

## 슬라이드 5: 종합 — "오늘부터 바꿀 행동 하나" (~2분)

### 4인의 공통 메시지

| 빌더 | 핵심 메시지 |
|------|------------|
| **Karpathy** | 명확하게 생각하고, 구조적으로 질문하라 |
| **Huang** | 전공 지식이 곧 프로그래밍 언어다 |
| **Altman** | AI는 인간의 창의성을 증폭하는 도구다 |
| **Musk** | 근본 원리부터 따져 묻는 습관을 멈추지 마라 |

### 핵심 원리

> **행동을 바꾸면 생각이 바뀐다.** (Inside-Out)

### 오늘부터 바꿀 행동 3가지

| # | 기존 습관 | 오늘부터의 행동 | Inside-Out 원리 |
|---|----------|---------------|----------------|
| 1 | "답 알려줘" | **"내 가설은 X인데, 틀린 부분을 찾아줘"** | Good-enough Brain의 가설을 먼저 세우고, AI로 예측 오류를 유발 |
| 2 | AI 답변을 그대로 수용 | **AI 답변에서 "예상과 다른 부분"을 찾아 기록하라** (오딧 로그) | 예측 오류를 기록하는 것 자체가 Precision Brain 가동 |
| 3 | 첫 번째 답에서 멈춤 | **"왜?"를 최소 3번 연속 물어라** (질문의 사다리 Level 3 이상) | 반사실적 추론(But What If)으로 내 모델의 허점 발견 |

> **주의:** AI는 자신 있는 어조로 틀린 답을 줄 수 있습니다. 행동 2(오딧 로그)와 행동 3("왜?" 반복)은 이러한 환각(Hallucination)을 잡아내는 실전 훈련이기도 합니다.

### 루프 도식

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Good-enough Brain ──→ 가설 생성 (Action)          │
│         │                                           │
│         ▼                                           │
│   AI에게 질문 ──→ AI 답변 수신                      │
│         │                                           │
│         ▼                                           │
│   예측 오류 (Prediction Error)                      │
│   "내 예상과 다른 부분은 어디인가?"                 │
│   "AI가 틀렸을 가능성은 없는가?"                    │
│         │                                           │
│         ▼                                           │
│   Precision Brain 가동 ──→ 후속 질문 + 모델 업데이트│
│         │                                           │
│         └──────────── 다시 가설 생성 ───────────────┘
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 참고 문헌

1. Karpathy, A. (2023.1.24). X/Twitter post. https://x.com/karpathy/status/1617979122625712128
2. Karpathy, A. (2023.5). "State of GPT." Microsoft Build.
3. Karpathy, A. (2023.11). "Intro to Large Language Models." YouTube.
4. Huang, J. (2024.2). World Government Summit keynote, Dubai — "Who Will Shape the Future of AI?"
5. Altman, S. (2023.2). "Planning for AGI and beyond." OpenAI Blog.
6. Musk, E. (2012). Kevin Rose Foundation 인터뷰.
7. Vance, A. (2015). *Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future.* HarperCollins. p.354.
8. Buzsáki, G. (2019). *The Brain from Inside Out.* Oxford University Press.

## 기존 자료 연결

- **프롬프팅 4원칙 상세**: `class_02_agentic_workflows_claude.md` — 동일한 원칙이 한국어로 상세 기술됨
- **질문의 사다리 (Inquiry Ladder)**: 같은 파일에 4단계(What → How → But What If → So What) 정의됨
- **멍게(Tunicate) 비유**: `class_01_1_agentic_orientation.md` 1-2절 "The Action Machine"에서 재활용
- **First Principles**: 1주차에서 도입됨, 본 슬라이드에서 콜백
- **Good-enough Brain / Precision Brain**: `class_01_1_agentic_orientation.md` 1-4절 핵심 개념 복습
