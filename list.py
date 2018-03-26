#!/usr/bin/env python3

import dropbox
import argparse
from stopwatch import Stopwatch
import os
import sys
import pprint
from bytecnt import Bytecnt
import dbox
from stopwatch import Stopwatch
from pprint import pprint
import logging
from util import Util


TOKEN_ENV_VAR = "DROPBOX_TOKEN"
TOKEN = os.getenv(TOKEN_ENV_VAR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List Dropbox folder')

    parser.add_argument('--token', default=TOKEN,
                        help='Access token '
                        '(see https://www.dropbox.com/developers/apps)')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Enable debug prints')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?',
                        help='remote folder', default='')
    args = parser.parse_args()

    logger = Util.setup_logging(os.path.basename(sys.argv[0]), args.debug)

    if not args.token:
        print("--token or {} envronment variable is mandatory".
              format(TOKEN_ENV_VAR))
        sys.exit(2)

    dbx = dropbox.Dropbox(args.token)

    res = dbox.list_folder(dbx, logger, args.folder, '')
    logger.debug(res)
    for key in res.keys():
         print(key)
