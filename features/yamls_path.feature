# Created by etienedalcol at 4/18/16
Feature: Buid from different Yaml paths
  # Enter feature description here

  @wip
  Scenario: Load a group of yamls
    #/Users/etienedalcol/git/bit.airconditioner/features/test_yamls
    Given I have a set of YAMLs located at "features/test_yamls/group_1"
    When I build the DAGs from those YAMLs
    Then I have the DAG defined in the YAMLs
    # Enter steps here