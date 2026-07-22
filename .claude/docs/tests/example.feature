# Gherkin test cases — one `.feature` file per critical PRD journey.
# Standard: ~/.claude/sop/TESTING.md
# Baseline: every critical user journey in the PRD must have E2E coverage.
# Rename this file per journey (e.g. login.feature, checkout.feature).

Feature: <capability from a PRD journey>
  As a <user>
  I want <goal>
  So that <benefit>

  Scenario: <happy path>
    Given <initial context>
    When <action>
    Then <expected outcome>

  Scenario: <edge or error case>
    Given <initial context>
    When <invalid action>
    Then <expected error handling>
