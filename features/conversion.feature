# Created by etienedalcol at 4/11/16
Feature: Check config type conversion
#
  Background:
    Given We have an empty yaml configuration

  Scenario: Date
    Given The line "my_date: 2016-03-20" has been appended to the YAML config
    When I load the YAML config
    Then The type of "my_date" is a "date"

  Scenario: Timedelta
    Given The line "my_delta: !timedelta 2h" has been appended to the YAML config
    When I load the YAML config
    Then The type of "my_delta" is a "timedelta"
