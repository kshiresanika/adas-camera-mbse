"""Create the SWR document with the first software requirements.

Hierarchy:  STK -> SYS -> SUB -> SWR
Safety requirements (SAF) are referenced through the attribute 'saf_ref';
the coverage script in a later step checks that every SAF item is covered.

Run from the project root with the venv active:
    python create_swr.py
Then:
    doorstop
    doorstop review all
"""
import subprocess
from pathlib import Path
import yaml

SWR_DIR = Path("reqs") / "swr"

# (text, parent SUB ids, extra attributes)
REQS = [
    ("The Pedestrian Detector shall process every processed image and output pedestrian objects with bounding box, distance estimate and a confidence between 0 and 1.",
     ["SUB-005"],
     dict(software_unit="Pedestrian Detector", component="Perception Software",
          asil="D", verification_method="test", saf_ref="")),
    ("The Pedestrian Detector shall complete the processing of each image within TBD ms.",
     ["SUB-005"],
     dict(software_unit="Pedestrian Detector", component="Perception Software",
          asil="D", verification_method="test", saf_ref="")),
    ("The Object Tracker shall maintain a track identifier for each pedestrian across consecutive frames and estimate its velocity.",
     ["SUB-006"],
     dict(software_unit="Object Tracker", component="Perception Software",
          asil="D", verification_method="test", saf_ref="")),
    ("The Collision Risk Estimator shall compute the time to collision for each track and map it to a risk value between 0 and 1.",
     ["SUB-006"],
     dict(software_unit="Collision Risk Estimator", component="Perception Software",
          asil="D", verification_method="test", saf_ref="")),
    ("The Health Monitor shall evaluate the image quality metrics of every frame against the thresholds TBD and set a blockage or blur flag when a threshold is violated.",
     ["SUB-007"],
     dict(software_unit="Health Monitor", component="Safety Monitor",
          asil="B", verification_method="test", saf_ref="")),
    ("The Health Monitor shall set the perception health status to degraded after TBD consecutive frames with a failed image quality check.",
     ["SUB-007"],
     dict(software_unit="Health Monitor", component="Safety Monitor",
          asil="B", verification_method="test", saf_ref="")),
    ("The Health Monitor shall set the perception health status to degraded when no new frame counter value has been received for TBD ms.",
     ["SUB-007"],
     dict(software_unit="Health Monitor", component="Safety Monitor",
          asil="B", verification_method="test", saf_ref="SAF-001")),
    ("The Plausibility Checker shall check each detection against an independent criterion (for example size-distance consistency) and flag implausible detections.",
     ["SUB-009"],
     dict(software_unit="Plausibility Checker", component="Safety Monitor",
          asil="D", verification_method="test", saf_ref="SAF-003")),
    ("The AEB Decision Logic shall set the AEB request active when the collision risk is at least TBD, the perception health status is valid and the detection is plausible.",
     ["SUB-008"],
     dict(software_unit="AEB Decision Logic", component="Safety Monitor",
          asil="D", verification_method="test", saf_ref="")),
    ("The AEB Decision Logic shall keep the AEB request inactive when no valid pedestrian detection exists.",
     ["SUB-009"],
     dict(software_unit="AEB Decision Logic", component="Safety Monitor",
          asil="B", verification_method="test", saf_ref="")),
    ("The Safe State Manager shall set the AEB request inactive and raise a driver warning when an internal fault of the Perception Software or the Safety Monitor is detected.",
     ["SUB-009", "SUB-011"],
     dict(software_unit="Safe State Manager", component="Safety Monitor",
          asil="D", verification_method="test", saf_ref="SAF-002")),
    ("The Message Handler shall append a CRC and increment an alive counter in every AEB request message.",
     ["SUB-010"],
     dict(software_unit="Message Handler", component="Communication Gateway",
          asil="D", verification_method="test", saf_ref="SAF-004")),
    ("The Message Handler shall send the degraded perception status to the vehicle network with a cycle time of TBD ms.",
     ["SUB-011"],
     dict(software_unit="Message Handler", component="Communication Gateway",
          asil="B", verification_method="test", saf_ref="")),
    ("The Event Logger shall write an event record to non-volatile memory for every AEB request and every degraded perception state.",
     ["SUB-012"],
     dict(software_unit="Event Logger", component="Diagnostic Manager",
          asil="QM", verification_method="test", saf_ref="")),
    ("The Event Logger shall return the stored event records over the diagnostic protocol on request of a service tool.",
     ["SUB-013"],
     dict(software_unit="Event Logger", component="Diagnostic Manager",
          asil="QM", verification_method="test", saf_ref="")),
]


def doorstop(*args):
    subprocess.run(["doorstop", *args], check=True)


def main():
    if not SWR_DIR.exists():
        doorstop("create", "SWR", str(SWR_DIR), "--parent", "SUB", "--separator", "-")
    if any(SWR_DIR.glob("SWR-*.yml")):
        print("SWR items already exist - stopping so nothing is duplicated.")
        return
    for i, (text, parents, extra) in enumerate(REQS, start=1):
        uid = f"SWR-{i:03d}"
        doorstop("add", "SWR")
        path = SWR_DIR / f"{uid}.yml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data["text"] = text
        data.update(extra)
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        for p in parents:
            doorstop("link", uid, p)
        print(f"created {uid} -> {', '.join(parents)}")


if __name__ == "__main__":
    main()
