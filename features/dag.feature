Feature: Generate DAGs

  Background:
    Given We have an empty configuration
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The cluster "my_cluster" has the task "my_other_task"
    And The task "my_task" is a dummy operator as default
    And The task "my_other_task" is a dummy operator as default

  Scenario: No DAG
    When I build the DAGs
    Then There are no DAGs

  Scenario: Empty DAG
    Given The game config contains the item "my_game"
    When I build the DAGs
    Then There is 1 DAG
    And The DAG "my_game" is empty

  Scenario: Ignore default game config
    Given The game config contains the item "default"
    When I build the DAGs
    Then There are no DAGs

  Scenario: DAG with two operators
    Given There are minimum default arguments specified
    Given The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"
    When I build the DAGs
    Then There is 1 DAG
    And The DAG "my_game" has 2 tasks
    And The DAG "my_game" has the task "my_task"
    And The DAG "my_game" has the task "my_other_task"

  Scenario: DAG with depending operators
    Given There are minimum default arguments specified
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"
    And The task "my_task" is dependency of the task "my_other_task"
    When I build the DAGs
    Then There is 1 DAG
    And The DAG "my_game" has 2 tasks
    And The DAG "my_game" has the task "my_task"
    And The DAG "my_game" has the task "my_other_task"
    And In the DAG "my_game" the task "my_task" is dependency of "my_other_task"

  Scenario: Missing dependency
    Given There are minimum default arguments specified
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"
    And The task "not_existing_task" is dependency of the task "my_task"
    When I try to build the DAGs
    Then There has been an exception "DependencyException"

  Scenario: Build selected DAGs
    Given The game config contains the item "my_dag_1"
    And The game config contains the item "my_dag_2"
    And The game config contains the item "my_dag_3"
    When I build the DAGs with the ids "my_dag_2,my_dag_3"
    Then There is 2 DAG
