# Coverage report (2026-10-17)

## Summary per document

| Document | Items | COVERED | PARTIAL | GAP | NON-TEST |
|---|---|---|---|---|---|
| STK | 6 | 1 | 3 | 1 | 1 |
| SYS | 10 | 4 | 4 | 1 | 1 |
| SUB | 14 | 9 | 0 | 5 | 0 |
| SAF | 5 | 3 | 0 | 0 | 2 |
| ICD | 6 | 0 | 0 | 0 | 6 |
| SWR | 15 | 15 | 0 | 0 | 0 |
| TST | 17 | 17 | 0 | 0 | 0 |

## Gaps (no test case reachable)

- **STK-006**: The system shall operate across defined lighting and weather conditions (day, night, low sun, rain).
- **SYS-009**: The system shall meet its detection and monitoring requirements in the operating conditions SC-01 to SC-04.
- **SUB-001**: The Camera Module shall capture images of the forward field of view at a frame rate of TBD fps.
- **SUB-002**: The Camera Module shall provide each raw image with a timestamp and a frame counter.
- **SUB-003**: The Image Signal Processor shall convert each raw image to a processed image within TBD ms.
- **SUB-004**: The Image Signal Processor shall provide image quality metrics (for example exposure, sharpness and blockage i
- **SUB-014**: The Camera Module and the Image Signal Processor shall keep the image quality sufficient for detection in the 

## Partially covered

- **STK-001**: The driver shall be protected from collisions with pedestrians in urban driving through automatic braking inte
- **STK-003**: The system shall detect degraded perception (e.g. blinded or dirty camera) and inform the driver and the vehic
- **STK-004**: The system shall support post-event diagnosis through logged data and traceable fault information.
- **SYS-001**: The system shall detect pedestrians in the forward field of view of the vehicle.
- **SYS-003**: The system shall issue the AEB request within TBD ms after the collision risk exceeds the threshold.
- **SYS-005**: The system shall detect a blinded, dirty or faulty camera.
- **SYS-007**: The system shall log diagnostic data for every AEB request and every degraded perception state.

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
| STK-001 | PARTIAL | test |
| STK-002 | COVERED | test |
| STK-003 | PARTIAL | test |
| STK-004 | PARTIAL | demonstration |
| STK-005 | NON-TEST | analysis |
| STK-006 | GAP | test |
| SYS-001 | PARTIAL | test |
| SYS-002 | COVERED | test |
| SYS-003 | PARTIAL | test |
| SYS-004 | COVERED | test |
| SYS-005 | PARTIAL | test |
| SYS-006 | COVERED | test |
| SYS-007 | PARTIAL | demonstration |
| SYS-008 | COVERED | demonstration |
| SYS-009 | GAP | test |
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

ICD: 6, SAF: 1, SUB: 4, SWR: 6, SYS: 3, TST: 2

## Test execution

17 test cases planned, 0 with a recorded result.
