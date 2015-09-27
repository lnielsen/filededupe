# This file is part of File Dedupe
# Copyright (C) 2015 Lars Holm Nielsen.
#
# File Dedupe is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

pep257 filededupe && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test && \
sphinx-build -qnNW -b doctest docs docs/_build/doctest
