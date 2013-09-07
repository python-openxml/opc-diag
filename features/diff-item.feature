Feature: diff an OPC package item
  In order to isolate the differences between an item in two OPC packages
  As an Open XML developer
  I need to diff a corresponding pair of items between two packages

  Scenario: diff the content types item between two packages
      When I issue a command to diff the content types between two packages
      Then the content types diff appears on stdout

  Scenario: diff the package rels item between two packages
      When I issue a command to diff the package rels between two packages
      Then the package rels diff appears on stdout

  Scenario: diff the slide master XML part between two packages
      When I issue a command to diff the slide master between two packages
      Then the slide master diff appears on stdout
