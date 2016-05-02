# Created by cedrikneumann at 02.05.16
Feature: #Enter feature name here
  # Enter feature description here

  #TODO add missing dag steps
  Background:
    Given We have an empty configuration
    And There is a cluster "my_cluster"
    And The cluster "my_cluster" has the task "my_task"

    #TODO implement then step
  Scenario Outline: Define task types
    Given The task "my_task" is a <task_type> operator as default
    When I build the DAGs
    Then The task "my_task" is a <operator_type> operator as default
    And There hasn't been an exception

    # TODO add all the task types
    Examples:
      | task_type | operator_type |
      | dummy     | DummyOperator |

    Scenario: Task doesn't exist for platform
    Given The task "my_task" is a none operator as default
    When I build the DAGs
    Then There is no task "my_task"
    And There hasn't been an exception

    Scenario: Throw exception when task in cluster has no definition
    When I build the DAGs
    Then There has been an exception "NoTaskException"

