"""Scan every fixture, print the findings and score, and compare with expected.json.

Run from the repo root:   python -m app.run_fixtures
Exit code is 1 if any fixture does not match expected.json.
"""
import json
import sys
from pathlib import Path

from app.scanner import scan_html_file
from app.scoring import score

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "html"


def main():
    expected = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    failures = 0
    for f in sorted(FIXTURES.glob("*.html")):
        result = scan_html_file(f)
        found = {v["id"] for v in result["violations"]}
        s = score(result["violations"])
        print(f"\n{f.name}  score={s}")
        for v in sorted(result["violations"], key=lambda v: v["id"]):
            print(f"   - {v['id']} ({v['impact']}, {v['nodes']} node(s))")
        if result["incomplete"]:
            print(f"   needs human review: {', '.join(sorted(result['incomplete']))}")

        exp = expected.get(f.name)
        if exp is None:
            print("   (no expectation in expected.json)")
            continue
        missing = [r for r in exp["must_include"] if r not in found]
        unwanted = [r for r in exp["must_not_include"] if r in found]
        if missing or unwanted:
            failures += 1
            if missing:
                print(f"   MISMATCH: expected but not found: {missing}")
            if unwanted:
                print(f"   MISMATCH: found but should not appear: {unwanted}")
        else:
            print("   matches expected.json")
    print(f"\n{failures} fixture(s) do not match expected.json")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
