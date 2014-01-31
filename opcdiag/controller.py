# -*- coding: utf-8 -*-

"""
Command-line application controller for opc-diag
"""

from opcdiag.model import Package
from opcdiag.presenter import DiffPresenter, ItemPresenter
from opcdiag.view import OpcView


_CONTENT_TYPES_URI = '[Content_Types].xml'


class OpcController(object):
    """
    Mediate between the command-line interface and the package model
    entities, orchestrating the execution of user commands by creating
    entity objects, delegating work to them, and using the appropriate view
    object to format the results to be displayed.
    """
    def browse(self, pkg_path, uri_tail):
        """
        Display pretty-printed XML contained in package item with URI ending
        with *uri_tail* in package at *pkg_path*.
        """
        pkg = Package.read(pkg_path)
        pkg_item = pkg.find_item_by_uri_tail(uri_tail)
        item_presenter = ItemPresenter(pkg_item)
        OpcView.pkg_item(item_presenter)

    def diff_item(self, package_1_path, package_2_path, uri_tail):
        """
        Display the meaningful differences between the item identified by
        *uri_tail* in the package at *package_1_path* and its counterpart in
        the package at *package_2_path*. Each path can be either a standard
        zip package (e.g. a .pptx file) or a directory containing an extracted
        package.
        """
        package_1 = Package.read(package_1_path)
        package_2 = Package.read(package_2_path)
        diff = DiffPresenter.named_item_diff(package_1, package_2, uri_tail)
        OpcView.item_diff(diff)

    def diff_pkg(self, package_1_path, package_2_path):
        """
        Display the meaningful differences between the packages at
        *package_1_path* and *package_2_path*. Each path can be either a
        standard zip package (e.g. .pptx file) or a directory containing an
        extracted package.
        """
        package_1 = Package.read(package_1_path)
        package_2 = Package.read(package_2_path)
        content_types_diff = DiffPresenter.named_item_diff(
            package_1, package_2, _CONTENT_TYPES_URI)
        rels_diffs = DiffPresenter.rels_diffs(package_1, package_2)
        xml_part_diffs = DiffPresenter.xml_part_diffs(package_1, package_2)
        OpcView.package_diff(content_types_diff, rels_diffs, xml_part_diffs)

    def extract_package(self, package_path, extract_dirpath):
        """
        Extract the contents of the package at *package_path* to individual
        files in a directory at *extract_dirpath*.
        """
        package = Package.read(package_path)
        package.prettify_xml()
        package.save_to_dir(extract_dirpath)

    def repackage(self, package_path, new_package_path):
        """
        Write the contents of the package found at *package_path* to a new
        zip package at *new_package_path*.
        """
        package = Package.read(package_path)
        package.save(new_package_path)

    def substitute(self, uri_tail, src_pkg_path, tgt_pkg_path, new_pkg_path):
        """
        Substitute the package item identified by *uri_tail* from the package
        at *src_pkg_path* into the package at *tgt_pkg_path* and save the
        resulting package at *new_pkg_path*. This can be handy for
        identifying which package item(s) in the source package are causing a
        "repair needed" error when loading the target package in MS Office.
        """
        package_1 = Package.read(src_pkg_path)
        package_2 = Package.read(tgt_pkg_path)
        pkg_item = package_1.find_item_by_uri_tail(uri_tail)
        package_2.substitute_item(pkg_item)
        package_2.save(new_pkg_path)
        OpcView.substitute(pkg_item.uri, src_pkg_path, tgt_pkg_path,
                           new_pkg_path)
