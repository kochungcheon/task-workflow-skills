# Task Workflow Skills

## 무엇을 하는가

과제 MD를 작은 기능으로 나누고, 중요한 기술 선택은 사용자와 논의합니다. 해커톤 모드에서는 독립적인 요구·코드·환경 조사를 동시에 수행할 수 있고, 결과는 하나의 설계 초안에 합칩니다. 그 뒤에는 현재 기능 하나만 TDD로 구현합니다. 사용자는 구현 전에 정한 HTML 지도와 누적 복습 문서를 읽고, 에이전트는 같은 기능의 E2E를 준비합니다. 인계 때 실제 코드와 지도를 대조하고 함께 E2E로 확인한 뒤, 사용자가 선택 이유를 짧게 설명하고 다음 기능으로 갑니다. 개발 뒤에는 누적 복습 문서의 중요한 선택·검증·열린 질문으로 인터뷰 답변을 연습합니다. 병렬 독립성이 애매하면 순차로 진행합니다. 서브 에이전트를 사용할 수 없으면 주 에이전트가 같은 TDD 절차를 수행합니다.

산출물은 `.workflow/<과제명>/` 아래에 둡니다. 결정과 작업 순서는 `plan.md`, 지금까지의 복습·인터뷰 브리프는 `review.md`, 현재 기능은 `tasks/T01.md`, 읽을 지도는 `maps/view.html`, 실행 근거는 `evidence/T01/`에 남습니다.

## 포함한 스킬

| 레이어 | 스킬 | 역할 |
|---|---|---|
| 자동화 | [task-delivery](skills/task-delivery/SKILL.md) | 전체 순서·현재 작업·검증 후 다음 작업 관리 |
| 도구 | [task-design-dialogue](skills/task-design-dialogue/SKILL.md) | 기술 선택 문답과 결정·가정 기록 |
| 도구 | [task-maps](skills/task-maps/SKILL.md) | 객체·흐름 지도와 HTML 생성·갱신 |
| 도구 | [task-evidence](skills/task-evidence/SKILL.md) | 구현 인계·공동 E2E·설명 근거·누적 복습 문서 정리 |

공개 스킬 6개도 묶었습니다: `to-tickets`(기능 분해), `tdd`(테스트 후 구현), `codebase-design`(책임 설계), `mermaid-diagrams`(지도 원본), `visual-explainer`(HTML), `simple-english`(기술 문장). 출처와 라이선스는 [THIRD_PARTY.md](THIRD_PARTY.md)에 있습니다.

`simple-english` 원문은 영어 문서용입니다. 영어 문서에는 원문 규칙을 적용합니다. 한국어 계획·작업·지도에는 [문서 어댑터](skills/contracts/components.md#simple-english-문서-어댑터)의 명료성 원칙만 적용합니다. 한국어를 영어로 번역하거나 영어 단어 수 규칙을 강제하지 않습니다. 패키지에는 문서 스킬만 포함하며 별도 세션 훅·출력 스타일은 설치하지 않습니다.

## 어떻게 쓰는가

Python 3.10 이상에서 스킬 묶음을 설치합니다. `my-project`는 사용할 프로젝트 경로로 바꿉니다.

```bash
git clone https://github.com/kochungcheon/task-workflow-skills.git
cd task-workflow-skills
python3 scripts/install.py --target ../my-project/.agents/skills
```

Codex 개인 스킬 폴더에 설치하려면 `--target ~/.codex/skills`를 사용합니다. 프로젝트 AGENTS.md에서 연결하려면 [AGENTS.snippet.md](AGENTS.snippet.md)를 참고합니다. HTML 지도를 만들 때는 Node.js 20 이상과 Chrome/Chromium을 준비하고 `npm ci --prefix ../my-project/.agents/skills/visual-explainer`를 한 번 실행합니다.

과제 MD 경로와 함께 다음처럼 요청합니다.

> 이 과제를 3시간 해커톤용 `task-delivery`로 진행하자. 독립적인 사실 조사는 병렬로 하고 하나의 티켓·기술 선택 초안으로 합쳐줘. 결정 후 현재 작업 MD·지도·누적 복습 문서를 만들고, 현재 작업 하나만 TDD로 구현해줘. 나는 구현 중 지도와 복습 문서를 읽고, 함께 E2E를 확인한 다음 설명하고 다음 기능으로 갈게. 끝나면 중요한 기술 선택과 검증을 바탕으로 인터뷰 답변을 연습하자. 병렬로 해도 될지 애매하면 순차로 진행해줘.

`$task-delivery <과제 MD 경로>`로 시작해도 됩니다. 설계 대화만 필요하면 `task-design-dialogue`, 지도만 필요하면 `task-maps`, 인계·검증·누적 복습만 필요하면 `task-evidence`를 요청합니다. 영어 기술 문서를 따로 다듬을 때는 `simple-english`를 직접 호출할 수 있습니다. 구현 보고 뒤에는 공동 E2E로 결과를 확인하고 같은 작업을 마친 다음 다음 작업으로 진행합니다.
