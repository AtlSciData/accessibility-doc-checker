# BDD tests (Cucumber + Java)

Plain-language scenarios live in `features/`. Java step definitions will live
under `src/test/java/...` and are added on Day 7.

## Planned Maven dependencies
- io.cucumber:cucumber-java
- io.cucumber:cucumber-junit-platform-engine
- org.junit.platform:junit-platform-suite
- org.seleniumhq.selenium:selenium-java
- io.rest-assured:rest-assured (API tests)
- com.deque.html.axe-core:selenium (accessibility checks on the app's own UI)

Check current versions on Maven Central when you create the `pom.xml`.

## Run (once implemented)
    mvn test

Reports are written under `cucumber-reports/` (ignored by Git).
