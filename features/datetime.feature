# Created by etienedalcol at 4/19/16
Feature: Check conversion from date to datetime from the yamls to the dags
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And The game config contains the item "my_game"
    And There is a cluster "my_cluster"
    And The game "my_game" has the cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The game "my_game" has the platform "test_platform"
    And The task "my_task" is a dummy operator as default

  Scenario: Start date on game config
    Given The game "my_game" has the argument "start_date" set as "2016-03-20"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The attribute "start_date" of the task "my_task" in DAG "my_game" is of type "datetime"

  Scenario: End date on game config
    Given The game "my_game" has the argument "end_date" set as "2016-03-20"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The attribute "end_date" of the task "my_task" in DAG "my_game" is of type "datetime"

  Scenario: Start date on cluster config
    Given The cluster "my_cluster" for the game "my_game" has the argument "start_date" set as "2016-03-20"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The attribute "start_date" of the task "my_task" in DAG "my_game" is of type "datetime"

  Scenario: End date on cluster config
    Given The cluster "my_cluster" for the game "my_game" has the argument "end_date" set as "2016-03-20"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The attribute "end_date" of the task "my_task" in DAG "my_game" is of type "datetime"


