"""Create the SYS document (if missing) and add the first system requirements.

Run from the project root with the venv active:
    python create_sys.py
Then:
    doorstop
    doorstop review all
"""
import subprocess
from pathlib import Path
import yaml

SYS_DIR = Path("reqs") / "sys"

# (text, parent STK ids, extra attributes)
REQS = [
    ("The system shall detect pedestrians in the forward field of view of the vehicle.",
     ["STK-001"],
     dict(rationale="Detection is the precondition for any pedestrian protection.",
          asil="D", verification_method="test",
          capella_ref="Detect pedestrians", scenarios="SC-01, SC-02, SC-03")),
    ("The system shall request AEB when the predicted collision risk exceeds the threshold TBD.",
     ["STK-001"],
     dict(rationale="The AEB request is the system's main safety output.",
          asil="D", verification_method="test",
          capella_ref="Decide AEB request", scenarios="SC-01, SC-02, SC-03")),
    ("The system shall issue the AEB request within TBD ms after the collision risk exceeds the threshold.",
     ["STK-001"],
     dict(rationale="Braking late reduces or removes the benefit of the intervention.",
          asil="D", verification_method="test",
          capella_ref="Decide AEB request", scenarios="SC-01, SC-02")),
    ("The system shall not issue an AEB request when no valid pedestrian detection exists.",
     ["STK-002"],
     dict(rationale="Unwarranted braking can cause accidents and erodes driver trust.",
          asil="B", verification_method="test",
          capella_ref="Decide AEB request", scenarios="SC-03, SC-04")),
    ("The system shall detect a blinded, dirty or faulty camera.",
     ["STK-003"],
     dict(rationale="Degraded images silently reduce detection performance.",
          asil="B", verification_method="test",
          capella_ref="Monitor perception health", scenarios="SC-04")),
    ("The system shall report degraded perception to the driver and the vehicle network within TBD ms of detecting it.",
     ["STK-003"],
     dict(rationale="The driver and the vehicle must know when the function is limited.",
          asil="B", verification_method="test",
          capella_ref="Output status to driver and vehicle", scenarios="SC-04")),
    ("The system shall log diagnostic data for every AEB request and every degraded perception state.",
     ["STK-004"],
     dict(rationale="Logged data supports root-cause analysis after incidents.",
          asil="QM", verification_method="demonstration",
          capella_ref="Log diagnostic data", scenarios="")),
    ("The system shall provide the logged diagnostic data to a connected service tool.",
     ["STK-004"],
     dict(rationale="Service staff need access to the data for fault analysis.",
          asil="QM", verification_method="demonstration",
          capella_ref="Log diagnostic data", scenarios="")),
    ("The system shall meet its detection and monitoring requirements in the operating conditions SC-01 to SC-04.",
     ["STK-006"],
     dict(rationale="The function must work in realistic lighting and weather conditions.",
          asil="QM", verification_method="test",
          capella_ref="Detect pedestrians", scenarios="SC-01, SC-02, SC-03, SC-04")),
    ("The system shall be developed in accordance with ISO 26262 for the ASIL allocated to each function.",
     ["STK-005"],
     dict(rationale="Safety-related functions require a compliant development process.",
          asil="n/a", verification_method="analysis",
          capella_ref="all system functions", scenarios="")),
]


def doorstop(*args):
    subprocess.run(["doorstop", *args], check=True)


def main():
    if not SYS_DIR.exists():
        doorstop("create", "SYS", str(SYS_DIR), "--parent", "STK", "--separator", "-")
    if any(SYS_DIR.glob("SYS-*.yml")):
        print("SYS items already exist - stopping so nothing is duplicated.")
        return

    for i, (text, parents, extra) in enumerate(REQS, start=1):
        uid = f"SYS-{i:03d}"
        doorstop("add", "SYS")
        path = SYS_DIR / f"{uid}.yml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data["text"] = text
        data.update(extra)
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        for parent in parents:
            doorstop("link", uid, parent)
        print(f"created {uid} -> {', '.join(parents)}")


if __name__ == "__main__":
    main()
