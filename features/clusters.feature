Feature: Configure Clusters on per game level

  Background: There two games with the same cluster containing two tasks
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The cluster "my_cluster" has the task "my_other_task"
    And The task "my_task" is a dummy operator as default
    And The task "my_other_task" is a dummy operator as default
    And The game config contains the item "my_game_1"
    And The game config contains the item "my_game_2"
    And The game "my_game_1" has the platform "android"
    And The game "my_game_1" has the cluster "my_cluster"
    And The game "my_game_2" has the platform "android"
    And The game "my_game_2" has the cluster "my_cluster"

  Scenario: Exclude one task for a specific game
    Given The cluster "my_cluster" for the game "my_game_1" has the argument "exclude" set as "my_task"
    When I build the DAGs
    Then There is 2 DAG
    And The DAG "my_game_1" has 1 tasks
    And The DAG "my_game_1" has the task "my_other_task"
    And The DAG "my_game_2" has 2 tasks

  Scenario: Exclude two tasks for a specific game
    Given The cluster "my_cluster" for the game "my_game_2" has the argument "exclude" set as "[my_task,my_other_task]"
    When I build the DAGs
    Then There is 2 DAG
    And The DAG "my_game_1" has 2 tasks
    And The DAG "my_game_2" is empty
