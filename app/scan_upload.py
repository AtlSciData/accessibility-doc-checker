"""Scan uploaded HTML text safely: no network, no file:// access."""
from pathlib import Path
from playwright.sync_api import sync_playwright

AXE_PATH = Path(__file__).parent / "vendor" / "axe.min.js"


def scan_html_text(html):
    if not AXE_PATH.exists():
        raise FileNotFoundError("axe.min.js missing from app/vendor")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            context = browser.new_context()
            context.route("**/*", lambda route: route.abort())
            page = context.new_page()
            page.set_default_timeout(15000)
            page.set_content(html, wait_until="load")
            page.add_script_tag(path=str(AXE_PATH))
            raw = page.evaluate("async () => await axe.run()")
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
        for v in raw["violations"]
    ]
    return {"violations": violations, "incomplete": [i["id"] for i in raw["incomplete"]]}
