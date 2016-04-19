# Created by etienedalcol at 4/18/16
Feature: Build from different Yaml paths
  # Enter feature description here

  Scenario: Load a group of yamls
    Given I have a set of YAMLs located at "features/test_yamls/group_1"
    When I build the DAGs from those YAMLs
    Then There is 1 DAG
    And The DAG "my_game" has the task "my_task"
    And The DAG "my_game" has the task "my_other_task"
    And In the DAG "my_game" the task "my_other_task" is dependency of "my_task"
