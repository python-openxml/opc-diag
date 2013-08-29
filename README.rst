*opc-diag* is a command-line application for exploring Microsoft Word, Excel,
and PowerPoint files from Office 2007 and later. Also known as *Office Open
XML*, the structure of these files adheres to the Open Packaging Convention
(OPC), specified by ISO/IEC 29500.

*opc-diag* provides the ``opc`` command, which allows OPC files to be browsed,
diff-ed, extracted, repackaged, and parts from one to be substituted into
another.

Its primary use is by developers of software that generates and/or
manipulates Microsoft Office documents.

A typical use would be diff-ing a Word file from before and after an operation,
say inserting picture, to identify the specific changes Word made to the XML.
This is handy when one is developing software to do the same without Word's
help::

   $ opc diff before.docx after.docx

Another main use is to diagnose an issue causing an Office document to not load
cleanly, typically because the software that generated it has a bug. These
problems can be tedious and often difficult to diagnose without tools like
*opc-diag*, and were the primary motivation for developing it.

More information is available in the `opc-diag documentation`_.

.. _`opc-diag documentation`:
   https://opc-diag.readthedocs.org/en/latest/
