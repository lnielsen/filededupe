# -*- coding: utf-8 -*-
#
# This file is part of File Dedupe
# Copyright (C) 2015 Lars Holm Nielsen.
#
# File Dedupe is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Utility methods."""

from __future__ import absolute_import, unicode_literals, print_function

from fs.opener import opener
from fs.path import join

import zlib
from difflib import SequenceMatcher


def path_to_fs(path):
    """Convert path to an FS object."""
    return opener.opendir(path)


def list_files(fs):
    """Get a list of filenames and locations."""
    for d, filenames in fs.walk():
        for f in filenames:
            p = join(d, f)
            yield f, dict(
                path=p,
                fullpath=(
                    fs.getsyspath(p) if fs.hassyspath(p) else fs.getpathurl(p)
                ),
            )


def checksumfile(fs, path):
    """Compute adler32 checksum of file."""
    value = zlib.adler32("")

    with fs.open(path, 'rb') as f:
        for data in f:
            value = zlib.adler32(data, value)

    return value


def compare(file_a, file_b, filename_func=None):
    """Compare two files."""
    name_a, name_b = file_a[0], file_b[0]
    # data_a, data_b = file_a[1], file_b[1]

    if filename_func is not None:
        name_a = filename_func(name_a)
        name_b = filename_func(name_b)

    if SequenceMatcher(None, name_a, name_b).ratio() > 0.9:
        return True
    return False
