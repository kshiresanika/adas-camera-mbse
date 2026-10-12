# Scope Statement: ADAS Camera Processing and Safety Monitoring System

Project: ADAS camera perception and safety monitoring (MBSE and requirements engineering)
Baseline: 0.1 (draft)

## System of interest

The system of interest is the camera-based perception and safety monitoring chain, consisting of the camera, the image signal processor (ISP), the SoC and the ECU. It detects pedestrians in the vehicle's forward path and issues an automatic emergency braking (AEB) trigger request to the vehicle. It also monitors its own perception quality and reports degraded states (for example a blinded or dirty camera) to the driver and the vehicle.

## Out of scope

- Brake actuation (the system issues a request only)
- Vehicle dynamics and control
- Maps and localization

## Stakeholders

- Driver
- Vehicle program
- Safety assessor
- Homologation
- Service
- Cybersecurity

## Assumptions

- ASIL ratings are assumed for this project. They are not the result of a full hazard analysis and risk assessment (HARA).
- No real vehicle data is used.
- Inputs are simulated or recorded only.

## Standards referenced

- ISO 26262 (functional safety)
- ISO 21448 (SOTIF)
- ASPICE SYS.1 to SYS.5 and SWE.1 to SWE.6
