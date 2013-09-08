Feature: Extract an OPC package into a directory
  In order to conveniently operate on individual parts in an OPC package
  As an Open XML developer
  I need to extract the items in an OPC package to files in a directory tree

  @wip
  Scenario: extract an OPC package into a directory
     Given a target directory that does not exist
      When I issue a command to extract a package
      Then the package items appear in the target directory
