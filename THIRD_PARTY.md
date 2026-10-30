# 공개 스킬의 출처와 라이선스

고정한 공식 저장소에서 스킬 폴더 전체를 복사했습니다. 모든 upstream 파일은 원문 그대로이며 파일별 SHA-256은 [dependencies.lock.json](dependencies.lock.json)에 기록했습니다. 각 스킬 폴더에 원저자의 LICENSE를 포함합니다.

| 스킬 | 공식 원문 | 고정 커밋 | 라이선스 |
|---|---|---|---|
| to-tickets | [공식 폴더](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/to-tickets) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | [MIT](skills/to-tickets/LICENSE) |
| tdd | [공식 폴더](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/tdd) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | [MIT](skills/tdd/LICENSE) |
| codebase-design | [공식 폴더](https://github.com/mattpocock/skills/tree/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/engineering/codebase-design) | `59db609eb1e18aaf59b63284d0e52255aff0c63c` | [MIT](skills/codebase-design/LICENSE) |
| mermaid-diagrams | [공식 폴더](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/mermaid-diagrams) | `3027f20f3181758385a1bb8c022d4041dfb4de84` | [MIT](skills/mermaid-diagrams/LICENSE) |
| visual-explainer | [공식 폴더](https://github.com/nicobailon/visual-explainer/tree/5f378868e0ea745a6284b51e710c390f0c76f72c/plugins/visual-explainer) | `5f378868e0ea745a6284b51e710c390f0c76f72c` | [MIT](skills/visual-explainer/LICENSE) |
| simple-english | [공식 폴더](https://github.com/AminBlg/SimpleEnglish/tree/a6fcb4fde098b33617cc1578d151ebf58774b883/skills/simple-english) | `a6fcb4fde098b33617cc1578d151ebf58774b883` | [MIT](skills/simple-english/LICENSE) |

## 패키지에서 추가한 부분

- `task-delivery`, `task-design-dialogue`, `task-maps`, `task-evidence`와 공통 계약·과제 양식은 이 패키지의 협업 절차입니다. 설계 대화의 질문 순서에는 Matt Pocock `grilling`의 결정 의존관계 방식을 참고했으며 원문 파일은 복사하지 않았습니다.
- visual-explainer에 HTML 렌더링용 `package.json`과 `package-lock.json`을 추가했습니다. Playwright Core 1.64.1을 고정하며 기존 원문 파일은 수정하지 않았습니다. 영상·슬라이드·MCP의 추가 의존성은 해당 원문 지침을 따릅니다.
- visual-explainer에 포함된 PELE 자원의 라이선스는 [PELE-LICENSE](skills/visual-explainer/kit/vendor/PELE-LICENSE)를 보존했습니다. Node 의존성의 라이선스는 npm 패키지에 포함됩니다.
- `to-tickets`의 분해 기준은 로컬 어댑터로 적용합니다. 공개 원문의 게시 절차·트래커 설정을 자동으로 실행하지 않습니다.
- `simple-english`는 영어 기술 문서 스킬 원문과 참조 파일만 포함합니다. 한국어 문서에는 원문의 명료성 원칙을 참고하는 패키지 어댑터를 적용하며 영어 문법·단어 수를 그대로 강제하지 않습니다. 원격 저장소의 세션 훅과 출력 스타일은 포함하지 않습니다.

## 업데이트

공식 커밋과 스킬 폴더·LICENSE를 함께 갱신하고 파일 해시를 다시 기록합니다. `scripts/check.py`와 설치 검사를 실행하고 공통 계약의 호출자에 미치는 영향을 검토합니다.
