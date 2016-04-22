# Created by etienedalcol at 4/11/16
Feature: Check config type conversion
#
  Background:
    Given We have an empty yaml configuration

  Scenario: Date
    Given The line "my_date: 2016-03-20" has been appended to the YAML config
    When I load the YAML config
    Then The type of "my_date" is a "date"

  Scenario Outline: Timedelta
    Given The line "my_delta: !timedelta <in>" has been appended to the YAML config
    When I load the YAML config
    Then The type of "my_delta" is a "timedelta"
    And The object "my_delta" prints to "<out>"

    Examples:
      | in            | out               |
      | 6s            | 0:00:06           |
      | 12m           | 0:12:00           |
      | 14h           | 14:00:00          |
      | 3d            | 3 days, 0:00:00   |
      | 4w            | 28 days, 0:00:00  |
      | 2w5d22h34m12s | 19 days, 22:34:12 |

  Scenario Outline: Lambda
    Given The line "my_lambda: !lambda '<fun>'" has been appended to the YAML config
    When I load the YAML config
    Then The type of "my_lambda" is a "function"
    And The function "my_lambda" evaluates "<in>" to "<out>"

    Examples:
      | fun          | in  | out |
      | s: s.lower() | STR | str |
      | s: s.upper() | str | STR |
