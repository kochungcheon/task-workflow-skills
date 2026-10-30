# Task Workflow Skills

작은 기능 하나를 **공유 지도 → TDD → 구현 인계 → 사용자와 공동 E2E**까지 확인하고 다음 기능으로 진행하는 에이전트 스킬 묶음입니다.

`task-delivery`가 진행을 관리하고 `task-maps`와 `task-evidence`가 산출물을 만듭니다. 에이전트가 읽고 수행하는 절차이며, 별도 서버나 자동 실행 엔진은 없습니다.

## 포함한 스킬

| 구분 | 스킬 | 역할 |
|---|---|---|
| 자동화 | [task-delivery](skills/task-delivery/SKILL.md) | 분해·현재 과제·인계 후 대기·공동 검증·다음 과제 |
| 도구 | [task-maps](skills/task-maps/SKILL.md) | 객체 지도와 프로젝트 흐름 지도 생성·갱신 |
| 도구 | [task-evidence](skills/task-evidence/SKILL.md) | handoff와 joint-e2e 근거·판정 |
| 공개 기능 | to-tickets · tdd · codebase-design | 작은 기능 분해 기준·TDD·책임과 경계 설계 |
| 공개 기능 | mermaid-diagrams · visual-explainer | 지도 원본과 사용자용 HTML |

공개 스킬 5개는 **고정 커밋의 전체 스킬 폴더와 라이선스**를 함께 넣었습니다. 원문과 버전은 [THIRD_PARTY.md](THIRD_PARTY.md), 파일별 SHA-256은 [dependencies.lock.json](dependencies.lock.json)에 있습니다. `to-tickets`는 분해 기준을 참고하며 원본의 외부 이슈 게시 절차를 자동 실행하지 않습니다.

## 다른 프로젝트에 가져가기

Python 3.10 이상이 필요합니다. 문서·스킬 설치에는 추가 Python 패키지나 네트워크가 필요하지 않습니다.

```bash
git clone https://github.com/kochungcheon/task-workflow-skills.git
cd task-workflow-skills
python3 scripts/check.py
python3 scripts/install.py --target ../my-project/.agents/skills
```

`my-project`를 사용할 프로젝트 위치로 바꿉니다. 대상 도구가 다른 스킬 폴더를 사용하면 `--target`에 그 폴더를 지정합니다. 예를 들어 개인 Codex 스킬 폴더에 설치하려면 `--target ~/.codex/skills`를 사용할 수 있습니다. 기존 스킬이 다른 내용이면 설치를 중단하며 덮어쓰지 않습니다. 같은 내용으로 다시 실행하면 그대로 재사용합니다.

설치기는 스킬 8개와 공통 `contracts` 폴더를 함께 복사합니다. **SKILL.md 하나만 복사하면 공통 계약·참조 파일을 잃습니다.** 개별 스킬만 내려받는 일반 설치기 대신 위 패키지 설치 명령을 사용하세요. 설치 후 도구의 스킬 목록을 다시 불러오거나 새 세션에서 시작합니다.

프로젝트에서 직접 읽게 하려면 [AGENTS.snippet.md](AGENTS.snippet.md)의 짧은 연결 문구를 기존 AGENTS.md에 추가할 수 있습니다. 설치기는 기존 프로젝트 지침을 수정하지 않습니다.

### HTML 지도 렌더링

HTML을 만들고 검증할 때는 Node.js 20 이상과 Chrome/Chromium, Playwright Core가 필요합니다. 브라우저는 운영 환경에서 준비하고 다음 명령으로 고정된 Node 의존성을 설치합니다.

```bash
npm ci --prefix ../my-project/.agents/skills/visual-explainer
node ../my-project/.agents/skills/visual-explainer/kit/render.mjs path/to/map.src.html
```

스킬 문서에서 렌더러 위치는 **실제로 읽은 visual-explainer 폴더**를 기준으로 정합니다. 영상·슬라이드·MCP 확장은 해당 원문의 별도 의존성을 따르며 이 워크플로우의 필수 기능은 아닙니다.

## 시작 문장

> 이 과제를 task-delivery 워크플로우로 분해해줘. 첫 서브 과제의 인수 기준, 객체 지도, 프로젝트 흐름 지도, TDD 검증 지점부터 보여줘. 구현 뒤에는 근거를 인계하고 공동 E2E를 함께 확인하자.

기본 수행자는 현재 에이전트입니다. 별도 에이전트 위임은 요청했을 때 사용합니다. 이미 합의한 범위·검증 지점은 재사용합니다.

`awaiting_joint_e2e`는 **구현 완료·공동 검증 대기**입니다. 현재 코드의 필수 E2E 통과와 사용자 결과 확인이 있어야 `verified`가 됩니다. 실패하면 같은 과제를 수정합니다.

## 경로와 버전 관리

- 패키지 내부 참조는 문서 위치 기준 상대 경로입니다. 특정 사용자의 절대 경로를 저장하지 않습니다.
- 의존 스킬은 같은 상위 폴더에 설치합니다. 없으면 현재 환경의 스킬 목록에서 이름으로 찾습니다.
- 공식 GitHub URL은 출처와 업데이트 기준입니다. 실행 중 매번 최신 원문을 내려받는 방식은 사용하지 않습니다.
- 업데이트할 때 고정 커밋·해시·라이선스와 호출 계약을 함께 확인합니다. 버전이 새롭다는 이유만으로 호환된다고 판단하지 않습니다.

## 자료와 검증

- [설계 이유](docs/workflow-design.md) · [HTML 설명 원본](docs/workflow.src.html) · [완성 HTML 다운로드](https://raw.githubusercontent.com/kochungcheon/task-workflow-skills/main/docs/workflow.html)
- [확인한 범위와 결과](docs/validation.md)
- [공유 계약](skills/contracts/task-workflow-v1.md) · [호출 관계와 공식 원문](skills/contracts/components.md) · [과제 양식](skills/task-delivery/assets/task.md)
- `python3 scripts/check.py`: 원문 해시·필수 자원·내부 링크·개인 절대 경로 점검
- `python3 -m unittest discover -s tests -v`: 설치·경로 이동·재실행·충돌 보존 검사

전체 실제 과제 한 회차의 행동 검증은 아직 수행하지 않았습니다. 사후 자기 설명 연습은 별도 설계이며, 6문항을 자동 출제하거나 프롬프트를 자동 채점하는 스킬은 이 묶음에 포함되지 않습니다.

작성한 스킬·설치 도구는 [MIT](LICENSE), 공개 스킬은 각각 동봉된 원저자의 MIT 라이선스를 따릅니다.
