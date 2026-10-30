# 재사용 기능과 호출 관계

공개 스킬에서 필요한 기능을 읽어 조합한다. 공개 스킬도 내부적으로 여러 단계를 가질 수 있다. 여기서 도구층이라는 말은 이 워크플로우에 제공하는 책임의 크기를 뜻한다.

## 호출자와 입출력

| 기능 | 호출자 | 입력 → 출력 | 누락·실패 시 |
|---|---|---|---|
| 과제 분해 · to-tickets 기준 | task-delivery | 원문·합의한 전체 계획 → 기능 순서·의존관계, 현재 TaskPacket | 모호한 기준/순환 의존을 알려 현재 분해에서 해결 |
| 설계 대화 · task-design-dialogue | task-delivery, 단독 설계 대화 | 요구·코드·계획 초안 → 결정 ID·상태·가정·작업/지도 변경 요약 | 현재 구현을 바꾸는 미결정과 근거 부족을 드러내 대화를 이어감 |
| 지도 · task-maps | task-delivery, 단독 지도 요청 | TaskPacket·코드·기존 지도 → MapSet | 불일치·읽을 수 없는 코드·렌더 불가를 blocked로 반환 |
| 구현 · tdd | task-delivery | 합의한 TaskPacket·MapSet → 변경 코드, 실제 Red/Green·회귀 근거 | 환경 오류/기능 실패/범위 변경을 구분해 반환 |
| 근거 · task-evidence | task-delivery, 단독 인계/E2E 검토 | 현재 패키지·실행 기록 → handoff 또는 joint-e2e Evidence | 누락은 blocked/needs_work, 관찰 실패는 fail |
| 자기 설명 기록 · task-evidence learning-review | 학습 모드의 task-delivery, 단독 설명 검토 | 현재 패키지·사용자 설명 → 과제의 LearningNote·복습 색인 | 설명 부재/버전 미확인은 pending, 남은 막힘은 revisit |
| 누적 복습 문서 · task-review | 학습 모드의 task-delivery, 단독 복습·인터뷰 준비 | 계획·모든 작업·지도·코드·검증·설명 → `review.md` 파생 요약 | 출처·현재 코드 불일치는 표시하고 해당 완료 주장을 보류 |
| 책임 설계 · codebase-design | task-maps, tdd의 경계 설계 | 코드·도메인 용어 → 책임/공개 인터페이스 판단 | 결정이 필요한 경계를 표시 |
| 원본 지도 · mermaid-diagrams | task-maps | 노드·관계 → 객체/흐름 .mmd | 문법·누락 관계 수정 |
| 사람이 보는 지도 · visual-explainer | task-maps | 같은 노드·관계·버전 → 검증한 HTML | 렌더 검사 실패 수정, 미확인 범위 표시 |
| 기술 문서 문장 · simple-english/한국어 어댑터 | task-delivery, task-design-dialogue, task-maps, task-evidence | 계획·작업·HTML·인계의 설명 문장 → 한 번에 읽히는 문장 | 언어에 맞는 규칙을 골라 사실·코드·근거를 보존 |

`task-delivery`만 순서·재시도·멈춤·재개를 결정한다. 공개 기능은 아래 어댑터를 통해 공통 계약에 맞춘다. 파일을 읽어 에이전트가 수행하는 조합이며 함수 호출 API가 아니다.

티켓 분해와 함께 찾은 기술적 선택은 `plan.md`의 PlanNote에 결정 ID로 둔다. `task-delivery`가 요구·코드의 사실과 작업 순서의 초안을 먼저 만들고 `task-design-dialogue`로 중요한 선택을 사용자와 왕복한다. 현재 작업 MD는 요구·결정·반영된 가정 ID를 참조한다. `task-maps`는 결정 ID를 관련 책임 노드와 HTML 요약에 연결하고 현재 작업의 미확인 가정도 표시한다. `task-evidence`는 구현된 선택과 근거가 계획·지도와 맞는지 확인한다. 도구층은 같은 계획·작업을 입력으로 받는다.

해커톤·시험 대비에서는 `task-delivery`가 기능 검증 뒤 짧은 설명을 요청하고 `learning-review`에 실제 응답을 전달한다. `task-maps`는 같은 과제의 이해 기록과 관련 노드를 연결한다. LearningNote는 v1의 선택 확장이며 기존 Evidence·verified 의미는 유지한다.

`task-review`는 위 원본의 누적 읽기 화면을 만든다. 최초 계획 뒤, 현재 기능의 인계·공동 E2E·설명 뒤 바뀐 부분만 갱신한다. 사용자는 이 문서와 HTML 지도로 현재까지의 선택·검증·다음 대화 지점을 보고, 에이전트는 원본 링크를 따라 현재 코드와 대조한다. ReviewBrief는 상태의 정본이나 추가 승인 관문이 아니다.

## to-tickets 어댑터

공개 원문은 수동 호출 및 트래커 게시를 포함한다. 여기서는 **설계 참고**로 읽고, 작은 완결 기능·의존관계·분해 검토 기준을 사용한다. 로컬 트래커는 `.workflow/<과제명>/tasks/`, 상태는 공유 계약, 한 파일에 한 과제로 명시한다. 이 지정으로 별도 트래커 설정 절차 없이 작업한다. 공개 원문의 외부 이슈 게시·전체 frontier 실행을 자동으로 가져오지 않는다.

기계적인 전역 변경은 원문처럼 확장→호출부 이전→옛 형태 제거로 나눌 수 있다. 각 단계에서 실제 확인할 보장과 다음 의존조건을 명시한다.

## tdd 어댑터

현재 과제 하나와 합의한 검증 인터페이스를 전달한다. 해커톤 모드에서 서브 에이전트가 가능하면 TDD 구현을 위임하고, 호출자는 계획·지도·상태·사용자 소통과 결과 검토를 유지한다. 수행자는 테스트 하나의 실제 Red→최소 구현→Green을 반복하고 코드·실행 근거·막힌 결정을 반환한다. 공개 `implement`·`implement-spec`의 커밋/전체 실행 정책은 이 기능에 포함되지 않는다. 다음 과제와 공동 E2E의 판단은 호출자가 한다.

## simple-english 문서 어댑터

영어 기술 문서를 쓸 때 `simple-english`를 읽고 원문의 문서 규칙을 적용한다. 한국어 계획·작업·지도 HTML·인계에는 다음 한국어 규칙을 적용한다: 결론이나 관찰 결과를 먼저 쓰고, 한 문장에 한 동작·사실을 담으며, 조건과 행위자를 드러낸다. `계획`, `구현`, `검증 완료`, `대기`를 구분하고 각각의 코드·실행 근거를 연결한다. 영어 단어 수·어휘·시제 규칙을 한국어에 적용하거나 한국어 문서를 영어로 번역하지 않는다. 코드·명령·식별값·인용·검증 결과는 문체를 위해 바꾸지 않는다. 원문의 영어 채팅 답변 형식도 한국어 대화에 강제하지 않는다. 문서가 바뀌는 시점에 짧게 점검하며 별도 문서 정리 단계를 추가하지 않는다.

## 공식 원문과 경로 해석

스킬은 이름으로 식별하고 아래 고정 버전의 공식 원문을 기준으로 삼는다. 특정 컴퓨터의 사용자 폴더를 실행 경로로 사용하지 않는다.

1. 함께 설치한 패키지가 있으면 아래 상대 경로를 **이 문서가 있는 폴더 기준**으로 읽는다. 현재 작업 디렉터리 기준으로 해석하지 않는다.
2. 함께 설치한 파일이 없으면 현재 환경의 스킬 목록에서 같은 이름의 스킬을 찾고 실제 SKILL.md 위치를 사용한다. 버전이나 동작이 다르면 차이를 먼저 확인한다.
3. 사용할 수 있는 파일이 없으면 누락된 스킬과 공식 원문을 알린다. 설치는 사용자가 요청한 범위에서 수행한다. SKILL.md가 참조하는 파일·렌더 자원도 함께 필요하다.

`task-delivery`, `task-design-dialogue`, `task-maps`, `task-evidence`, `task-review`, `contracts`는 같은 상위 폴더에 배치한다. 이동할 때 공통 계약과 참조 파일까지 포함한 패키지를 설치한다.

| 스킬 | 패키지 내부 상대 경로 | 고정한 공식 원문 |
|---|---|---|
| to-tickets | `../to-tickets/SKILL.md` | [Matt · to-tickets](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/to-tickets/SKILL.md) |
| tdd | `../tdd/SKILL.md` | [Matt · tdd](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/tdd/SKILL.md) |
| codebase-design | `../codebase-design/SKILL.md` | [Matt · codebase-design](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/codebase-design/SKILL.md) |
| mermaid-diagrams | `../mermaid-diagrams/SKILL.md` | [agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/mermaid-diagrams/SKILL.md) |
| visual-explainer | `../visual-explainer/SKILL.md` | [visual-explainer](https://github.com/nicobailon/visual-explainer/blob/5f378868e0ea745a6284b51e710c390f0c76f72c/plugins/visual-explainer/SKILL.md) |
| simple-english | `../simple-english/SKILL.md` | [AminBlg · SimpleEnglish](https://github.com/AminBlg/SimpleEnglish/blob/a6fcb4fde098b33617cc1578d151ebf58774b883/skills/simple-english/SKILL.md) |

E2E 실행은 프로젝트 기존 명령과 허용 도구를 우선한다. gstack `qa-only`·Anthropic `webapp-testing`은 과제와 환경이 맞을 때 선택할 후보이며 이 패키지의 필수 의존성이 아니다. 이 패키지는 위 고정 버전의 스킬 폴더와 라이선스를 함께 제공한다. 설치된 상대 경로만으로 참조를 해결할 수 있다. `simple-english`의 Claude·Codex 플러그인 훅과 출력 스타일은 묶지 않는다. 문서 작성 스킬만 설치한다.

## 기능을 바꿀 때

변경한 기능의 위 표 호출자를 확인하고 공유 계약의 입력·출력·오류 의미를 대조한다. 같은 계약이면 관련 기능·회귀를 확인한다. 계약이 달라지면 주 버전과 호출부를 맞추고 정상 인계·실패 복귀·사용자 확인 누락·오래된 지도·필수 출력 누락 사례를 다시 검토한다. 원문 스킬 업데이트만으로 계약 호환성을 추정하지 않는다.
