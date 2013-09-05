Feature: Browse an OPC package item
  In order to readily explore the contents of an OPC package item
  As an Open XML developer
  I need to browse an OPC package item formatted for readability

  Scenario Outline: Browse the content types item of a package
      When I issue a command to browse the content types of a <pkg_type> package
      Then the formatted content types item appears on stdout

  Examples: Package Types
    | pkg_type |
    |   zip    |
    |   dir    |
