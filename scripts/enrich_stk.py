"""Add extra attributes to the STK items. Existing text, links and level are kept.

Run from the project root with the venv active:
    python enrich_stk.py
Then:
    doorstop
    doorstop review all
"""
from pathlib import Path
import yaml

STK_DIR = Path("reqs") / "stk"

EXTRA = {
    "STK-001": dict(
        rationale="Pedestrian collisions are a leading cause of urban fatalities; AEB is a key mitigation.",
        source="Vehicle program / Euro NCAP VRU scenarios",
        priority="high", asil="D", verification_method="test"),
    "STK-002": dict(
        rationale="Unwarranted braking can cause rear-end collisions and erodes driver trust; controllability must be preserved.",
        source="Vehicle program / ISO 26262 and SOTIF controllability",
        priority="high", asil="B", verification_method="test"),
    "STK-003": dict(
        rationale="A degraded camera can silently reduce detection performance; the driver and vehicle must be informed.",
        source="Safety assessor",
        priority="high", asil="B", verification_method="test"),
    "STK-004": dict(
        rationale="Logged data supports root-cause analysis after incidents and field issues.",
        source="Service / diagnostics",
        priority="medium", asil="QM", verification_method="demonstration"),
    "STK-005": dict(
        rationale="Safety-related functions require a documented safety argument and compliant development process.",
        source="Safety assessor",
        priority="high", asil="n/a", verification_method="analysis"),
    "STK-006": dict(
        rationale="Pedestrian detection must work in the realistic lighting and weather conditions of the operational domain.",
        source="Vehicle program",
        priority="medium", asil="QM", verification_method="test"),
}


def main():
    for uid, extra in EXTRA.items():
        path = STK_DIR / f"{uid}.yml"
        if not path.exists():
            print(f"skip {uid}: {path} not found")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data.update(extra)
        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        print(f"updated {uid}")


if __name__ == "__main__":
    main()
