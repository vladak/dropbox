#!/usr/bin/env python3

import dropbox
import argparse
from stopwatch import Stopwatch
import os
import sys
import pprint
import dbox
from stopwatch import Stopwatch
from pprint import pprint
import logging
from util import Util


TOKEN_ENV_VAR = "DROPBOX_TOKEN"
TOKEN = os.getenv(TOKEN_ENV_VAR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download file from Dropbox')

    parser.add_argument('--token', default=TOKEN,
                        help='Access token '
                        '(see https://www.dropbox.com/developers/apps)')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Enable debug prints')
    parser.add_argument('file', metavar='file', type=str, nargs=1,
                        help='file to download')
    parser.add_argument('destination', metavar='dst', type=str, nargs='?',
                        help='destination path. If not set, the file will '
                        'be downloaded to current directory', default=None)
    args = parser.parse_args()

    logger = Util.setup_logging(os.path.basename(sys.argv[0]), args.debug)

    if not args.token:
        print("--token or {} envronment variable is mandatory".
              format(TOKEN_ENV_VAR))
        sys.exit(2)

    dbx = dropbox.Dropbox(args.token)

    src = args.file[0]
    logger.debug(src)
    data = dbox.download(dbx, logger, src)
    if args.destination:
        dst = args.destination
    else:
        dst = os.path.basename(src)
    with open(dst, 'wb') as f:
        f.write(data)
    # XXX verify content hash
