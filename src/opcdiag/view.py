"""Objects that fulfill the view role in opc-diag, interfacing to the console."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from opcdiag.presenter import ItemPresenter


def _write(text: str):
    """Write *text* to stdout."""
    sys.stdout.write(text)


class OpcView:
    """Interfaces to the console by formatting command results for proper display."""

    @staticmethod
    def item_diff(diff: str):
        """Display *diff*, a standard unified_diff string, on stdout."""
        text = ""
        if diff:
            text += "%s\n" % diff
        _write(text)

    @staticmethod
    def package_diff(
        content_types_diff: str, rels_diffs: Iterable[str], xml_part_diffs: Iterable[str]
    ):
        """Write a consolidated diff between two packages to stdout.

        Includes its *content_types_diff*, any *rels_diffs*, and any *xml_part_diffs*.
        """
        diff_blocks = [content_types_diff] if content_types_diff else []
        diff_blocks.extend(rels_diffs)
        diff_blocks.extend(xml_part_diffs)
        text = "%s\n" % "\n\n".join(diff_blocks) if diff_blocks else ""
        _write(text)

    @staticmethod
    def pkg_item(presenter: ItemPresenter):
        """Display the text value of pkg_item, adding a linefeed at end to make terminal happy."""
        text = "%s\n" % presenter.text
        _write(text)

    @staticmethod
    def substitute(uri: str, src_pkg_path: str, tgt_pkg_path: str, new_pkg_path: str):
        """
        Display a confirmation method detailing the package item substitution
        that was executed.
        """
        msg = "substituted '%s' from '%s' into '%s' and saved the result as" " '%s'\n" % (
            uri,
            src_pkg_path,
            tgt_pkg_path,
            new_pkg_path,
        )
        msg = msg.replace("\\", "/")  # normalize directory separator
        _write(msg)
