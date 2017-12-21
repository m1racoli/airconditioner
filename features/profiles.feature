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

Feature: Resolve task definitions based on profiles

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
    And The task "my_task" is a bash operator for profile "my_profile" and platform "default"
    And The task "my_task" for profile "my_profile" and platform "default" has the argument "bash_command" set to "echo hello"
    And The game "my_game" has the profile "my_profile"
    When I build the DAGs
    Then The DAG "my_game" has the task "my_task" as a bash operator
