# Coverage report (2026-10-17)

## Summary per document

| Document | Items | COVERED | PARTIAL | GAP | NON-TEST |
|---|---|---|---|---|---|
| STK | 6 | 5 | 0 | 0 | 1 |
| SYS | 10 | 9 | 0 | 0 | 1 |
| SUB | 14 | 14 | 0 | 0 | 0 |
| SAF | 5 | 3 | 0 | 0 | 2 |
| ICD | 6 | 0 | 0 | 0 | 6 |
| SWR | 21 | 21 | 0 | 0 | 0 |
| TST | 23 | 23 | 0 | 0 | 0 |

## Gaps (no test case reachable)

None.

## Partially covered

None.

## Verified outside the test plan (analysis or inspection)

- **STK-005** (analysis): The system shall meet the applicable functional safety requirements (ISO 26262) for its intended use.
- **SYS-010** (analysis): The system shall be developed in accordance with ISO 26262 for the ASIL allocated to each function.
- **SAF-003** (analysis): The Safety Monitor shall validate the output of the Perception Software with an independent plausibility check
- **SAF-005** (analysis): The safety-related components shall be developed according to ISO 26262 for their allocated ASIL.
- **ICD-001** (inspection): The Camera Module shall provide the raw image to the Image Signal Processor with resolution TBD, frame rate TB
- **ICD-002** (inspection): The Image Signal Processor shall provide the processed image to the Perception Software with format TBD and a 
- **ICD-003** (inspection): The Image Signal Processor shall provide the image quality metrics to the Safety Monitor with every frame, wit
- **ICD-004** (inspection): The Perception Software shall provide the collision risk per tracked pedestrian to the Safety Monitor with cyc
- **ICD-005** (inspection): The Safety Monitor shall provide the AEB request, the system state and the degradation status to the Communica
- **ICD-006** (inspection): The Safety Monitor shall provide event data (AEB event, degraded state) to the Diagnostic Manager with content

## Status of stakeholder, system and safety requirements

| ID | Status | Verification method |
|---|---|---|
| STK-001 | COVERED | test |
| STK-002 | COVERED | test |
| STK-003 | COVERED | test |
| STK-004 | COVERED | demonstration |
| STK-005 | NON-TEST | analysis |
| STK-006 | COVERED | test |
| SYS-001 | COVERED | test |
| SYS-002 | COVERED | test |
| SYS-003 | COVERED | test |
| SYS-004 | COVERED | test |
| SYS-005 | COVERED | test |
| SYS-006 | COVERED | test |
| SYS-007 | COVERED | demonstration |
| SYS-008 | COVERED | demonstration |
| SYS-009 | COVERED | test |
| SYS-010 | NON-TEST | analysis |
| SAF-001 | COVERED | test |
| SAF-002 | COVERED | test |
| SAF-003 | NON-TEST | analysis |
| SAF-004 | COVERED | test |
| SAF-005 | NON-TEST | analysis |

## Link problems

No items without a parent link.

No links to missing items.

## Open points (TBD in the requirement text)

ICD: 6, SAF: 1, SUB: 4, SWR: 8, SYS: 3, TST: 3

## Test execution

23 test cases planned, 0 with a recorded result.
