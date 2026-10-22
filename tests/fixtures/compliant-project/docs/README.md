# Documentation Index

| Area | Path | Holds |
| --- | --- | --- |
| Project overview | [project.md](project.md) | purpose, scope, status, commands |
| Architecture | [architecture/overview.md](architecture/overview.md) | units and flows |
| Specifications | [specs/widget-export.md](specs/widget-export.md) | required behavior |
| Plans | [plans/README.md](plans/README.md) | plan lifecycle |

Empty categories carry no placeholder file: decisions, guides, verification, archive.

Canonical commands live in [project.md](project.md#canonical-commands).

## Authoritative Sources

| Source | Canonical home | Why it stays there |
| --- | --- | --- |
| [`DESIGN.md`](../DESIGN.md) | this source | `tests/test_page.py` reads it by path; moving it fails the suite |
| [`README.md`](../README.md) | this source | the distribution surface publishes it from the repository root |
| `doc/legacy-notes.md` | [architecture/overview.md](architecture/overview.md) | moved: source removed, boundary notes carried across |

## Unresolved

| Item | Why it is open | Who decides |
| --- | --- | --- |
| CSV export is unimplemented | [specs/widget-export.md](specs/widget-export.md) records the gap; no handler exists | `Not established` |

## 국문 문서 색인

한국어 제목이 실제로 앵커로 해결되는지 확인하는 구획이다. 아래 링크는 모두 같은 문서를 가리킨다.

- [9. API 설계 (FastAPI)](architecture/overview.md#9-api-설계-fastapi)
- [퍼센트 인코딩된 같은 제목](architecture/overview.md#9-api-%EC%84%A4%EA%B3%84-fastapi)
- [T-603. 웹 UI](architecture/overview.md#t-603-웹-ui)
- [9.6 바인딩과 서비스 소유권](architecture/overview.md#96-바인딩과-서비스-소유권)
- [두 번째 같은 제목](architecture/overview.md#반복되는-제목-1)
- [명시적 HTML 앵커](architecture/overview.md#owner-table)
