# Accessibility score formula (draft v0.1)

The score is a transparent, repeatable number between 0 and 100. It is a
**triage aid, not a compliance certification**. Automated checks catch only
part of WCAG, so a score of 100 does not mean a file is fully accessible.

## Formula

For each violation rule found:

    penalty(rule) = weight(impact) * min(node_count, CAP)

    score = max(0, 100 - sum(penalty over all violations))

| Impact   | weight | CAP (max nodes counted per rule) |
|----------|--------|----------------------------------|
| critical | 10     | 3                                |
| serious  | 7      | 3                                |
| moderate | 3      | 5                                |
| minor    | 1      | 5                                |

Why a cap: one rule repeated 40 times (e.g. 40 images without alt text)
should hurt the score, but should not hide every other problem.

## Rules of the road
- Every number above is a starting point. Tune it on Day 2 using your fixtures,
  then freeze it and record the final values here.
- The same input must always produce the same score (unit-test this).
- Report the score together with the list of issues and the "needs human
  review" items, never the score alone.

## v1.0 (frozen)
Only violations carrying a WCAG tag are scored. Best-practice-only rules (for example landmark-one-main, region, heading-order) are listed as advice and do not change the score. Weights and caps: critical 10 (cap 3), serious 7 (cap 3), moderate 3 (cap 5), minor 1 (cap 5).

