"""Create the TST document with the planned test cases.

Hierarchy:  STK -> SYS -> SUB -> SWR -> TST

Run from the project root with the venv active:
    python create_tst.py
Then:
    doorstop
    doorstop review all
"""
import subprocess
from pathlib import Path
import yaml

TST_DIR = Path("reqs") / "tst"

# (test description, parent SWR ids, extra attributes)
REQS = [
    ("Run the Pedestrian Detector on recorded clips of an adult crossing in daylight and check the output object fields.",
     ["SWR-001"],
     dict(test_level="unit", environment="SIL", scenario="SC-01",
          pass_criteria="Detection rate of at least TBD percent; every object has bounding box, distance and a confidence between 0 and 1.")),
    ("Run the Pedestrian Detector on recorded night clips with a pedestrian in dark clothing and check the output object fields.",
     ["SWR-001"],
     dict(test_level="unit", environment="SIL", scenario="SC-03",
          pass_criteria="Detection rate of at least TBD percent; every object has bounding box, distance and a confidence between 0 and 1.")),
    ("Measure the processing time of the Pedestrian Detector over a long recorded sequence.",
     ["SWR-002"],
     dict(test_level="software integration", environment="HIL", scenario="SC-01",
          pass_criteria="Maximum processing time per image is below TBD ms.")),
    ("Feed a sequence with a pedestrian crossing and a child emerging from occlusion into the Object Tracker.",
     ["SWR-003"],
     dict(test_level="unit", environment="SIL", scenario="SC-01, SC-02",
          pass_criteria="Track identifier stays constant for TBD percent of the frames; velocity error below TBD m/s.")),
    ("Feed known distances and speeds into the Collision Risk Estimator and compare the risk output with the expected mapping.",
     ["SWR-004"],
     dict(test_level="unit", environment="SIL", scenario="SC-01, SC-02",
          pass_criteria="Risk value is between 0 and 1 and matches the reference mapping within TBD.")),
    ("Inject frames with blur and with a blocked lens into the Health Monitor.",
     ["SWR-005"],
     dict(test_level="unit", environment="SIL", scenario="SC-04",
          pass_criteria="Blur or blockage flag is set for every injected frame that violates a threshold and for no clean frame.")),
    ("Inject TBD consecutive frames with a failed image quality check.",
     ["SWR-006"],
     dict(test_level="software integration", environment="SIL", scenario="SC-04",
          pass_criteria="Perception health status changes to degraded after exactly TBD frames and not earlier.")),
    ("Stop the frame counter updates for TBD ms.",
     ["SWR-007"],
     dict(test_level="software integration", environment="HIL", scenario="SC-04",
          pass_criteria="Perception health status changes to degraded within TBD ms of the last valid frame.")),
    ("Inject a detection with an inconsistent size and distance into the Plausibility Checker.",
     ["SWR-008"],
     dict(test_level="unit", environment="SIL", scenario="SC-03",
          pass_criteria="The detection is flagged as implausible; consistent detections are not flagged.")),
    ("Provide a collision risk above the threshold with valid health and a plausible detection.",
     ["SWR-009"],
     dict(test_level="system", environment="SIL", scenario="SC-01, SC-02",
          pass_criteria="AEB request becomes active within TBD ms.")),
    ("Provide a collision risk above the threshold while the perception health status is degraded.",
     ["SWR-009"],
     dict(test_level="system", environment="SIL", scenario="SC-04",
          pass_criteria="AEB request stays inactive and the degraded status is reported.")),
    ("Run a sequence without any pedestrian in the field of view.",
     ["SWR-010"],
     dict(test_level="system", environment="SIL", scenario="all (no pedestrian)",
          pass_criteria="AEB request stays inactive for the whole sequence.")),
    ("Inject a fault into the Perception Software and into the Safety Monitor in turn.",
     ["SWR-011"],
     dict(test_level="system", environment="HIL", scenario="SC-01",
          pass_criteria="AEB request is set inactive and the driver warning is raised within TBD ms of the fault.")),
    ("Check the CRC and the alive counter of AEB request messages, then corrupt and repeat messages at the receiver.",
     ["SWR-012"],
     dict(test_level="software integration", environment="HIL", scenario="SC-01",
          pass_criteria="Valid messages are accepted; corrupted and repeated messages are rejected.")),
    ("Measure the cycle time of the degraded status message on the vehicle network.",
     ["SWR-013"],
     dict(test_level="software integration", environment="HIL", scenario="SC-04",
          pass_criteria="Cycle time equals TBD ms with a tolerance of TBD ms.")),
    ("Trigger an AEB request and a degraded state, then power-cycle the system and read the memory.",
     ["SWR-014"],
     dict(test_level="software integration", environment="HIL", scenario="SC-01, SC-04",
          pass_criteria="One event record per trigger exists after the power cycle with complete content.")),
    ("Read the stored event records from a connected service tool over the diagnostic protocol.",
     ["SWR-015"],
     dict(test_level="system", environment="HIL", scenario="SC-01, SC-04",
          pass_criteria="All stored records are returned unchanged and completely.")),
]


def doorstop(*args):
    subprocess.run(["doorstop", *args], check=True)


def main():
    if not TST_DIR.exists():
        doorstop("create", "TST", str(TST_DIR), "--parent", "SWR", "--separator", "-")
    if any(TST_DIR.glob("TST-*.yml")):
        print("TST items already exist - stopping so nothing is duplicated.")
        return
    for i, (text, parents, extra) in enumerate(REQS, start=1):
        uid = f"TST-{i:03d}"
        doorstop("add", "TST")
        path = TST_DIR / f"{uid}.yml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data["text"] = text
        data.update(extra)
        data["status"] = "planned"
        data["result"] = ""
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        for p in parents:
            doorstop("link", uid, p)
        print(f"created {uid} -> {', '.join(parents)}")


if __name__ == "__main__":
    main()
