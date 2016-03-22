import os
import sys
import json
import configargparse
import sh

REINDEX_CMD_LIST = {'r': 'createrepo .', 'u': 'updatearchive.sh'}
BASE_DIR = '/root/stage.mapr.com/backups/releases'
ECO_4X_DIR = BASE_DIR + '/ecosystem-4.x'
ECO_5X_DIR = BASE_DIR + '/ecosystem-5.x'
ECO_DIR_DICT = {'4': ECO_4X_DIR, '5': ECO_5X_DIR}


def setup():
    p = configargparse.getArgumentParser()
    p.add_argument('-d', '--dest', required=True, help='Destination - Example: 4ru = ecosystem4 redhat and ubuntu, supports multiple comma separated values ie. 4ru,5ru')
    try:
        options = p.parse_known_args()
    except:
        print(p.format_help())
        sys.exit(0)

    return options[0]


def doReindex():
    options = setup()
    ecoList = options.dest.split(',')

    for eco in ecoList:
        destEco = eco[0]
        destOS = eco[1:]

        for os in destOS:
            # Recreate the index for the repository
            if os is 'r':
                print 'Recreating index for Redhat: %s' % REINDEX_CMD_LIST['r']
                # sh.cd(ECO_DIR_DICT[destEco])
                run = sh.Command('which createrepo')
                run()
            elif os is 'u':
                print 'Recreating index for Ubuntu: %s' % REINDEX_CMD_LIST['u']
            else:
                print 'This is an invalid OS'


if __name__ == "__main__":
    doReindex()
