# -*- coding: utf-8 -*-

''' Unicode-aware wrapper for tarfile.TarFile. '''

import os
import tarfile
from mcomix.archive import archive_base

class TarArchive(archive_base.NonUnicodeArchive):
    def __init__(self, archive):
        super(TarArchive, self).__init__(archive)
        # Track if archive contents have been listed at least one time: this
        # must be done before attempting to extract contents.
        self._contents_listed = False
        self._contents = []
        self._contents_info = []
        self.tar = None

    def is_solid(self):
        return True

    def iter_contents(self):
        if not self._contents_listed:
            if not self.tar:
                # Make sure we start back at the beginning of the tar.
                self.tar = tarfile.open(self.archive, 'r:*')
            self._contents.clear()
            self._contents_info.clear()
            self._contents_info.extend(((self._unicode_filename(info.name), info)
                                        for info in self.tar.getmembers()))
            self._contents.extend((name for name, info in self._contents_info))
            self._contents_listed = True
        yield from self._contents

    def list_contents(self):
        return [filename for filename in self.iter_contents()]

    def extract(self, filename, destination_dir):
        if not self._contents_listed:
            self.list_contents()
        original_filename = self._original_filename(filename)
        destination_path = os.path.join(destination_dir, filename)
        self.tar.extract(original_filename, path=destination_dir)
        if original_filename is not filename:
            os.rename(os.path.join(destination_dir, original_filename),
                      destination_path)
        return destination_path

    def iter_extract(self, entries, destination_dir):
        if not self._contents_listed:
            self.list_contents()
        # generate members from entries, same order as getmembers
        infos = []
        names = []
        for name, info in self._contents_info:
            if name in entries:
                infos.append(info)
                names.append(name)
        self.tar.extractall(path=destination_dir, members=infos)
        yield from names

    def close(self):
        if self.tar is not None:
            self.tar.close()
            self.tar = None

# vim: expandtab:sw=4:ts=4
