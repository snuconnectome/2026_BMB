function createAILiteracySurvey() {
  // 1. 폼 생성 및 제목/설명 설정
  var form = FormApp.create('🤖 2026 BMB AI 리터러시 및 에이전시(Agency) 사전 설문');
  form.setDescription('이 설문은 여러분이 단순히 AI의 "버튼을 누를 줄 아는지" 묻는 것이 아닙니다.\n우리가 평가하고자 하는 것은 여러분의 인지적 주권(Cognitive Sovereignty)과 예측 불확실성을 다루는 태도입니다. 솔직하게 답변해 주시기 바랍니다.');

  // 2. Part 1: AI 활용도 및 플랫폼 경험 (Technical Baseline)
  form.addSectionHeaderItem().setTitle('Part 1: AI 활용도 및 플랫폼 경험 (Technical Baseline)');
  
  form.addCheckboxItem()
      .setTitle('1. 현재 구독 중인 유료 AI 서비스는 무엇입니까? (중복 선택 가능)')
      .setChoiceValues([
        'ChatGPT Plus (OpenAI)',
        'Claude Pro (Anthropic)',
        'Perplexity Pro',
        '유료 서비스 구독하지 않음'
      ])
      .showOtherOption(true)
      .setRequired(true);

  form.addMultipleChoiceItem()
      .setTitle('2. 지난 한 달간 가장 주된 AI 활용 목적은 무엇이었습니까?')
      .setChoiceValues([
        '과제/어학 등 텍스트 번역 및 교정',
        '모르는 개념이나 정보 단순 검색',
        '코드 작성, 디버깅, 혹은 데이터 분석',
        '장문 텍스트 요약 및 브레인스토밍',
        'AI를 활용한 능동적인 학습 프로세스 구축 (에이전트 활용)'
      ])
      .setRequired(true);

  // 3. Part 2: 인지적 조향(Cognitive Steering) 및 예측 오차(Prediction Error)에 대한 태도
  form.addSectionHeaderItem().setTitle('Part 2: 인지적 조향(Cognitive Steering) 및 예측 오차(Prediction Error)에 대한 태도');

  form.addMultipleChoiceItem()
      .setTitle('3. AI가 엉뚱한 대답이나 명백한 사실 오류(Hallucination)를 내놓았을 때, 당신의 주된 반응은?')
      .setChoiceValues([
        'A. "AI는 아직 한계가 명확하군. 차라리 구글 검색이나 논문을 직접 읽는 게 낫겠다." (도구 폐기)',
        'B. "내가 질문(Prompt)을 잘못 했나 보네. 정답이 나올 때까지 프롬프트를 조금씩 바꿔본다." (수동적 조향)',
        'C. "재밌군. 내 가설(Prediction)과 어떻게 왜 틀렸는지 분석하고, NotebookLM의 특정 데이터를 지시하여 내 논리대로 AI를 강제 교정(Steering)한다." (인지적 대결)'
      ])
      .setRequired(true);

  form.addMultipleChoiceItem()
      .setTitle('4. 학습(Learning)이란 무엇이라고 확신하십니까?')
      .setChoiceValues([
        'A. 세계에 이미 존재하는 방대한 지식을 뇌라는 하드디스크에 오류 없이 저장하는 것. (Outside-In)',
        'B. 내 뇌가 만든 세상에 대한 질문(Hypothesis)을 테스트하기 위해 행동하고, 그 과정에서 발생한 오차(Error)를 통해 모델을 수정하는 것. (Inside-Out)'
      ])
      .setRequired(true);

  form.addMultipleChoiceItem()
      .setTitle('5. AI 시대에 인간 고유의 역할은 무엇이 될 것이라 직관하십니까?')
      .setChoiceValues([
        'A. AI가 만든 창작물에 대한 최종 검토 및 윤리적 책임의 수행자',
        'B. 높은 품질의 질문 도출 및 정교한 프롬프트 엔지니어로 진화',
        'C. 도구를 도구로 남겨두고 인간 본연의 인문학적 소양 탐구',
        'D. AI의 논리 회로와 격렬하게 충돌(Sparring)하며, 인간 자신의 예측 모델을 부수는 파괴적 지휘자'
      ])
      .setRequired(true);

  // 4. Part 3: 선언적 서약 (Declaration)
  form.addSectionHeaderItem()
      .setTitle('Part 3: 선언적 서약 (Declaration)')
      .setHelpText('본 수업은 기존의 수동적 학습 방식을 지양합니다. 만약 당신이 AI가 요약해 준 자료를 수동적으로 암기하고 제출할 생각이라면, 이 강좌가 추구하는 방향과 큰 괴리가 있을 것입니다.');

  form.addCheckboxItem()
      .setTitle('서약 내용 확인 (필수)')
      .setChoiceValues([
        '본인은 본 강좌에서 AI 도구 사용 시 능동적 조향(Steering)을 수행할 것이며, 대화의 과정(Audit Log)을 투명하게 기록함으로써 AI에게 끌려가지 않고 나의 주체적인 사고력과 판단력을 온전히 키워나갈 것을 서약합니다.'
      ])
      .setRequired(true);

  // 5. 완료 후 터미널(로그)에 링크 출력
  Logger.log('=========================================');
  Logger.log('✅ 구글 폼 생성이 완료되었습니다!');
  Logger.log('🔗 수정용 링크 (교수님용): ' + form.getEditUrl());
  Logger.log('🔗 배포용 링크 (학생 배포용): ' + form.getPublishedUrl());
  Logger.log('=========================================');
}
