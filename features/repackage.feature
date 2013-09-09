Feature: Repackage an extracted OPC package to zip package
  In order to produce an OPC package with hand-modified content
  As an Open XML developer
  I need to repackage an extracted OPC package from its directory into a zip

  @wip
  Scenario: repackage an expanded OPC package from its directory to a zip
      When I issue a command to repackage an expanded package directory
      Then a zip package with matching contents appears at the path I specified
