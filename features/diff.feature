Feature: diff two OPC packages
  In order to detect all the differences between two OPC packages
  As an Open XML developer
  I need to diff two packages against each other

  Scenario: diff two packages against each other
      When I issue a command to diff two packages
      Then the package diff appears on stdout
