#!/usr/bin/env python3

import dropbox
import argparse
from stopwatch import Stopwatch
import os
import sys
import pprint
from bytecnt import Bytecnt
import logging
from util import Util


TOKEN_ENV_VAR = "DROPBOX_TOKEN"
TOKEN = os.getenv(TOKEN_ENV_VAR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get space info from Dropbox')

    parser.add_argument('--token', default=TOKEN,
                        help='Access token '
                        '(see https://www.dropbox.com/developers/apps)')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Enable debug prints')
    args = parser.parse_args()

    logger = Util.setup_logging(os.path.basename(sys.argv[0]), args.debug)

    if not args.token:
        print("--token or {} envronment variable is mandatory".
              format(TOKEN_ENV_VAR))
        sys.exit(2)

    dbx = dropbox.Dropbox(args.token)

    with Stopwatch.stopwatch('spaceUsage'):
        su = dbx.users_get_space_usage()

    # XXX should check is_individual()
    ia = su.allocation.get_individual()
    acct = dbx.users_get_current_account()
    pct = su.used / ia.allocated
    print("User {} used {} out of {} (at {}% capacity)".
          format(acct.name.display_name, Bytecnt.bytecnt_to_str(su.used),
                 Bytecnt.bytecnt_to_str(ia.allocated), int(pct)))
