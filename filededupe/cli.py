# -*- coding: utf-8 -*-
#
# This file is part of File Dedupe
# Copyright (C) 2015 Lars Holm Nielsen.
#
# File Dedupe is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

u"""Command line interface."""

from __future__ import print_function, absolute_import

import os
import json

import click
from fs.errors import ResourceInvalidError

from .filededupe import compare, list_files, path_to_fs, checksumfile


@click.group()
def cli():
    u"""Small utility for detecting duplicate files."""


@cli.command()
@click.argument('path')
@click.argument('output', type=click.File('wt'))
@click.option('--with-checksum', is_flag=True)
def prepare(path, output, with_checksum):
    u"""Prepare a data file for a directory."""
    try:
        fs = path_to_fs(path)
    except ResourceInvalidError as e:
        raise click.BadParameter(u"%s is not a directory" % e.path)

    click.echo(u"Listing files in %s..." % path)
    files = list(list_files(fs))

    if with_checksum:
        with click.progressbar(files, label=u"Finding checksums") as filelist:
            for f, data in filelist:
                data[u'checksum'] = checksumfile(fs, data[u'path'])

    click.echo(u"Writing data file %s..." % output.name)
    json.dump(files, output)


@cli.command()
@click.argument('src', type=click.File('rt'))
@click.argument('dst', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
def match(src, dst, output):
    u"""Compare files from two JSON data files."""
    click.echo(u"Loading data...")
    src_files = json.load(src)
    dst_files = json.load(dst)

    matches = []
    with click.progressbar(src_files,
                           label=u'Matching files') as files:
        for a in files:
            for b in dst_files:
                if compare(a, b):
                    matches.append((a, b))
                    click.echo(
                        u"Found possible match: %s vs %s" % (a[0], b[0])
                    )

    click.echo(u"Writing data file %s..." % output.name)
    json.dump(matches, output)


@cli.command()
@click.argument('path', type=click.File('rt'))
def inspect(path):
    u"""Compare files from two JSON data files."""
    matches = json.load(path)

    duplicates = map(lambda (a, b): a, matches)

    for f in duplicates:
        if f[0] != '.DS_Store':
            click.echo(f[1]['fullpath'])
            if os.path.exists(f[1]['fullpath']):
                try:
                    os.remove(f[1]['fullpath'])
                except OSError:
                    click.echo("ERROR: Could not remove %s" % f[1]['fullpath'])
