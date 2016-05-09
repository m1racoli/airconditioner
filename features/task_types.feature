# Created by cedrikneumann at 02.05.16
Feature: Different task types
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"

  Scenario Outline: Define task types
    Given The task "my_task" is a <task_type> operator as default
    When I try to build the DAGs
    Then The task "my_task" in the DAG "my_game" is a <operator_type> operator as default
    And There hasn't been an exception

    Examples:
      | task_type   | operator_type       |
      | dummy       | DummyOperator       |
      | subschedule | SubScheduleOperator |

    Scenario: Task doesn't exist for platform
    Given The task "my_task" is a none operator as default
    When I try to build the DAGs
    Then There is no task "my_task" in the DAG "my_game"
    And There hasn't been an exception

    Scenario: Throw exception when task in cluster has no definition
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

