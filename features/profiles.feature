# Created by cedrikneumann at 06.04.16
Feature: Resolve task definitions based on profiles
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"

  Scenario: Resolve default
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"

  Scenario: Resolve default no default profile and with a different profile given
    Given The task "my_task" is a dummy operator for profile "my_profile" and platform "default"
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

  Scenario: Resolve profile with profile given
    Given The task "my_task" is a dummy operator for profile "my_profile" and platform "default"
    And The game "my_game" has the profile "my_profile"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"

  Scenario: Resolve profile with default given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    And The game "my_game" has the profile "my_profile"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"

  Scenario: Resolve default when default and profile given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    And The task "my_task" is a mysql operator for profile "my_profile" and platform "default"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a dummy operator

  Scenario: Resolve profile when default and profile given
    Given The task "my_task" is a dummy operator for profile "default" and platform "default"
    And The task "my_task" is a mysql operator for profile "my_profile" and platform "default"
    And The task "my_task" for profile "my_profile" and platform "default" has the argument "sql" set to "SELECT 1"
    And The game "my_game" has the profile "my_profile"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a mysql operator