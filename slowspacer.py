#!/usr/bin/env python
'''Slowspacer: While tailing logs, add some space and a marker between old and new logs

Ever try to debug something by watching a log and get confused about which log lines were new
and which were stale and already there?  Pipe your tail to slowspacer and after receiving no logs
for N seconds (default is 3), it will add space and a marker to create visual separation between
batches of logs.

TODO: This depends on Python, and it would be nice to rewrite it in C or Rust so it didn't.

Example: tail -f /var/log/yourlog.log | slowspacer
'''

__author__ = "James Lee"
__license__ = "CC0 Public Domain"
__email__ = "jimmybot@jimmybot.com"

import fcntl
import os
import select
import time

def _no_block_read(infile):
    try:
        line = infile.readline()

    # Reading will not block with the nonblocking attribute set
    # If there is nothing to read, instead of blocking, IOError is raised
    except IOError:
        line = None

    return line

def watch(logfile, timeout=3, spacer='='):
    is_spaced = False
    spacer_line = spacer * 80

    # default is that reading stdin will block if no data is ready to be read
    # we use fcntl to set reading to non-blocking
    fcntl.fcntl(logfile.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    while True:
        # either data is available to be read or we may need to add a spacer
        rfiles, wfiles, xfiles = select.select([logfile], [], [], timeout)

        # select says we're ready to read
        if rfiles:
            # normally we should not block here but
            # we can get one if a partial line was written
            # in this case, our behavior is to *not* output the partial line
            line = _no_block_read(rfiles[0])
            if line and len(line):
                # we have real content again, reset is_spaced to False
                is_spaced = False
                while line and len(line):
                    print line,
                    line = _no_block_read(rfiles[0])

        # select timed-out with nothing available to read, let's print a spacer
        else:
            # check if a spacer was already printed before printing
            # (no need to print consecutive spacers)
            if not is_spaced:
                is_spaced = True
                print
                print spacer_line
                print

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--seconds', metavar='S', default='3', type=int, help='number of seconds to wait before adding a spacer (default is 3)')
    parser.add_argument('-c', '--character', metavar='C', default='=', type=str, help='character used as a spacer (default is \'=\')')
    args = parser.parse_args()

    watch(sys.stdin, args.seconds, args.character)
