# -*- coding: utf-8 -*-
#
# This file is part of File Dedupe
# Copyright (C) 2015 Lars Holm Nielsen.
#
# File Dedupe is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""File Dedupe is a small utility for detecting duplicate files.

Usage:

.. code-block:: console

   $ filededupe prepare /path/to/directory ~/srcfilelist.json
   $ filededupe prepare /path/to/another-directory ~/dstfilelist.json
   $ filededupe match ~/srcfilelist.json ~/dstfilelist.json ~/matches.json
   $ filededupe inspect ~/matches.json
"""

from __future__ import absolute_import, unicode_literals, print_function

from .version import __version__


__all__ = ('__version__',)
