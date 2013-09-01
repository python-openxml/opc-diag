Feature: diff an OPC package item
  In order to isolate the differences between an item in two OPC packages
  As an Open XML developer
  I need to diff a corresponding pair of items between two packages

  @wip
  Scenario: diff the content types item between two packages
      When I issue a command to diff the content types between two packages
      Then the content types diff appears on stdout
