Feature: Substitute an item from one OPC package into another
  In order to isolate which package item is causing a load error
  As an Open XML developer
  I need to substitute a suspect item into a known good package

  @wip
  Scenario: substitute a package item from one package into another
      When I issue a command to substitute a package item
      Then the resulting package contains the substituted item
