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

Feature: Resolve task definitions based on platforms

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
