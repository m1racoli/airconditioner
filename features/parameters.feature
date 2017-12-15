# Created by cedrikneumann at 06.04.16
Feature: Define and overwrite parameters
  # Enter feature description here

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"
    And The task "my_task" is a dummy operator as default
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
