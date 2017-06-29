# Created by cedrikneumann at 06.04.16
Feature: Resolve task definitions based on platforms
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"

  Scenario: default given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"

  Scenario: platform given
    Given The task "my_task" is a dummy operator for profile "default" and platform "android"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"

  Scenario: other platform given
    Given The task "my_task" is a dummy operator for profile "default" and platform "ios"
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

  Scenario: default and other platform given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    Given The task "my_task" is a mysql operator for profile "default" and platform "ios"
    And The task "my_task" for profile "default" and platform "ios" has the argument "sql" set to "SELECT 1"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a dummy operator

  Scenario: default and platform given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    Given The task "my_task" is a bash operator for profile "default" and platform "android"
    And The task "my_task" for profile "default" and platform "android" has the argument "bash_command" set to "echo hello"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a bash operator

  Scenario: platform and other platform given
    Given The task "my_task" is a dummy operator for profile "default" and platform "android"
    Given The task "my_task" is a mysql operator for profile "default" and platform "ios"
    And The task "my_task" for profile "default" and platform "ios" has the argument "sql" set to "SELECT 1"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a dummy operator
