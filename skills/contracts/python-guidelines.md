# Python 애플리케이션 코드 가이드

Python 업무 애플리케이션을 설계·구현·리뷰할 때 읽는다. 기능을 업무 도메인별로 묶고, API → Service → Handler → Repository의 책임과 호출 방향을 기준으로 작업한다.

먼저 소비 프로젝트의 AGENTS.md, 기존 코드, Python 지원 버전, 의존성 파일, 검사 설정과 CI를 확인한다. 프로젝트에 명시된 규약과 사용자가 정한 범위를 우선하며, 규약이 없는 새 업무 애플리케이션에는 아래 구조를 기본으로 적용한다. 기존 구조와 차이가 있으면 현재 작업에 적용할 범위와 이유를 `plan.md`에 남긴다. 파일과 클래스는 책임·변경 이유에 따라 나누고, 업무 애플리케이션의 저장 책임은 Repository에 둔다. 일회성 스크립트·순수 계산 도구는 필요한 함수와 모듈로 구성하며, 간단한 파일 입출력도 그 범위 안에서 처리할 수 있다.

## 도메인과 호출 방향

`orders`, `inventory`처럼 업무 용어로 모듈을 구분한다. 한 도메인의 정책과 데이터 접근은 그 도메인이 소유한다. 아래 표는 업무 계층 사이의 호출 기준이다. 입력 모델·오류 타입·로깅·순수 계산 도구와 의존성 주입은 해당 책임에 맞춰 사용할 수 있다.

| 계층 | 맡는 일 | 허용하는 업무 호출 | 제한하는 호출 |
|---|---|---|---|
| API | 요청 형식 검증, 인증 정보 전달, 결과·오류의 응답 변환 | 요청마다 하나의 Service 진입 함수 | Handler·Repository 직접 호출, 여러 Service의 조합 |
| Service | 유스케이스의 처리 순서와 트랜잭션 범위 구성 | 필요한 Handler 함수의 조합 | 다른 Service 함수, Repository의 직접 호출 |
| Handler | 권한·상태·업무 조건 판단과 업무 동작 구현 | Repository와 다른 Handler | API·Service 호출 |
| Repository | 저장·조회·조건부 변경과 저장소 오류 처리 | DB·파일·저장소 드라이버와 저장 관련 내부 도구 | API·Service·Handler 호출 |

한 Service에 여러 공개 유스케이스 함수를 둘 수 있다. API의 각 요청은 그중 한 함수로 들어간다. Service 간에 필요한 공통 업무 동작은 Handler로 추출한다. Handler 간 호출은 의존 방향이 명확한 경우에 사용하며 순환 의존은 해소한다. 계층 이름을 위한 전달 함수가 늘어나면 책임 경계를 먼저 재검토한다.

예를 들어 주문 생성은 API의 `create_order`가 Service의 `place_order`를 호출하고, Service가 주문 조건 확인·재고 예약·주문 저장 Handler를 순서대로 실행하는 형태다. 할인 가능 여부와 재고 부족의 업무 판단은 Handler, 재고의 원자적 차감 쿼리와 주문 레코드 저장은 각 Repository가 맡는다.

다른 도메인과 협력할 때는 필요한 공개 Handler와 입력·출력 계약을 명시한다. 호출하는 Service 또는 Handler가 그 계약에 의존하도록 하고, 상대 도메인의 Repository·테이블·내부 ORM 모델 접근은 해당 도메인 안에 둔다. 예를 들어 주문은 재고 도메인의 공개 예약 Handler를 사용한다. 경계를 넘는 호출과 실패 처리 방식은 중요한 설계 결정으로 기록한다. 여러 도메인에서 쓰인다는 이유만으로 업무 정책을 `common`에 옮기지 않는다.

## 트랜잭션·오류·비동기

- Service는 한 유스케이스에서 함께 성공하거나 되돌릴 저장 작업의 범위를 정한다. 트랜잭션 context manager 또는 Unit of Work로 범위를 열고, Handler와 Repository에는 같은 저장 컨텍스트를 주입한다. Service는 SQL·ORM 쿼리를 직접 실행하지 않는다. 이 트랜잭션 추상화의 사용은 허용하며 Repository의 업무 메서드 호출과 구분한다.
- Repository의 쓰기는 바깥 트랜잭션에 참여한다. 여러 단계가 함께 성공해야 하면 각 단계의 독자적인 commit을 피하고, 완료 시 commit·예외 시 rollback하는 주체를 하나로 둔다. 중복·동시 요청의 보장은 DB 제약과 조건부 갱신까지 포함해 확인한다.
- 외부 API와 DB를 함께 쓰면 외부 호출 성공 뒤 저장 실패 같은 부분 실패를 설계한다. 필요한 경우 멱등 키·재시도·보상·outbox 중 실제 요구에 맞는 방법을 선택한다. 여러 저장소의 원자성은 사용하는 기술이 보장하는 범위로 기록한다.
- 예상 가능한 업무 실패는 의미가 있는 오류 타입으로 전달하고 API 경계에서 응답으로 변환한다. 저장소 오류를 성공 값이나 빈 결과로 숨기지 않는다. 예외를 변환할 때 원인을 연결하고, 요청·계정 등 필요한 맥락을 남기되 비밀 값은 제외한다.
- sync/async는 사용하는 I/O 도구에 맞춘다. 비동기 호출은 끝까지 `await`하고, 비동기 요청 경로의 동기 I/O는 해당 프레임워크가 제공하는 실행 경계로 넘긴다. 세션·연결의 생성과 종료를 명시하고, 동시 작업의 공유 가능 여부를 드라이버 기준으로 확인한다.

## 디렉터리 예시

아래는 Python API 애플리케이션에서 필요한 파일을 찾기 위한 예시다. 사용 중인 프레임워크와 기존 배치에 맞춰 조정한다.

```text
app/
  domains/
    orders/
      api.py             요청·응답 경계
      service.py         유스케이스와 트랜잭션 범위
      handlers.py        업무 규칙과 동작
      repository.py      저장·조회
      schemas.py         공개 입력·출력 모델
      models.py          도메인 내부 데이터·저장 모델
    inventory/
      ...
  common/
    database.py          연결·세션·트랜잭션 지원
    errors.py            공통 오류 기반 타입
  integrations/          외부 SDK·API 어댑터
  config.py              설정 로딩과 검증
  dependencies.py        객체 생성과 의존성 연결
  router.py              도메인 라우터 등록
  server.py              애플리케이션 생성과 수명 관리
scripts/                 운영·개발 명령
tests/
  domains/
    orders/              정책·유스케이스·저장·API의 관련 검사
pyproject.toml           프로젝트·개발 도구 설정
uv.lock                  uv를 사용하는 프로젝트의 잠금 파일
```

HTTP 프레임워크 타입과 응답 변환은 API 경계에 둔다. 아래 계층에는 필요한 값과 명시적 입력 모델을 전달하고, ORM 객체를 공개 응답 계약으로 노출하는 대신 필요한 결과 필드로 변환한다. `dependencies.py`는 연결과 객체 구성을 담당하며 정책 판단은 Handler에 둔다. DI 라이브러리와 별도 `run.py`는 프로젝트 실행 방식에 맞춰 선택한다.

도메인에서 사용하는 외부 SDK 연결은 `integrations`에 둘 수 있다. 재사용할 독립 패키지가 생기면 `libs` 등 별도 위치를 검토한다. 업무 규칙은 소유 도메인에 남기고, 설정은 한 곳에서 읽어 필요한 객체에 주입한다.

## Python 코드와 테스트

- 함수와 필드는 업무 의미가 드러나는 이름을 쓴다. 공개 함수·계층 경계의 입력과 반환값에 타입을 표시하고, 누락·빈 값·업무 실패의 의미를 구분한다. 가변 기본 인자와 호출 사이에 공유되는 숨은 상태를 피한다.
- 반복되는 업무 규칙은 소유 Handler에 모은다. 단순한 값 변환은 가까운 위치에 두고, 재사용·교체·검증의 구체적 필요가 생길 때 인터페이스를 추가한다.
- 정책의 정상·실패 조건은 Handler 또는 공개 유스케이스 경계에서 검증한다. Repository의 제약·쿼리·rollback은 실제 테스트 저장소로 확인하고, API는 입력·응답·오류 매핑을 확인한다. 내부 함수 호출 횟수보다 관찰 가능한 결과와 저장 상태를 단언한다.
- TDD 수행자와 리뷰어는 같은 요구·고객 정책·이 가이드의 적용 범위를 받는다. 해당 작업의 타입 검사·lint·format·테스트 명령은 기존 `ImplementationChecks`에 기록한다. 리뷰에서는 도메인 경계·계층 호출·트랜잭션 범위를 직접 대조한다.

## Ruff 설치와 검사

외부에서 이 스킬 묶음을 설치하면 이 문서도 함께 복사된다. Python 개발 도구는 코드를 개발하는 소비 프로젝트의 환경과 의존성 관리 방식에 맞춰 준비한다. 기존 Ruff·Black·Flake8·isort·타입 검사기와 CI를 먼저 읽고, 적용할 도구·설정·범위를 정한다. 기존 formatter가 있으면 해당 명령을 재사용한다.

첫 전체 검사 전에 아래 [설정과 적용 범위](#설정과-적용-범위)를 반영해 설치된 스킬과 생성 산출물을 검사 대상에서 제외한다. 그 뒤 선택한 환경의 설치·검사 명령을 실행한다.

새 Python 프로젝트의 기본 제안은 Ruff의 lint와 formatter다. 설정과 버전은 프로젝트에서 관리한다. 설치가 필요한 것으로 정했으면 준비 단계에서 개발 의존성을 추가하고 실제 검사 명령을 실행한다. 다운로드·권한·환경 실패가 발생하면 명령과 원인을 `not_run`으로 남긴다. Ruff의 검사 범위는 규칙 위반과 형식이며, 타입 검사는 프로젝트의 타입 검사기로, 업무 동작은 테스트로, 계층 준수는 설계·코드 리뷰로 확인한다. [Ruff 설치](https://docs.astral.sh/ruff/installation/) · [Ruff formatter](https://docs.astral.sh/ruff/formatter/)

### uv 프로젝트

`pyproject.toml`이 있는 소비 프로젝트 루트에서 실행한다. 새 프로젝트가 아직 없으면 사용할 디렉터리에서 `uv init --bare`로 초기화한 뒤 진행한다. `uv add --dev`는 개발 의존성을 기록하고, 팀은 `pyproject.toml`과 `uv.lock`을 함께 버전 관리한다. [uv 설치](https://docs.astral.sh/uv/getting-started/installation/) · [개발 의존성](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies)

```bash
uv add --dev ruff
uv run ruff check .
uv run ruff format --check .
```

새 checkout에서는 `uv sync --locked --dev`로 기록된 환경을 준비한 뒤 같은 검사 명령을 사용한다. 기존 프로젝트의 도구 버전 갱신은 해당 프로젝트의 의존성 변경 범위로 다룬다.

### pip와 venv 프로젝트

기존 가상환경을 사용한다. macOS/Linux에서 새 환경이 필요하면 아래처럼 시작할 수 있다. Windows에서는 실행기 경로를 `.venv\Scripts\python.exe`로 바꾼다. 설치한 Ruff 버전은 기존 개발 의존성 파일과 잠금 방식에 반영한다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ruff
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
```

### 설정과 적용 범위

Ruff 설정은 `pyproject.toml`, `ruff.toml`, `.ruff.toml` 중 프로젝트가 실제 사용하는 파일에서 관리한다. 새 프로젝트의 `pyproject.toml`에는 아래 항목을 병합할 수 있다. `requires-python` 또는 Ruff의 `target-version`은 프로젝트가 지원하는 Python 버전에 맞춘다. 아래 검사 대상 제외에는 설치된 스킬과 생성된 워크플로우 산출물을 둔다. 다른 위치에 설치했다면 그 경로도 반영한다. [Ruff 설정](https://docs.astral.sh/ruff/configuration/)

```toml
[tool.ruff]
extend-exclude = [".agents/skills", ".codex/skills", ".workflow"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]
```

이 예시는 오류 가능성이 큰 기본 검사와 import 정리를 사용한다. 줄 길이·따옴표 등은 Ruff 기본 형식에서 시작하고 기존 코드 규약이 있으면 맞춘다. 이미 같은 설정 섹션이 있으면 해당 항목을 편집한다. 별도 `ruff.toml`에는 `[tool.ruff]` 접두어를 제거한 형식이 필요하므로 현재 설정 파일 형식에 맞춰 반영한다.

첫 도입에서는 기존 위반과 이번 변경을 구분해 적용 범위를 정한다. CI가 필수로 검사하는 범위는 그대로 실행해 결과를 기록하고, 대규모 정리는 별도 작업으로 다룬다. 수정이 필요하면 합의한 파일 범위에 `ruff check --fix <경로>`와 `ruff format <경로>`를 실행하고 diff·관련 테스트를 확인한다. 인계 검사는 파일을 변경하지 않는 `ruff check`와 `ruff format --check`를 사용한다. 기존 Black을 사용하는 프로젝트에서는 format 검사를 기존 명령으로 수행한다.

## 워크플로우에서 사용하는 위치

`task-delivery`는 Python 작업 시작 시 적용 규약·개발 환경·검사 명령을 확인해 계획과 현재 작업에 남기고, 구현 수행자에게 이 문서와 해당 범위를 전달한다. `task-design-dialogue`는 중요한 경계·트랜잭션 선택에 사용하고, `task-maps`는 그 책임과 실제 호출을 표시한다. `task-quality-review`는 적용 규약을 읽기 목록에 포함해 설계와 변경 코드를 검토한다. `task-evidence`는 기존 계약에 따라 실제 검사 결과와 리뷰 근거를 인계에 연결한다.
