"""Run axe-core against an HTML file using a headless browser (Playwright)."""
from pathlib import Path

from playwright.sync_api import sync_playwright

AXE_PATH = Path(__file__).parent / "vendor" / "axe.min.js"


def scan_html_file(path):
    """Scan one HTML file. Returns {'violations': [...], 'incomplete': [...]}.

    Each violation: id, impact, help, help_url, nodes (count), tags.
    'incomplete' lists rule ids axe could not decide automatically, which
    need a human to review.
    """
    path = Path(path).resolve()
    if not AXE_PATH.exists():
        raise FileNotFoundError(
            f"{AXE_PATH} not found. Download axe.min.js into app/vendor/ (see Day 2 steps)."
        )
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(path.as_uri())
            page.add_script_tag(path=str(AXE_PATH))
            results = page.evaluate("async () => await axe.run()")
        finally:
            browser.close()

    violations = [
        {
            "id": v["id"],
            "impact": v.get("impact"),
            "help": v["help"],
            "help_url": v["helpUrl"],
            "nodes": len(v["nodes"]),
            "tags": v["tags"],
        }
        for v in results["violations"]
    ]
    incomplete = [i["id"] for i in results["incomplete"]]
    return {"violations": violations, "incomplete": incomplete}
