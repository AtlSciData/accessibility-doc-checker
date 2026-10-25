"""Transparent accessibility score.

score = max(0, 100 - sum(weight(impact) * min(nodes, cap(impact))))
Only violations tied to a WCAG success criterion (a tag starting with "wcag")
are scored. Best-practice-only rules are reported as advice, not scored.
Violations with no 'tags' key are treated as WCAG (keeps simple callers/tests working).
"""

WEIGHTS = {"critical": 10, "serious": 7, "moderate": 3, "minor": 1}
CAPS = {"critical": 3, "serious": 3, "moderate": 5, "minor": 5}


def is_wcag(violation):
    tags = violation.get("tags")
    if tags is None:
        return True
    return any(t.startswith("wcag") for t in tags)


def penalty(impact, node_count):
    key = impact if impact in WEIGHTS else "minor"
    return WEIGHTS[key] * min(node_count, CAPS[key])


def score(violations):
    total = sum(
        penalty(v.get("impact"), v["nodes"])
        for v in violations
        if is_wcag(v)
    )
    return max(0, 100 - total)
