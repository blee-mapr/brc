#!/Users/blee/workspace/blee/brcli/venv/bin/python

import os
import sys
import logging
import configargparse
import sh
from sh import rsync
import componentcopy
import reindex


def setup():
    p = configargparse.ArgParser(default_config_files=['./config.ini'])
    p.add('command', nargs='+', help='Main command task')
    options = p.parse_known_args()
    return options[0]


def main():
    options = setup()
    cmd = options.command[0]
    if cmd == 'copy':
        cc = componentcopy
        cc.doComponentCopy()
    elif cmd == 'json':
        cc = componentcopy
        cc.generateJson()
    elif cmd == 'reindex':
        ri = reindex
        ri.doReindex()
    else:
        print 'Unknown command given: %s' % cmd
    return 0


if __name__ == "__main__":
    main()
