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

Feature: Manage time deltas

  Background:
    Given We have an empty configuration
    And There are minimum default arguments specified
    And There is a cluster "my_cluster"
    And The game config contains the item "my_game"
    And The game "my_game" has the platform "android"
    And The game "my_game" has the cluster "my_cluster"

  Scenario: A later time delta depends on the next previous time delta
    Given The cluster "my_cluster" has the task "delta_1"
    And The cluster "my_cluster" has the task "delta_2"
    And The cluster "my_cluster" has the task "delta_3"
    And The task "delta_1" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_1" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 2h"
    And The task "delta_2" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_2" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 4h"
    And The task "delta_3" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_3" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 6h"
    When I build the DAGs
    Then The DAG "my_game" has the task "delta_1" as a time_delta operator
    And The DAG "my_game" has the task "delta_2" as a time_delta operator
    And The DAG "my_game" has the task "delta_3" as a time_delta operator
    And In the DAG "my_game" the task "delta_1" is dependency of "delta_2"
    And In the DAG "my_game" the task "delta_2" is dependency of "delta_3"
    And In the DAG "my_game" the task "delta_1" is not dependency of "delta_3"

  Scenario: A later time delta depends on the next previous time delta even when tasks were set in odd orders
    Given The cluster "my_cluster" has the task "delta_first"
    And The cluster "my_cluster" has the task "delta_second"
    And The cluster "my_cluster" has the task "delta_last"
    And The task "delta_first" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_first" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 2m"
    And The task "delta_second" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_second" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 4m"
    And The task "delta_last" is a time_delta operator for profile "default" and platform "default"
    And The task "delta_last" for profile "default" and platform "default" has the argument "delta" set to "!timedelta 6m"
    When I build the DAGs
    Then The DAG "my_game" has the task "delta_second" as a time_delta operator
    And The DAG "my_game" has the task "delta_first" as a time_delta operator
    And The DAG "my_game" has the task "delta_last" as a time_delta operator
    And In the DAG "my_game" the task "delta_first" is dependency of "delta_second"
    And In the DAG "my_game" the task "delta_second" is dependency of "delta_last"
    And In the DAG "my_game" the task "delta_first" is not dependency of "delta_last"
    And In the DAG "my_game" the task "delta_last" is not dependency of "delta_first"
