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
| export -> CSV writer | `Not established` | absent | planned-absent |
