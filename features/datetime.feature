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

Feature: Check conversion from date to datetime from the yamls to the dags

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


