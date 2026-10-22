# Architecture Overview

## Units

| Unit | Responsibility | Entry point | Evidence |
| --- | --- | --- | --- |
| api | serve widget reads | `src/widget.py` | `src/widget.py` |

## Dependencies And Contracts

| From | To | Contract | Evidence | Verification state |
| --- | --- | --- | --- | --- |
| api | store | JSON records | `src/widget.py` | statically traced |

## Representative Flows

1. HTTP GET `/widgets` -> `api.list_widgets` -> JSON array (evidence: `src/widget.py`)

## Intended Versus Actual

| Relationship | Intended | Actual | Disposition |
| --- | --- | --- | --- |
| export -> CSV writer | [../specs/widget-export.md](../specs/widget-export.md) | absent | planned-absent |

## 9. API 설계 (FastAPI)

HTTP 표면은 `src/widget.py`가 정의한다. 이 제목은 한국어 앵커 해결을 검증한다.

## T-603. 웹 UI

웹 UI는 아직 없다. 계획만 존재한다.

## 9.6 바인딩과 서비스 소유권

소유권은 확립되지 않았다 (`Not established`).

## 반복되는 제목

첫 번째 등장.

## 반복되는 제목

두 번째 등장. 링크는 `-1` 접미사로 도달한다.

<a id="owner-table"></a>

## 소유자 표

작성자가 직접 선언한 앵커로 도달하는 구획이다.
