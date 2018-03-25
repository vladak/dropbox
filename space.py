#!/usr/bin/env python3

import dropbox
import argparse
import stopwatch
import os
import sys
import pprint
from bytecnt import Bytecnt

# XXX catch exception ? move to main() ?
TOKEN = os.getenv("VARY_TOKEN")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get space info from Dropbox')

    parser.add_argument('--token', default=TOKEN,
                        help='Access token '
                        '(see https://www.dropbox.com/developers/apps)')
    args = parser.parse_args()

    if not args.token:
        print("--token is mandatory")
        sys.exit(2)

    dbx = dropbox.Dropbox(args.token)

    # print(dbx.users_get_current_account())

    # XXX with stopwatch.stopwatch('spaceUsage'):
    su = dbx.users_get_space_usage()
    ia = su.allocation.get_individual()
    bcu = Bytecnt(su.used)
    bca = Bytecnt(ia.allocated)
    # XXX report user
    print("Used {} out of {}".
          format(bcu.bytecnt_to_str(), bca.bytecnt_to_str()))
