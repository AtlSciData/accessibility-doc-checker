# DRAFT: written on Day 1 as a target for the end-to-end tests.
# Step definitions are implemented on Day 7. Rule IDs and score thresholds
# must be confirmed against real axe results on Day 2.
Feature: Scan an HTML file and see its accessibility score
  As a content author
  I want to upload a file and see an accessibility score with the issues found
  So that I know what to fix before publishing

  Background:
    Given I open the checker page

  Scenario Outline: Known-bad files show the expected issue and a score below 100
    When I upload "<file>"
    Then I should see the issue "<rule>" listed
    And the score should be below 100

    Examples:
      | file                         | rule           |
      | 01-missing-lang-title.html   | html-has-lang  |
      | 02-form-no-labels.html       | label          |
      | 03-images-no-alt.html        | image-alt      |
      | 04-low-contrast.html         | color-contrast |
      | 05-heading-table-link.html   | link-name      |

  Scenario: An accessible file has no serious or critical issues
    When I upload "06-accessible-baseline.html"
    Then I should see no serious or critical issues

  Scenario: Fixing a file raises its score
    Given I have uploaded "01-missing-lang-title.html"
    And I note the original score
    When I click "Fix"
    Then the new score should be higher than the original score
    And I can download the fixed file

  Scenario: The upload page itself is accessible
    Then the checker page has no serious or critical accessibility violations
