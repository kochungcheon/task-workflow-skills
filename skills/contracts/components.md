# 재사용 기능과 호출 관계

공개 스킬에서 필요한 기능을 읽어 조합한다. 공개 스킬도 내부적으로 여러 단계를 가질 수 있다. 여기서 도구층이라는 말은 이 워크플로우에 제공하는 책임의 크기를 뜻한다.

## 호출자와 입출력

| 기능 | 호출자 | 입력 → 출력 | 누락·실패 시 |
|---|---|---|---|
| 과제 분해 · to-tickets 기준 | task-delivery | 과제·기준 → 한 기능씩의 TaskPacket, 의존관계 | 모호한 기준/순환 의존을 알려 현재 분해에서 해결 |
| 지도 · task-maps | task-delivery, 단독 지도 요청 | TaskPacket·코드·기존 지도 → MapSet | 불일치·읽을 수 없는 코드·렌더 불가를 blocked로 반환 |
| 구현 · tdd | task-delivery | 합의한 TaskPacket·MapSet → 변경 코드, 실제 Red/Green·회귀 근거 | 환경 오류/기능 실패/범위 변경을 구분해 반환 |
| 근거 · task-evidence | task-delivery, 단독 인계/E2E 검토 | 현재 패키지·실행 기록 → handoff 또는 joint-e2e Evidence | 누락은 blocked/needs_work, 관찰 실패는 fail |
| 책임 설계 · codebase-design | task-maps, tdd의 경계 설계 | 코드·도메인 용어 → 책임/공개 인터페이스 판단 | 결정이 필요한 경계를 표시 |
| 원본 지도 · mermaid-diagrams | task-maps | 노드·관계 → 객체/흐름 .mmd | 문법·누락 관계 수정 |
| 사람이 보는 지도 · visual-explainer | task-maps | 같은 노드·관계·버전 → 검증한 HTML | 렌더 검사 실패 수정, 미확인 범위 표시 |

`task-delivery`만 순서·재시도·멈춤·재개를 결정한다. 공개 기능은 아래 어댑터를 통해 공통 계약에 맞춘다. 파일을 읽어 에이전트가 수행하는 조합이며 함수 호출 API가 아니다.

## to-tickets 어댑터

공개 원문은 수동 호출 및 트래커 게시를 포함한다. 여기서는 **설계 참고**로 읽고, 작은 완결 기능·의존관계·분해 검토 기준을 사용한다. 로컬 트래커는 `.workflow/<과제명>/tasks/`, 상태는 공유 계약, 한 파일에 한 과제로 명시한다. 이 지정으로 별도 트래커 설정 절차 없이 작업한다. 공개 원문의 외부 이슈 게시·전체 frontier 실행을 자동으로 가져오지 않는다.

기계적인 전역 변경은 원문처럼 확장→호출부 이전→옛 형태 제거로 나눌 수 있다. 각 단계에서 실제 확인할 보장과 다음 의존조건을 명시한다.

## tdd 어댑터

현재 과제 하나와 합의한 검증 인터페이스를 전달한다. 테스트 하나의 실제 Red→최소 구현→Green을 반복하고 실제 실행 근거를 반환한다. 공개 `implement`·`implement-spec`의 커밋/전체 실행 정책은 이 기능에 포함되지 않는다. 다음 과제와 공동 E2E의 판단은 호출자가 한다.

## 공식 원문과 경로 해석

스킬은 이름으로 식별하고 아래 고정 버전의 공식 원문을 기준으로 삼는다. 특정 컴퓨터의 사용자 폴더를 실행 경로로 사용하지 않는다.

1. 함께 설치한 패키지가 있으면 아래 상대 경로를 **이 문서가 있는 폴더 기준**으로 읽는다. 현재 작업 디렉터리 기준으로 해석하지 않는다.
2. 함께 설치한 파일이 없으면 현재 환경의 스킬 목록에서 같은 이름의 스킬을 찾고 실제 SKILL.md 위치를 사용한다. 버전이나 동작이 다르면 차이를 먼저 확인한다.
3. 사용할 수 있는 파일이 없으면 누락된 스킬과 공식 원문을 알린다. 설치는 사용자가 요청한 범위에서 수행한다. SKILL.md가 참조하는 파일·렌더 자원도 함께 필요하다.

`task-delivery`, `task-maps`, `task-evidence`, `contracts`는 같은 상위 폴더에 배치한다. 이동할 때 공통 계약과 참조 파일까지 포함한 패키지를 설치한다.

| 스킬 | 패키지 내부 상대 경로 | 고정한 공식 원문 |
|---|---|---|
| to-tickets | `../to-tickets/SKILL.md` | [Matt · to-tickets](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/to-tickets/SKILL.md) |
| tdd | `../tdd/SKILL.md` | [Matt · tdd](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/tdd/SKILL.md) |
| codebase-design | `../codebase-design/SKILL.md` | [Matt · codebase-design](https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/codebase-design/SKILL.md) |
| mermaid-diagrams | `../mermaid-diagrams/SKILL.md` | [agent-toolkit](https://github.com/softaworks/agent-toolkit/blob/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/mermaid-diagrams/SKILL.md) |
| visual-explainer | `../visual-explainer/SKILL.md` | [visual-explainer](https://github.com/nicobailon/visual-explainer/blob/5f378868e0ea745a6284b51e710c390f0c76f72c/plugins/visual-explainer/SKILL.md) |

E2E 실행은 프로젝트 기존 명령과 허용 도구를 우선한다. gstack `qa-only`·Anthropic `webapp-testing`은 과제와 환경이 맞을 때 선택할 후보이며 이 패키지의 필수 의존성이 아니다. 이 패키지는 위 고정 버전의 스킬 폴더와 라이선스를 함께 제공한다. 설치된 상대 경로만으로 참조를 해결할 수 있다.

## 기능을 바꿀 때

변경한 기능의 위 표 호출자를 확인하고 공유 계약의 입력·출력·오류 의미를 대조한다. 같은 계약이면 관련 기능·회귀를 확인한다. 계약이 달라지면 주 버전과 호출부를 맞추고 정상 인계·실패 복귀·사용자 확인 누락·오래된 지도·필수 출력 누락 사례를 다시 검토한다. 원문 스킬 업데이트만으로 계약 호환성을 추정하지 않는다.
