# Accessibility Document Checker (working title)

Upload an HTML (and, later, DOCX) file, get an accessibility score and issue
list, apply automatic fixes, rescan, and download the improved file.

**Status:** MVP in progress (2-week build). Learning project for accessibility
testing (WCAG 2.2, axe-core) and BDD with Gauge, hosted on AWS.

## MVP scope
- [ ] HTML: upload -> scan -> score -> auto-fix -> rescan -> download
- [ ] DOCX: upload -> structural scan -> score (read-only)
- [ ] Gauge (Java + Selenium) end-to-end specs
- [ ] REST Assured API tests
- [ ] GitHub Actions CI
- [ ] Deployed on AWS (S3 + CloudFront + API Gateway + Lambda)

## Repo layout
    app/        Python backend: scanner, scorer, fixer
    web/        Static front end (upload page, score, download)
    tests/gauge Gauge specs and Java step implementations
    fixtures/   Known-bad sample files with expected results
    infra/      AWS deployment scripts / templates
    docs/       Scoring formula, design notes, test strategy

## Honest limits
- Automated tools find only a portion of accessibility problems; manual review
  with a keyboard and screen reader is still required.
- Auto-fix cannot judge meaning (e.g. whether alt text is accurate). Such items
  are flagged for a human, not guessed.

## Test content
Sample files in `fixtures/` are original and written for this project.
