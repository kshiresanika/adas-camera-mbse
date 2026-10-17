"""Traceability matrix and coverage report for the Doorstop requirements.

Reads reqs/<doc>/*.yml directly, so it needs only PyYAML (installed with Doorstop).

Run from the project root with the venv active:
    python trace_report.py

Writes:
    reports/trace_matrix.csv
    reports/coverage_report.md

Chain:  STK -> SYS -> SUB -> SWR -> TST
                   \\-> SAF  (reached from SWR through the attribute saf_ref)
                      SUB -> ICD

Status of a requirement:
    COVERED   every branch below it ends in a test case
    PARTIAL   some branches end in a test case, some do not
    GAP       nothing below it ends in a test case
    NON-TEST  verification_method is analysis or inspection (evidence outside TST)
"""
import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

DOCS = ["STK", "SYS", "SUB", "SAF", "ICD", "SWR", "TST"]
NON_TEST = {"analysis", "inspection"}
OUT = Path("reports")


def load():
    items = {}
    for prefix in DOCS:
        folder = Path("reqs") / prefix.lower()
        if not folder.exists():
            continue
        for f in sorted(folder.glob(f"{prefix}-*.yml")):
            d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            if d.get("active", True) is False:
                continue
            links = []
            for entry in d.get("links") or []:
                links.append(next(iter(entry)) if isinstance(entry, dict) else str(entry))
            d["uid"] = f.stem
            d["prefix"] = prefix
            d["links"] = links
            d["text"] = " ".join(str(d.get("text", "")).split())
            items[f.stem] = d
    return items


def main():
    items = load()
    if not items:
        print("No requirement files found under reqs/. Run this from the project root.")
        return

    children = defaultdict(list)
    unknown_links = []
    for uid, d in items.items():
        for parent in d["links"]:
            if parent in items:
                children[parent].append(uid)
            else:
                unknown_links.append((uid, parent))
        saf = str(d.get("saf_ref") or "").strip()
        if saf:
            if saf in items:
                if uid not in children[saf]:
                    children[saf].append(uid)
            else:
                unknown_links.append((uid, saf))

    orphans = [
        uid for uid, d in items.items()
        if d["prefix"] != "STK" and not any(p in items for p in d["links"])
    ]

    memo = {}

    def status(uid):
        if uid in memo:
            return memo[uid]
        d = items[uid]
        if d["prefix"] == "TST":
            s = "COVERED"
        elif str(d.get("verification_method", "")).lower() in NON_TEST:
            s = "NON-TEST"
        else:
            rel = [status(c) for c in children[uid]]
            rel = [r for r in rel if r != "NON-TEST"]
            if not rel:
                s = "GAP"
            elif all(r == "COVERED" for r in rel):
                s = "COVERED"
            elif any(r in ("COVERED", "PARTIAL") for r in rel):
                s = "PARTIAL"
            else:
                s = "GAP"
        memo[uid] = s
        return s

    def paths(uid, row):
        row = dict(row)
        row[items[uid]["prefix"]] = uid
        kids = children[uid]
        if not kids:
            yield row
            return
        for kid in kids:
            yield from paths(kid, row)

    OUT.mkdir(exist_ok=True)

    # Traceability matrix
    with open(OUT / "trace_matrix.csv", "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(DOCS + ["STK_status"])
        for stk in sorted(u for u, d in items.items() if d["prefix"] == "STK"):
            for row in paths(stk, {}):
                writer.writerow([row.get(p, "") for p in DOCS] + [status(stk)])

    # Coverage report
    lines = [f"# Coverage report ({date.today().isoformat()})", ""]

    lines += ["## Summary per document", "",
              "| Document | Items | COVERED | PARTIAL | GAP | NON-TEST |",
              "|---|---|---|---|---|---|"]
    for prefix in DOCS:
        group = [u for u, d in items.items() if d["prefix"] == prefix]
        if not group:
            continue
        c = Counter(status(u) for u in group)
        lines.append(
            f"| {prefix} | {len(group)} | {c['COVERED']} | {c['PARTIAL']} | {c['GAP']} | {c['NON-TEST']} |")
    lines.append("")

    for label, wanted in (("Gaps (no test case reachable)", "GAP"),
                          ("Partially covered", "PARTIAL")):
        found = [u for u in items if items[u]["prefix"] != "TST" and status(u) == wanted]
        lines += [f"## {label}", ""]
        if not found:
            lines += ["None.", ""]
        else:
            for u in found:
                lines.append(f"- **{u}**: {items[u]['text'][:110]}")
            lines.append("")

    lines += ["## Verified outside the test plan (analysis or inspection)", ""]
    non_test = [u for u in items if status(u) == "NON-TEST"]
    if non_test:
        for u in non_test:
            lines.append(f"- **{u}** ({items[u].get('verification_method')}): {items[u]['text'][:110]}")
    else:
        lines.append("None.")
    lines.append("")

    lines += ["## Status of stakeholder, system and safety requirements", "",
              "| ID | Status | Verification method |", "|---|---|---|"]
    for u in items:
        if items[u]["prefix"] in ("STK", "SYS", "SAF"):
            lines.append(f"| {u} | {status(u)} | {items[u].get('verification_method', '')} |")
    lines.append("")

    lines += ["## Link problems", ""]
    if orphans:
        lines.append("Items without a parent link: " + ", ".join(sorted(orphans)))
    else:
        lines.append("No items without a parent link.")
    if unknown_links:
        lines.append("")
        lines.append("Links to items that do not exist: "
                     + ", ".join(f"{a} -> {b}" for a, b in unknown_links))
    else:
        lines.append("")
        lines.append("No links to missing items.")
    lines.append("")

    tbd = Counter(d["prefix"] for d in items.values() if "TBD" in d["text"])
    lines += ["## Open points (TBD in the requirement text)", ""]
    if tbd:
        lines.append(", ".join(f"{k}: {v}" for k, v in sorted(tbd.items())))
    else:
        lines.append("None.")
    lines.append("")

    tests = [d for d in items.values() if d["prefix"] == "TST"]
    executed = sum(1 for d in tests if str(d.get("result") or "").strip())
    lines += ["## Test execution", "",
              f"{len(tests)} test cases planned, {executed} with a recorded result.", ""]

    (OUT / "coverage_report.md").write_text("\n".join(lines), encoding="utf-8")

    total = Counter(status(u) for u in items if items[u]["prefix"] != "TST")
    print("Wrote reports/trace_matrix.csv and reports/coverage_report.md")
    print("Requirement status:", dict(total))
    if orphans:
        print("Items without parent link:", ", ".join(sorted(orphans)))
    if unknown_links:
        print("Links to missing items:", unknown_links)


if __name__ == "__main__":
    main()
