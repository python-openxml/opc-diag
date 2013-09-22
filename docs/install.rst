.. _install:

Installation
============


Installing with pip
-------------------

For many users, installation is as simple as executing the following from the
command line::

   $ pip install opc-diag

There are, however, some common difficulties:

|opcd| depends on the ``lxml`` Python package, which cannot reliably be
installed by ``pip`` or ``easy_install`` on Windows. Building it from source
requires a compiler and other items the typical Windows user will not have
installed. Therefore we recommend Windows users manually install |lxml| using
a GUI installer before installing |opcd|. For that, the precompiled binaries at
http://www.lfd.uci.edu/~gohlke/pythonlibs/ have been the best source so far.

|lxml| depends on the ``libxslt`` and ``libxml2`` libraries. If those are not
present the |lxml| build will fail during the install. Linux users shouldn't
have too much trouble as these libraries are commonly installed by default. If
not, ``yum`` or ``apt-get`` is your friend for getting them installed. OS
X users running recent versions may also find these already installed. If not,
they can be installed using Homebrew.


Getting the Code
----------------

opc-diag is developed on GitHub, where the code is
`freely available <https://github.com/python-openxml/opc-diag>`_.

You can clone the repository like this::

    git clone git://github.com/python-openxml/opc-diag.git
