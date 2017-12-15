# Created by cedrikneumann at 07.04.16
Feature: Manage time deltas
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"

  Scenario: A later time delta depends on the next previous time delta
    Given The cluster "my_cluster" has the task "delta_1"
    And The cluster "my_cluster" has the task "delta_2"
    And The cluster "my_cluster" has the task "delta_3"
    And The task "delta_1" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_1" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 2h"
    And The task "delta_2" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_2" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 4h"
    And The task "delta_3" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_3" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 6h"
    When I build the DAGs
    Then The DAG "my_game" has the task "delta_1" as a time_delta operator
    And The DAG "my_game" has the task "delta_2" as a time_delta operator
    And The DAG "my_game" has the task "delta_3" as a time_delta operator
    And In the DAG "my_game" the task "delta_1" is dependency of "delta_2"
    And In the DAG "my_game" the task "delta_2" is dependency of "delta_3"
    And In the DAG "my_game" the task "delta_1" is not dependency of "delta_3"

  Scenario: A later time delta depends on the next previous time delta even when tasks were set in odd orders
    Given The cluster "my_cluster" has the task "delta_1"
    And The cluster "my_cluster" has the task "delta_3"
    And The cluster "my_cluster" has the task "delta_2"
    And The task "delta_2" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_2" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 4h"
    And The task "delta_1" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_1" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 2h"
    And The task "delta_3" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_3" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 6h"
    When I build the DAGs
    Then The DAG "my_game" has the task "delta_1" as a time_delta operator
    And The DAG "my_game" has the task "delta_2" as a time_delta operator
    And The DAG "my_game" has the task "delta_3" as a time_delta operator
    And In the DAG "my_game" the task "delta_1" is dependency of "delta_2"
    And In the DAG "my_game" the task "delta_2" is dependency of "delta_3"
    And In the DAG "my_game" the task "delta_1" is not dependency of "delta_3"