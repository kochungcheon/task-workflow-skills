# Task Workflow Skills

## 무엇을 하는가

과제 MD를 작은 기능으로 나누고, 중요한 기술 선택은 사용자와 논의합니다. 해커톤 모드에서는 독립적인 요구·코드·환경 조사를 동시에 수행할 수 있고, 결과는 하나의 설계 초안에 합칩니다. 중요한 설계는 이전 대화를 전달받지 않은 리뷰어가 요구·작업 MD·지도·관련 코드로 검토합니다. 그 뒤에는 현재 기능 하나만 TDD로 구현합니다. 사용자는 구현 전에 정한 HTML 지도와 누적 복습 문서를 읽고, 에이전트는 같은 기능의 E2E를 준비합니다. 인계 전에 변경 코드와 주변 경로를 리뷰하고 프로젝트의 자동 검사를 실행합니다. 주요 지적을 해결하고 영향을 받는 검사·리뷰를 다시 확인한 뒤 실제 코드와 지도를 맞춰 공동 E2E로 확인합니다. 그 뒤 사용자가 선택 이유를 짧게 설명하고 다음 기능으로 갑니다. 개발 뒤에는 누적 복습 문서의 중요한 선택·검증·열린 질문으로 인터뷰 답변을 연습합니다. 병렬 독립성이 애매하면 순차로 진행합니다. 서브 에이전트를 사용할 수 없으면 주 에이전트가 같은 TDD 절차를 수행합니다.

초기 분석, 현재 기능의 착수 전, 구현·검증 중에 고객 정책의 빈틈이 발견되면 `task-customer-interview`를 호출합니다. 사용자가 고객사 담당자나 챗봇에게 질문을 전달하고 답변을 가져오는 방식으로 시작합니다. 답변의 출처와 해석을 구분해 요구·인수 기준에 반영한 뒤 기술 설계와 구현을 이어갑니다. 분석·리뷰에서는 구현 결과를 바꾸는 개념의 의미·관계와 업무 규칙의 조건·예외·출처를 기본으로 점검합니다. 필요한 보완은 기존 요구·질문·인수 기준에 짧게 연결하고, 정의의 정본을 구현자와 리뷰어가 함께 참조합니다.

산출물은 `.workflow/<과제명>/` 아래에 둡니다. 고객 질문·답변·출처, 결정과 작업 순서는 `plan.md`, 지금까지의 복습·인터뷰 브리프는 `review.md`, 현재 기능은 `tasks/T01.md`, 읽을 지도는 `maps/view.html`, 설계·코드 리뷰와 자동 검사·E2E 근거는 `evidence/T01/`에 남습니다.

## 포함한 스킬

전체 호출 관계와 고객 인터뷰·독립 리뷰의 재개 경로는 [스킬 구조 지도](docs/workflow.html)에서 확인합니다.

| 레이어 | 스킬 | 역할 |
|---|---|---|
| 자동화 | [task-delivery](skills/task-delivery/SKILL.md) | 전체 순서·현재 작업·검증 후 다음 작업 관리 |
| 도구 | [task-customer-interview](skills/task-customer-interview/SKILL.md) | 고객 업무·정책·예외 확인과 답변의 요구·인수 기준 연결 |
| 도구 | [task-design-dialogue](skills/task-design-dialogue/SKILL.md) | 기술 선택 문답과 결정·가정 기록 |
| 도구 | [task-quality-review](skills/task-quality-review/SKILL.md) | 중요한 설계의 독립 검토와 변경 코드·문서 정합성 리뷰 |
| 도구 | [task-maps](skills/task-maps/SKILL.md) | 객체·흐름 지도와 HTML 생성·갱신 |
| 도구 | [task-evidence](skills/task-evidence/SKILL.md) | 구현 인계·공동 E2E·기능별 설명 근거 정리 |
| 도구 | [task-review](skills/task-review/SKILL.md) | 누적 `review.md`와 기술 인터뷰 복습 질문 정리 |

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

과제 MD 경로와 함께 `$task-delivery ./requirements.md`로 시작합니다. 해커톤 시작·고객 인터뷰·설계 문답·독립 리뷰·지도 갱신·구현 재개·공동 E2E·전체 복습까지 복사해 쓸 문장은 **[워크플로우 사용 예제](docs/usage-examples.md)**에 모았습니다. 영어 기술 문서를 따로 다듬을 때는 `simple-english`를 직접 호출할 수 있습니다.

서버에 Chrome/Chromium이 없으면 [서버 미리보기 절차](skills/contracts/server-preview.md)를 사용합니다. 완성 HTML을 생성해 미리보기 서버로 제공하고, HTTP 응답·사용자 화면 확인·앱 기능 E2E를 따로 기록합니다.

## Python 프로젝트에 적용하기

[Python 코드 가이드](skills/contracts/python-guidelines.md)에 도메인별 구조, API → Service → Handler → Repository의 호출 규칙, 트랜잭션·오류·테스트 기준을 정리했습니다. 가이드는 스킬과 함께 설치되며, `task-delivery`와 설계·지도·리뷰 도구가 Python 작업에서 읽습니다. 기존 프로젝트의 명시된 규약과 적용 범위를 먼저 확인합니다.

개발 도구가 필요한 새 프로젝트에는 Ruff의 lint와 formatter를 제안합니다. 설치할 환경·기존 설정을 확인한 뒤 아래 명령을 **소비 프로젝트의 `pyproject.toml`이 있는 디렉터리**에서 실행합니다. [Ruff 설치](https://docs.astral.sh/ruff/installation/) · [uv 설치](https://docs.astral.sh/uv/getting-started/installation/)

첫 전체 검사 전에 가이드의 [설정과 적용 범위](skills/contracts/python-guidelines.md#설정과-적용-범위)를 반영해 설치된 스킬과 생성 산출물을 제외합니다.

```bash
uv add --dev ruff
uv run ruff check .
uv run ruff format --check .
```

설정 예시, 설치된 스킬·생성 산출물의 검사 제외, pip/venv 방식과 기존 도구가 있는 프로젝트의 적용 절차는 가이드에 있습니다. 개발 의존성과 잠금 파일은 소비 프로젝트에서 관리하고, 실행 결과는 현재 작업의 구현 검사 기록에 연결합니다.
