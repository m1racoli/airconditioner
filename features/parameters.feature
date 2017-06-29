# Created by cedrikneumann at 06.04.16
Feature: Define and overwrite parameters
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The task "my_task" is a dummy operator as default
    And The task "my_other_task" is a dummy operator as default
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"


  Scenario: The game name is accessible in the task
    When I build the DAGs
    Then The parameter "game" of the task "my_task" in DAG "my_game" equals "my_game"

  Scenario Outline: Reserved parameters cannot be overwritten
    Given The game "<game>" has the parameter "<key>" set as "<value>"
    When I build the DAGs
    Then The parameter "<key>" of the task "my_task" in DAG "my_game" equals "<expected>"

    Examples:
      | game    | key      | value   | expected |
      | my_game | game     | another | my_game  |
      | default | game     | another | my_game  |
      | my_game | platform | another | android  |
      | default | platform | another | android  |
      | my_game | profile  | another | default  |
      | default | profile  | another | default  |

  Scenario: Set default parameter
    Given The game "default" has the parameter "my_param" set as "my_value"
    When I build the DAGs
    Then The parameter "my_param" of the task "my_task" in DAG "my_game" equals "my_value"

  Scenario: Set game parameter
    Given The game "my_game" has the parameter "my_param" set as "my_value"
    When I build the DAGs
    Then The parameter "my_param" of the task "my_task" in DAG "my_game" equals "my_value"

  Scenario: Game parameter overwrites the default parameter
    Given The game "default" has the parameter "my_param" set as "default_value"
    And The game "my_game" has the parameter "my_param" set as "my_value"
    When I build the DAGs
    Then The parameter "my_param" of the task "my_task" in DAG "my_game" equals "my_value"

  Scenario: Set default argument
    Given The game "default" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Set game argument
    Given The game "my_game" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Set cluster argument
    Given The cluster "my_cluster" for the game "my_game" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Game argument overwrites the default argument
    Given The game "default" has the argument "queue" set as "default_value"
    And The game "my_game" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Clusters argument overwrites the game argument
    Given The game "my_game" has the argument "queue" set as "default_value"
    And The cluster "my_cluster" for the game "my_game" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Clusters argument overwrites the default argument
    Given The game "default" has the argument "queue" set as "default_value"
    And The cluster "my_cluster" for the game "my_game" has the argument "queue" set as "my_queue"
    When I build the DAGs
    Then The attribute "queue" of the task "my_task" in DAG "my_game" equals "my_queue"

  Scenario: Clusters argument overwrites the default argument
    Given The game "default" has the argument "conn_id" set as "default_conn_id"
    And The cluster "my_cluster" for the game "my_game" has the argument "sql" set as "SELECT 1 FROM DUAL"
    And The cluster "my_cluster" for the game "my_game" has the argument "conn_id" set as "my_conn_id"
    And The cluster "my_cluster" has the task "my_http_task"
    And The task "my_http_task" is a sql_sensor operator as default
    When I build the DAGs
    Then The attribute "conn_id" of the task "my_http_task" in DAG "my_game" equals "my_conn_id"

  Scenario: When start date is set on cluster and game config and cluster's is youngest, task has cluster date
    Given The game "my_game" has the argument "start_date" set as "2016-03-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-06-15"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The start_date of the task "my_task" in DAG "my_game" equals "2016-06-15"

  Scenario: When start date is set on cluster and game config and game's is youngest, task has game date
    Given The game "my_game" has the argument "start_date" set as "2016-06-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-03-15"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The start_date of the task "my_task" in DAG "my_game" equals "2016-06-20"

  Scenario: When start date is set on cluster, game and game cluster config and cluster's is youngest, task has cluster date
    Given The game "my_game" has the argument "start_date" set as "2016-01-20"
    Given The cluster "my_cluster" for the game "my_game" has the argument "start_date" set as "2016-03-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-06-15"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The start_date of the task "my_task" in DAG "my_game" equals "2016-06-15"

  Scenario: When start date is set on cluster, game and game cluster config and game clusters's is youngest, task has game cluster date
    Given The game "my_game" has the argument "start_date" set as "2016-01-20"
    Given The cluster "my_cluster" for the game "my_game" has the argument "start_date" set as "2016-06-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-03-15"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The start_date of the task "my_task" in DAG "my_game" equals "2016-06-20"

  Scenario: When start date is set on cluster, game and game cluster config and game is youngest, task has game date
    Given The game "my_game" has the argument "start_date" set as "2016-05-20"
    Given The cluster "my_cluster" for the game "my_game" has the argument "start_date" set as "2016-04-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-02-15"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    Then The start_date of the task "my_task" in DAG "my_game" equals "2016-05-20"

  Scenario: When start date is set on cluster and game for a task this must not affect other tasks
    Given The game "my_game" has the argument "start_date" set as "2016-01-20"
    And The cluster "my_cluster" has a task "my_task" with the argument "start_date" set as "2016-02-15"
    And The cluster "my_cluster" has the task "my_other_task"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task"
    And The start_date of the task "my_task" in DAG "my_game" equals "2016-02-15"
    And The start_date of the task "my_other_task" in DAG "my_game" equals "2016-01-20"