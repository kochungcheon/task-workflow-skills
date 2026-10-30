# Task Workflow Skills

## 무엇을 하는가

과제 MD를 작은 기능으로 나누고, 중요한 기술 선택은 사용자와 논의합니다. 해커톤 모드에서는 현재 기능의 TDD를 전담 서브 에이전트에게 맡기고, 주 에이전트가 설계·지도·결과 검토를 맡습니다. 사용자는 구현 중 객체·흐름 HTML 지도로 맥락을 확인합니다. 함께 E2E로 실제 동작을 검증하고, 사용자가 선택 이유를 짧게 설명한 뒤 다음 기능으로 갑니다. 서브 에이전트를 사용할 수 없으면 주 에이전트가 같은 TDD 절차를 수행합니다.

산출물은 `.workflow/<과제명>/` 아래에 둡니다. 결정과 작업 순서는 `plan.md`, 현재 기능은 `tasks/T01.md`, 읽을 지도는 `maps/view.html`, 실행 근거는 `evidence/T01/`에 남습니다.

## 포함한 스킬

| 레이어 | 스킬 | 역할 |
|---|---|---|
| 자동화 | [task-delivery](skills/task-delivery/SKILL.md) | 전체 순서·현재 작업·검증 후 다음 작업 관리 |
| 도구 | [task-design-dialogue](skills/task-design-dialogue/SKILL.md) | 기술 선택 문답과 결정·가정 기록 |
| 도구 | [task-maps](skills/task-maps/SKILL.md) | 객체·흐름 지도와 HTML 생성·갱신 |
| 도구 | [task-evidence](skills/task-evidence/SKILL.md) | 구현 인계·공동 E2E·설명 근거 정리 |

공개 스킬 5개도 묶었습니다: `to-tickets`(기능 분해), `tdd`(테스트 후 구현), `codebase-design`(책임 설계), `mermaid-diagrams`(지도 원본), `visual-explainer`(HTML). 출처와 라이선스는 [THIRD_PARTY.md](THIRD_PARTY.md)에 있습니다.

## 어떻게 쓰는가

Python 3.10 이상에서 스킬 묶음을 설치합니다. `my-project`는 사용할 프로젝트 경로로 바꿉니다.

```bash
git clone https://github.com/kochungcheon/task-workflow-skills.git
cd task-workflow-skills
python3 scripts/install.py --target ../my-project/.agents/skills
```

Codex 개인 스킬 폴더에 설치하려면 `--target ~/.codex/skills`를 사용합니다. 프로젝트 AGENTS.md에서 연결하려면 [AGENTS.snippet.md](AGENTS.snippet.md)를 참고합니다. HTML 지도를 만들 때는 Node.js 20 이상과 Chrome/Chromium을 준비하고 `npm ci --prefix ../my-project/.agents/skills/visual-explainer`를 한 번 실행합니다.

과제 MD 경로와 함께 다음처럼 요청합니다.

> 이 과제를 3시간 해커톤용 `task-delivery`로 진행하자. 티켓과 중요한 기술 선택의 초안을 먼저 보여줘. 결정 후 현재 작업 MD와 지도를 만들고, 현재 작업의 TDD는 서브 에이전트에게 맡겨줘. 나는 지도를 읽고 함께 E2E를 확인한 다음, 설명하고 다음 기능으로 갈게.

`$task-delivery <과제 MD 경로>`로 시작해도 됩니다. 설계 대화만 필요하면 `task-design-dialogue`, 지도만 필요하면 `task-maps`, 인계·검증 근거만 필요하면 `task-evidence`를 요청합니다. 구현 보고 뒤에는 공동 E2E로 결과를 확인하고 같은 작업을 마친 다음 다음 작업으로 진행합니다.
