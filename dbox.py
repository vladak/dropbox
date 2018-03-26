#!/usr/bin/env python3

import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import dropbox
from stopwatch import Stopwatch


def normalize_path(path):
    while '//' in path:
        path = path.replace('//', '/')
    return path


def list_folder(dbx, logger, folder, subfolder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    path = normalize_path(path)
    path = path.rstrip('/')
    try:
        with Stopwatch.stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        logger.error('Folder listing failed for',
                     path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv


def download(dbx, logger, folder, subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    path = normalize_path(path)
    with Stopwatch.stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            logger.error('*** HTTP error', err)
            return None
    data = res.content
    logger.debug(len(data), 'bytes; md:', md)

    return data


def upload(dbx, logger, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    path = normalize_path(path)
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with Stopwatch.stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            logger.error('*** API error', err)
            return None
    logger.debug('uploaded as', res.name.encode('utf8'))

    return res
