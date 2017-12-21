#
# Copyright 2017 Wooga GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

Feature: Different task types

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
    And The task "my_task" for profile "default" and platform "default" has the argument "<arg_name>" set to "<arg_val>"
    When I try to build the DAGs
    Then There hasn't been an exception
    And The task "my_task" in the DAG "my_game" is a <operator_type> operator as default

    Examples:
      | task_type  | operator_type   | arg_name     | arg_val   |
      | bash       | BashOperator    | bash_command | echo 'jo' |
      | time_delta | TimeDeltaSensor | delta        | 1m        |

  Scenario: Task doesn't exist for platform but it's set as None (meaning it's intentional)
    Given The task "my_task" is a none operator as default
    When I try to build the DAGs
    Then There is 1 DAG
    And There is no task "my_task" in the DAG "my_game"
    And There hasn't been an exception

  Scenario: Throw exception when task in cluster has no definition
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

  Scenario: Throw exception when task in cluster has no definition for game platform
    Given The task "my_task" is a dummy operator for profile "default" and platform "ios"
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

  Scenario: Throw exception when task in cluster has no definition for certain profile
    Given The game "my_game" has the profile "my_profile"
    And The task "my_task" is a dummy operator for profile "other_profile" and platform "android"
    When I try to build the DAGs
    Then There has been an exception "NoTaskException"

  Scenario: Throw exception for unknown task type
    Given The task "my_task" is a bizarre operator as default
    When I try to build the DAGs
    Then There has been an exception "TaskTypeException"

  Scenario: Custom task types
    Given The task "my_task" is a custom_type operator as default
    And I define the type custom_type for the CustomOperator
    When I try to build the DAGs with custom task types
    Then There hasn't been an exception
    And The task "my_task" in the DAG "my_game" is a CustomOperator operator as default

  Scenario: Throw exception for colliding task types
    Given I define the type dummy for the CustomOperator
    When I try to build the DAGs with custom task types
    Then There has been an exception "TaskTypeException"
