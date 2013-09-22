.. _quickstart:

Quickstart
==========


Use Case 1: ``diff`` two versions of an Office document
-------------------------------------------------------

In order to determine what changes a particular operation makes to the
underlying XML in a document, an OpenXML developer can use |opcd| to 'diff'
a before and after version.

The command:

.. code-block:: bash

    $ opc diff before.docx after.docx

might present output like this when a new paragraph is added to a Word file:

.. code-block:: diff

    --- before/word/document.xml

    +++ after/word/document.xml

    @@ -20,11 +20,16 @@

         mc:Ignorable="w14 wp14"
         >
       <w:body>
    -    <w:p w:rsidR="0015074B" w:rsidRDefault="0015074B">
    +    <w:p w:rsidR="0015074B" w:rsidRDefault="006E20C4">
    +      <w:r>
    +        <w:t>New paragraph</w:t>
    +      </w:r>
    +    </w:p>
    +    <w:p w:rsidR="006E20C4" w:rsidRDefault="006E20C4">
           <w:bookmarkStart w:id="0" w:name="_GoBack"/>
           <w:bookmarkEnd w:id="0"/>
         </w:p>
    -    <w:sectPr w:rsidR="0015074B" w:rsidSect="00034616">
    +    <w:sectPr w:rsidR="006E20C4" w:rsidSect="00034616">
           <w:pgSz w:w="12240" w:h="15840"/>
           <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
           <w:cols w:space="720"/>

From this we can see that Word inserted a new ``<w:p>`` (paragraph) element
containing a ``<w:r>`` (run) element which itself contains a ``<w:t>`` (text)
element which in turn contains the added text. In addition, it updated the
``w:rsidRDefault`` attribute of the paragraph and other rsid-related attributes
on the ``<w:sectPr>`` (section) element. The rsid-prefixed attributes are part
of the mechanism Word uses to track revisions.

This capability comes in handy when you want to figure out how a document
feature is implemented in OpenXML so you can write code to make the same sort
of changes. It can also be handy for isolating a change your code made that's
causing a document to no longer load cleanly.


Use Case 2: ``browse`` a part in an Office Document
---------------------------------------------------

In order to closely examine the XML of an Office document part, perhaps to
confirm the XML is being generated correctly or to get a general overview of
the XML for a particular part, an OpenXML developer can use |opcd| to browse
a *part* contained in an OPC document.

In OPC terminology, a document file, e.g. ``example.docx``, is known as
a *package*. In common-sense terms, a package is a zip archive containing
a number of files arranged in a specific directory hierarchy. If you unzip the
file, that's exactly what you'll get. An individual "file" in a package is
known as a *package item*, some of which are known as a *part*. It's not
uncommon to simply refer to any of them as a *part* or *package part*.

The command:

.. code-block:: bash

    $ opc browse example.docx core.xml

presents output that looks something like this:

.. code-block:: xml

    <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <cp:coreProperties
        xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcmitype="http://purl.org/dc/dcmitype/"
        xmlns:dcterms="http://purl.org/dc/terms/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        >
      <dc:title/>
      <dc:subject/>
      <dc:creator>Steve Canny</dc:creator>
      <cp:keywords/>
      <dc:description/>
      <cp:lastModifiedBy>Steve Canny</cp:lastModifiedBy>
      <cp:revision>1</cp:revision>
      <dcterms:created xsi:type="dcterms:W3CDTF">2013-09-21T23:52:00Z</dcterms:created>
      <dcterms:modified xsi:type="dcterms:W3CDTF">2013-09-21T23:53:00Z</dcterms:modified>
    </cp:coreProperties>

``core.xml`` is a part that all OpenXML files produced by an Office application
will contain. It's relatively short, which is why I chose it for this example.

You can see that |opcd| has taken care of extracting it from the .docx file
and formatting the XML for readability, including indenting each of the
namespace declarations onto a line of its own. It also doesn't leave extracted
zip directories hanging around on the filesystem. These are some of the basic
capabilities that reduce the tedium in exploring OpenXML files.


Use Case 3: ``diff`` a part between two Office Documents
--------------------------------------------------------

Once you've narrowed down the relevant differences between two documents to
a specific part, the ``diff-item`` subcommand allows you to limit the diff to
a particular part that appears in both packages.

Extending the prior two examples, say we wanted to focus our attention on the
differences between the ``/docProps/core.xml`` part in two documents.

The command:

.. code-block:: bash

    $ opc diff-item before.docx after.docx core.xml

presents output that looks something like this:

.. code-block:: diff

    --- before/docProps/core.xml

    +++ after/docProps/core.xml

    @@ -12,7 +12,7 @@

       <cp:keywords/>
       <dc:description/>
       <cp:lastModifiedBy>Steve Canny</cp:lastModifiedBy>
    -  <cp:revision>1</cp:revision>
    -  <dcterms:created xsi:type="dcterms:W3CDTF">2013-09-21T23:52:00Z</dcterms:created>
    -  <dcterms:modified xsi:type="dcterms:W3CDTF">2013-09-21T23:52:00Z</dcterms:modified>
    +  <cp:revision>2</cp:revision>
    +  <dcterms:created xsi:type="dcterms:W3CDTF">2013-09-21T23:53:00Z</dcterms:created>
    +  <dcterms:modified xsi:type="dcterms:W3CDTF">2013-09-21T23:53:00Z</dcterms:modified>
     </cp:coreProperties>

You can see that Word incremented the ``<cp:revision>`` element and updated the
``<dcterms:created>`` and ``<dcterms:modified>`` elements.


Use Case 4: ``extract`` a package to a directory
------------------------------------------------

There are a number of situations in which it's useful to break a package file
into its parts and perhaps to put it back together again later. The ``extract``
subcommand provides the first half of this process, complemented by the
``repackage`` subcommand discussed next.

The command:

.. code-block:: bash

    $ opc extract example.xlsx example_dir

will extract all the package items in ``example.xlsx`` into the directory
example_dir. The hierarchy of the package item names forms the structure of
subdirectories that are created in ``example_dir``. For example, the main
workbook will be found at ``example_dir/xl/workbook.xml`` and the thumbnail
image that may appear in a desktop icon for the file is found at
``example_dir/docProps/thumbnail.jpeg``.

Users on a \*nix operating system can accomplish much the same thing with the
command:

.. code-block:: bash

    $ unzip example.xlsx -d example_dir

but I thought it might be handy from time to time to have it built into |opcd|.


Use Case 5: ``repackage`` a package directory into a file
---------------------------------------------------------

As a complement to the ``extract`` subcommand, ``repackage`` allows a directory
containing a set of package files to be reassembled into a single file.

This enables some useful workflows, one of which is using the directory as
a sort of "source code" tree for a document which can be "compiled" into
a (hopefully) working Office document. A typical use would be to try out some
proposed changes by hand, editing the XML directly, then opening the
resulting packing in Office to see how it renders.

Theoretically it could be used in a production workflow of some type where one
or more of the XML parts was formed with a templating system, but I haven't
tried that.

The command:

.. code-block:: bash

    $ opc repackage example_dir example.xlsx

will reassemble the package item files found in ``example_dir`` into a package
at ``example.xlsx``.


Use Case 6: ``substitute`` a part from one package into another
---------------------------------------------------------------

Which brings us to the final subcommand, ``substitute``.

Perhaps the most vexing challenge one encounters as an OpenXML developer is the
dreaded "requires repair" error. This is when you create an Office document
that can't be loaded by Office. Typically, you are presented with an error
like:

    *PowerPoint found a problem with content in the file example.pptx.
    PowerPoint can attempt to repair the file ...*.

Often, the Office application can fix the file if you press the "Repair"
button, but it tells you nothing about what the problem was. If everything
worked fine before your last code change, you might have a good idea where to
look. Sometimes however, you have little in the way of clues and you are
visited by the unsettling realization that it could essentially be anything.

This is where ``substitute`` is a big help. It allows you to individually
substitute suspect parts from a broken file into a working one. (Using the
repair capability of the Office applications can often provide you with
a working version of the file to complement the broken one you've built.) If
the new file works, you've ruled out the substituted part. If the new file is
broken, you can focus on the differences between the two versions of that
specific part using ``diff-item``. In the needle in a haystack situation, this
helps narrow your focus to 5-10% of the haystack.

The command:

.. code-block:: bash

    $ opc substitute core.xml broken.docx working.docx trial.docx

combines the ``/docProps/core.xml`` part from ``broken.docx`` with all the
parts *except* ``core.xml`` from ``working.docx``, and saves the resulting
package as ``trial.docx``.

There are a lot of parameters to this command, so it prints the following
confirmation to ensure you asked for what you actually intended::

    substituted 'docProps/core.xml' from 'broken.docx' into 'working.docx' and saved the result as 'trial.docx'

Note that neither the source package (e.g. ``broken.docx``) nor the target
package (``working.docx`` in this example) are affected by this command. They
simply provide content for the result package (``trial.docx``).
