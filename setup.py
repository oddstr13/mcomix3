#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import

""" MComix installation routines.

Example usage:
    Normal installation (all files are copied into a directory in python/lib/site-packages/mcomix)
    $ ./setup.py install

    For distribution packaging (All files are installed relative to /tmp/mcomix)
    $ ./setup.py install --single-version-externally-managed --root /tmp/mcomix --prefix /usr
"""

import os
import re

from glob import glob
from setuptools import setup, find_packages


with open('mcomix/__init__.py', 'r') as fh:
    version = re.search(r'__version__ *= *(["\'])(.*?[^\\])\1', fh.read()).group(2)


with open("README.rst", "r") as fh:
    long_description = fh.read()


with open("requirements.txt", "r") as fh:
    requirements = []
    for line in fh.readlines():
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)


setup(
    name='mcomix',
    version=version,
    packages=find_packages(exclude=['test*']),
    package_data={
        'mcomix': [
            'messages/*/*/*.mo',
            'images/*.png',
            'images/*/*.png',
        ],
    },
    entry_points={
        'console_scripts': [
            'mcomix = mcomix.__main__:run',
            'comicthumb = mcomix.comicthumb:main'
        ],
        'setuptools.installation': [
            'eggsecutable = mcomix.__main__:run'
        ],
        'mcomix.plugins': [
            'ArchiveReader = mcomix.plugins.foo_plugin:TestArchiveReader',
            'ArchiveReader 2 = mcomix.plugins.foo_plugin:Potatoe',
            'ArchiveReader 3 = mcomix.plugins.foo_plugin:ErroringPotatoe',
        ],
    },
    test_suite="test",
    install_requires=requirements,
    zip_safe=True,

    # Various MIME files that need to be copied to certain system locations on Linux.
    # Note that these files are only installed correctly if
    # --single-version-externally-managed is used as argument to "setup.py install".
    # Otherwise, these files end up in a MComix egg directory in site-packages.
    # (Thank you, setuptools!)
    data_files=[
        ('share/man/man1', glob('man/*')),
        ('share/applications', ['mime/mcomix.desktop']),
        ('share/appdata', ['mime/mcomix.appdata.xml']),
        # ('share/mime/packages', ['mime/mcomix.xml']),
        ('share/icons/hicolor/16x16/apps', ['mcomix/images/16x16/mcomix.png']),
        ('share/icons/hicolor/22x22/apps', ['mcomix/images/22x22/mcomix.png']),
        ('share/icons/hicolor/24x24/apps', ['mcomix/images/24x24/mcomix.png']),
        ('share/icons/hicolor/32x32/apps', ['mcomix/images/32x32/mcomix.png']),
        ('share/icons/hicolor/48x48/apps', ['mcomix/images/48x48/mcomix.png']),
        ('share/icons/hicolor/16x16/mimetypes', glob('mime/icons/16x16/*.png')),
        ('share/icons/hicolor/22x22/mimetypes', glob('mime/icons/22x22/*.png')),
        ('share/icons/hicolor/24x24/mimetypes', glob('mime/icons/24x24/*.png')),
        ('share/icons/hicolor/32x32/mimetypes', glob('mime/icons/32x32/*.png')),
        ('share/icons/hicolor/48x48/mimetypes', glob('mime/icons/48x48/*.png')),
    ],

    # Package metadata
    author='Ark',
    author_email='https://sourceforge.net/u/aaku/profile/',
    maintainer='Odd Stråbø',
    maintainer_email='oddstr13@openshell.no',
    url='https://mcomix.sourceforge.net',
    description='GTK comic book viewer',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="License :: OSI Approved :: GNU General Public License (GPL)",
    download_url="https://sourceforge.net/projects/mcomix/files",
    platforms=[
        'Operating System :: POSIX :: Linux',
        # 'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD',
    ],
)
