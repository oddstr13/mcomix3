User under win32 should use `original mcomix`_.

=======
MComix3
=======

|quality gate| |license| |tests| |release| |bugs|

|maintainability rating| |reliability rating| |security rating| |technical debt|


Fork from MComix gtk3 branch, switch to python3.

Only tested under Linux.

Required:
---------
- **Python3** 3.5 or later. `1`_
- **PyGObject** 3.24 or later `2`_, with **GTK+ 3 gir bindings** 3.22 or later.
- **Pillow** 5.2.0 or later. `3`_ (`Latest version`_ is always recommended)

Recommended:
------------
- **unrar**, **rar** or **libunrar** to extract RAR archives. `4`_
- **7z** `5`_ (**p7zip** `6`_ for POSIX system) to extract 7Z and LHA archives.
- **p7zip** with rar codec (**p7zip-rar** on Debian-like systems, providing ``Codecs/Rar.so`` file) to extract RAR archives.
- **lha** `7`_ to extract LHA archives.
- **mupdf** `8`_ for PDF support.
- **libflif_dec** or **libflif** `9`_ for FLIF support.

Run:
----
``python3 mcomix/mcomixstarter.py <diretory, archive or image>``

Install:
--------
**setup.py is not working**

``python3 installer.py --srcdir=mcomix --target=<somewhere>``

then:

``python3 <somewere>/mcomix/mcomixstarter.py <directory, archive or image>``

.. _original mcomix: https://sourceforge.net/projects/mcomix/
.. _1: https://www.python.org/downloads/
.. _2: https://pygobject.readthedocs.io/
.. _3: https://pillow.readthedocs.io/
.. _Latest version: https://pypi.org/project/Pillow/
.. _4: https://www.rarlab.com/rar_add.htm
.. _5: https://www.7-zip.org/
.. _6: http://p7zip.sourceforge.net/
.. _7: https://fragglet.github.io/lhasa/
.. _8: https://mupdf.com/
.. _9: https://github.com/FLIF-hub/FLIF


.. |quality gate| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=oddstr13_mcomix3
    :alt: Quality Gate Status

.. |license| image:: https://img.shields.io/github/license/oddstr13/mcomix3
    :target: https://github.com/oddstr13/mcomix3/blob/odd-choices/COPYING
    :alt: License

.. |tests| image:: https://github.com/oddstr13/mcomix3/workflows/Python%20tests/badge.svg
    :target: https://github.com/oddstr13/mcomix3/actions?query=workflow%3A%22Python+tests%22
    :alt: GitHub Workflow Status

.. |release| image:: https://img.shields.io/github/v/release/oddstr13/mcomix3
    :target: https://github.com/oddstr13/mcomix3/releases
    :alt: GitHub Release

.. |maintainability rating| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=sqale_rating
    :alt: Maintainability rating

.. |reliability rating| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=reliability_rating
    :alt: Reliability rating

.. |security rating| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=security_rating
    :alt: Security rating

.. |technical debt| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=sqale_index
    :alt: Technical debt

.. |bugs| image:: https://sonarcloud.io/api/project_badges/measure?project=oddstr13_mcomix3&metric=bugs
    :alt: Bugs
