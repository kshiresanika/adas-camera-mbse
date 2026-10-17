"""Close the verification gaps of the camera and ISP chain.

Adds SWR-016 .. SWR-021 (linked to SUB-001 .. SUB-004 and SUB-014) and
TST-018 .. TST-023 (linked to the new SWR items).

Run from the project root with the venv active:
    python create_gap_closure.py
Then:
    python trace_report.py
    doorstop
    doorstop review all
"""
import subprocess
from pathlib import Path
import yaml

SWR_DIR = Path("reqs") / "swr"
TST_DIR = Path("reqs") / "tst"

# (text, parent SUB ids, extra attributes)
NEW_SWR = [
    ("The Camera Driver shall configure the image sensor at start-up to the frame rate TBD fps and verify the configuration by reading back the sensor registers.",
     ["SUB-001"],
     dict(software_unit="Camera Driver", component="Camera Module",
          asil="D", verification_method="test", saf_ref="")),
    ("The Camera Driver shall add a timestamp and a frame counter to every frame before it is passed on.",
     ["SUB-002"],
     dict(software_unit="Camera Driver", component="Camera Module",
          asil="D", verification_method="test", saf_ref="SAF-001")),
    ("The ISP Pipeline Configurator shall load the tuned ISP parameter set that matches the active lighting condition (day, night, low sun).",
     ["SUB-003"],
     dict(software_unit="ISP Pipeline Configurator", component="Image Signal Processor",
          asil="D", verification_method="test", saf_ref="")),
    ("The ISP Pipeline Configurator shall complete the conversion of each raw image within TBD ms.",
     ["SUB-003"],
     dict(software_unit="ISP Pipeline Configurator", component="Image Signal Processor",
          asil="D", verification_method="test", saf_ref="")),
    ("The ISP Pipeline Configurator shall compute exposure, sharpness and blockage indicators for every processed image and attach them as image quality metrics.",
     ["SUB-004"],
     dict(software_unit="ISP Pipeline Configurator", component="Image Signal Processor",
          asil="B", verification_method="test", saf_ref="")),
    ("The Exposure Control shall adapt exposure and gain so that the pedestrian region stays within the usable brightness range in the operating conditions SC-01 to SC-04.",
     ["SUB-014"],
     dict(software_unit="Exposure Control", component="Image Signal Processor",
          asil="QM", verification_method="test", saf_ref="")),
]

# (test description, index of the new SWR item (1-based), extra attributes)
NEW_TST = [
    ("Start the camera and read back the sensor registers, then measure the frame rate over one minute.",
     1,
     dict(test_level="software integration", environment="HIL", scenario="SC-01",
          pass_criteria="Register read-back equals the configured values; frame rate equals TBD fps with a tolerance of TBD.")),
    ("Record a ten-minute stream and check the timestamps and the frame counter of every frame.",
     2,
     dict(test_level="software integration", environment="HIL", scenario="SC-01",
          pass_criteria="Timestamps increase monotonically; the frame counter increases by one per frame.")),
    ("Change the lighting in a light chamber between day, night and low sun and read the active ISP parameter set.",
     3,
     dict(test_level="software integration", environment="bench", scenario="SC-01, SC-03, SC-04",
          pass_criteria="The parameter set matching each lighting condition is active within TBD s of the change.")),
    ("Measure the conversion time of the Image Signal Processor for every frame of a long sequence.",
     4,
     dict(test_level="software integration", environment="HIL", scenario="SC-01",
          pass_criteria="Maximum conversion time is below TBD ms.")),
    ("Feed reference charts (sharp, blurred, blocked) into the ISP and compare the image quality metrics with the reference values.",
     5,
     dict(test_level="software integration", environment="bench", scenario="SC-04",
          pass_criteria="Metrics deviate from the reference values by less than TBD; blocked and blurred charts are indicated.")),
    ("Run the exposure control in a light chamber across the illuminance range TBD with a pedestrian target.",
     6,
     dict(test_level="system", environment="bench", scenario="SC-01, SC-02, SC-03, SC-04",
          pass_criteria="The pedestrian region stays within the usable brightness range at every illuminance step.")),
]


def doorstop(*args):
    subprocess.run(["doorstop", *args], check=True)


def write_item(path, text, extra):
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data["text"] = text
    data.update(extra)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def main():
    n_swr = len(list(SWR_DIR.glob("SWR-*.yml")))
    n_tst = len(list(TST_DIR.glob("TST-*.yml")))
    if n_swr != 15 or n_tst != 17:
        print(f"Expected 15 SWR and 17 TST items, found {n_swr} and {n_tst}.")
        print("Stopping so nothing is duplicated or misnumbered.")
        return

    new_swr_ids = []
    for i, (text, parents, extra) in enumerate(NEW_SWR, start=1):
        uid = f"SWR-{n_swr + i:03d}"
        doorstop("add", "SWR")
        path = SWR_DIR / f"{uid}.yml"
        if not path.exists():
            raise SystemExit(f"Expected {path} after doorstop add, but it does not exist.")
        write_item(path, text, extra)
        for p in parents:
            doorstop("link", uid, p)
        new_swr_ids.append(uid)
        print(f"created {uid} -> {', '.join(parents)}")

    for i, (text, swr_index, extra) in enumerate(NEW_TST, start=1):
        uid = f"TST-{n_tst + i:03d}"
        doorstop("add", "TST")
        path = TST_DIR / f"{uid}.yml"
        if not path.exists():
            raise SystemExit(f"Expected {path} after doorstop add, but it does not exist.")
        extra = dict(extra, status="planned", result="")
        write_item(path, text, extra)
        parent = new_swr_ids[swr_index - 1]
        doorstop("link", uid, parent)
        print(f"created {uid} -> {parent}")


if __name__ == "__main__":
    main()
