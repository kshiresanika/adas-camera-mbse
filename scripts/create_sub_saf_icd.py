"""Create the SUB, SAF and ICD documents with their first requirements.

Hierarchy:  STK -> SYS -> SUB -> ICD
                      \\-> SAF

Run from the project root with the venv active:
    python create_sub_saf_icd.py
Then:
    doorstop
    doorstop review all
"""
import subprocess
from pathlib import Path
import yaml

# Each requirement: (text, parent ids, extra attributes)

SUB = [
    ("The Camera Module shall capture images of the forward field of view at a frame rate of TBD fps.",
     ["SYS-001"],
     dict(rationale="A sufficient frame rate is needed to track moving pedestrians.",
          asil="D", verification_method="test",
          component="Camera Module", capella_ref="Capture camera image")),
    ("The Camera Module shall provide each raw image with a timestamp and a frame counter.",
     ["SYS-001", "SYS-007"],
     dict(rationale="Timing and sequence information support tracking, monitoring and logging.",
          asil="D", verification_method="test",
          component="Camera Module", capella_ref="Capture camera image")),
    ("The Image Signal Processor shall convert each raw image to a processed image within TBD ms.",
     ["SYS-001", "SYS-003"],
     dict(rationale="Processing latency is part of the end-to-end AEB response time.",
          asil="D", verification_method="test",
          component="Image Signal Processor", capella_ref="Process image (ISP)")),
    ("The Image Signal Processor shall provide image quality metrics (for example exposure, sharpness and blockage indicators) with every processed image.",
     ["SYS-005"],
     dict(rationale="The perception health monitoring needs objective image quality inputs.",
          asil="B", verification_method="test",
          component="Image Signal Processor", capella_ref="Process image (ISP)")),
    ("The Perception Software shall detect pedestrians in each processed image and output an object list with position and confidence.",
     ["SYS-001"],
     dict(rationale="The object list is the basis for the collision risk estimate.",
          asil="D", verification_method="test",
          component="Perception Software", capella_ref="Detect pedestrians")),
    ("The Perception Software shall estimate the collision risk for each tracked pedestrian.",
     ["SYS-002"],
     dict(rationale="The AEB decision depends on a quantified collision risk.",
          asil="D", verification_method="test",
          component="Perception Software",
          capella_ref="Track pedestrians and predict collision risk")),
    ("The Safety Monitor shall derive a perception health status from the image quality metrics and the plausibility of the detections.",
     ["SYS-005"],
     dict(rationale="Combining both sources detects degradation that either one alone would miss.",
          asil="B", verification_method="test",
          component="Safety Monitor", capella_ref="Monitor perception health")),
    ("The Safety Monitor shall issue an AEB request when the collision risk exceeds the threshold TBD and the perception health status is valid.",
     ["SYS-002"],
     dict(rationale="The request is only trustworthy if the perception behind it is healthy.",
          asil="D", verification_method="test",
          component="Safety Monitor", capella_ref="Decide AEB request")),
    ("The Safety Monitor shall suppress the AEB request when no valid pedestrian detection exists.",
     ["SYS-004"],
     dict(rationale="Avoids unwarranted braking.",
          asil="B", verification_method="test",
          component="Safety Monitor", capella_ref="Decide AEB request")),
    ("The Communication Gateway shall transmit the AEB request and the system state to the vehicle network within TBD ms of the decision.",
     ["SYS-003", "SYS-006"],
     dict(rationale="Gateway latency is part of the end-to-end AEB response time.",
          asil="D", verification_method="test",
          component="Communication Gateway",
          capella_ref="Output status to driver and vehicle")),
    ("The Communication Gateway shall transmit the degraded perception status to the vehicle network for display to the driver.",
     ["SYS-006"],
     dict(rationale="The driver must be informed when the function is limited.",
          asil="B", verification_method="test",
          component="Communication Gateway",
          capella_ref="Output status to driver and vehicle")),
    ("The Diagnostic Manager shall store an event record (timestamp, collision risk, health status, AEB request) for every AEB request and every degraded perception state.",
     ["SYS-007"],
     dict(rationale="Event records enable root-cause analysis.",
          asil="QM", verification_method="demonstration",
          component="Diagnostic Manager", capella_ref="Log diagnostic data")),
    ("The Diagnostic Manager shall provide the stored event records to a connected service tool on request.",
     ["SYS-008"],
     dict(rationale="Service staff need access to the records.",
          asil="QM", verification_method="demonstration",
          component="Diagnostic Manager", capella_ref="Log diagnostic data")),
    ("The Camera Module and the Image Signal Processor shall keep the image quality sufficient for detection in the operating conditions SC-01 to SC-04.",
     ["SYS-009"],
     dict(rationale="Detection performance depends on image quality across lighting and weather.",
          asil="QM", verification_method="test",
          component="Camera Module, Image Signal Processor",
          capella_ref="Capture camera image; Process image (ISP)")),
]

SAF = [
    ("The Safety Monitor shall detect a lost or stale image stream within TBD ms and treat it as degraded perception.",
     ["SYS-005"],
     dict(rationale="A frozen image looks valid to the detection but hides pedestrians.",
          asil="B", verification_method="test",
          component="Safety Monitor", capella_ref="Monitor perception health")),
    ("The system shall enter a defined safe state (AEB request inhibited, driver informed) when a failure of the Perception Software or the Safety Monitor is detected.",
     ["SYS-004", "SYS-006"],
     dict(rationale="Assumed safe state is fail-silent with driver notification; to be confirmed by a HARA.",
          asil="D", verification_method="test",
          component="Safety Monitor", capella_ref="Monitor perception health")),
    ("The Safety Monitor shall validate the output of the Perception Software with an independent plausibility check before issuing an AEB request.",
     ["SYS-004", "SYS-010"],
     dict(rationale="Independence limits common-cause failures between detection and decision.",
          asil="D", verification_method="analysis",
          component="Safety Monitor", capella_ref="Decide AEB request")),
    ("The Communication Gateway shall protect the AEB request message with a CRC and an alive counter.",
     ["SYS-002", "SYS-010"],
     dict(rationale="Corrupted or repeated messages must not trigger or hide a brake request.",
          asil="D", verification_method="test",
          component="Communication Gateway",
          capella_ref="Output status to driver and vehicle")),
    ("The safety-related components shall be developed according to ISO 26262 for their allocated ASIL.",
     ["SYS-010"],
     dict(rationale="Process compliance is part of the safety argument.",
          asil="n/a", verification_method="analysis",
          component="all safety-related components", capella_ref="all logical functions")),
]

ICD = [
    ("The Camera Module shall provide the raw image to the Image Signal Processor with resolution TBD, frame rate TBD, pixel format TBD, timestamp and frame counter.",
     ["SUB-001", "SUB-002"],
     dict(rationale="Fixes the first interface of the image chain.",
          asil="D", verification_method="inspection",
          component="Camera Module -> Image Signal Processor", capella_ref="raw image")),
    ("The Image Signal Processor shall provide the processed image to the Perception Software with format TBD and a maximum latency of TBD ms.",
     ["SUB-003", "SUB-005"],
     dict(rationale="Fixes the interface that feeds the detection.",
          asil="D", verification_method="inspection",
          component="Image Signal Processor -> Perception Software",
          capella_ref="processed image")),
    ("The Image Signal Processor shall provide the image quality metrics to the Safety Monitor with every frame, with content TBD.",
     ["SUB-004", "SUB-007"],
     dict(rationale="Fixes the interface that feeds the health monitoring.",
          asil="B", verification_method="inspection",
          component="Image Signal Processor -> Safety Monitor",
          capella_ref="image quality metrics")),
    ("The Perception Software shall provide the collision risk per tracked pedestrian to the Safety Monitor with cycle time TBD ms.",
     ["SUB-006", "SUB-008"],
     dict(rationale="Fixes the interface between detection and decision.",
          asil="D", verification_method="inspection",
          component="Perception Software -> Safety Monitor",
          capella_ref="collision risk")),
    ("The Safety Monitor shall provide the AEB request, the system state and the degradation status to the Communication Gateway with cycle time TBD ms and content TBD.",
     ["SUB-008", "SUB-010", "SUB-011"],
     dict(rationale="Fixes the safety-critical output interface.",
          asil="D", verification_method="inspection",
          component="Safety Monitor -> Communication Gateway",
          capella_ref="AEB request and system state; degradation status")),
    ("The Safety Monitor shall provide event data (AEB event, degraded state) to the Diagnostic Manager with content TBD.",
     ["SUB-012"],
     dict(rationale="Fixes the interface that feeds the event records.",
          asil="QM", verification_method="inspection",
          component="Safety Monitor -> Diagnostic Manager",
          capella_ref="AEB event; degraded state")),
]


def doorstop(*args):
    subprocess.run(["doorstop", *args], check=True)


def build(prefix, folder, parent, reqs):
    path = Path("reqs") / folder
    if not path.exists():
        doorstop("create", prefix, str(path), "--parent", parent, "--separator", "-")
    if any(path.glob(f"{prefix}-*.yml")):
        print(f"{prefix} items already exist - skipping so nothing is duplicated.")
        return
    for i, (text, parents, extra) in enumerate(reqs, start=1):
        uid = f"{prefix}-{i:03d}"
        doorstop("add", prefix)
        item = path / f"{uid}.yml"
        data = yaml.safe_load(item.read_text(encoding="utf-8")) or {}
        data["text"] = text
        data.update(extra)
        item.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        for p in parents:
            doorstop("link", uid, p)
        print(f"created {uid} -> {', '.join(parents)}")


def main():
    build("SUB", "sub", "SYS", SUB)
    build("SAF", "saf", "SYS", SAF)
    build("ICD", "icd", "SUB", ICD)


if __name__ == "__main__":
    main()
