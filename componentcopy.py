import os
import sys
import json
import configargparse
import sh
from sh import cp, rm
from sh import rsync
log = open('/root/blee-temp/scripts/brc/logfile.txt', 'w+')

# eco4Directory=/root/stage.mapr.com/backups/releases/ecosystem-4.x
# eco5Directory=/root/stage.mapr.com/backups/releases/ecosystem-5.x
# eco4_redhat=$eco4Directory/redhat
# eco4_ubuntu=$eco4Directory/ubuntu/dists/binary
# eco5_redhat=$eco5Directory/redhat
# eco5_ubuntu=$eco5Directory/ubuntu/dists/binary

rsync = rsync.bake('-av')

OS_LIST = {'r': 'redhat', 'u': 'ubuntu'}
PACKAGETYPE_DICT = {'redhat': 'redhat', 'ubuntu': 'ubuntu/dists/binary'}
PKG_DICT = {'r': 'yum/qa/opensource.release', 'u': 'qa/opensource.release/dists/binary'}
BASE_DIR = '/root/stage.mapr.com/backups/releases'
ECO_4X_DIR = BASE_DIR + '/ecosystem-4.x'
ECO_5X_DIR = BASE_DIR + '/ecosystem-5.x'
ECO_DIR_DICT = {'4': ECO_4X_DIR, '5': ECO_5X_DIR}
RELEASE_DIR = '/home/MAPRTECH/share/packages'


def setup():
    p = configargparse.getArgumentParser()
    p.add_argument('-c', '--component', required=True, help='Component [name]-[version]. ie: hbase-1.1.1')
    # p.add_argument('--cname', required=True, help='Component Name')
    # p.add_argument('--cver', required=True, help='Component Version')
    p.add_argument('--dest', required=True, help='Destination - Example: 4ru = ecosystem4 redhat and ubuntu, supports multiple comma separated values ie. 4ru,5ru')
    try:
        options = p.parse_known_args()
    except:
        print(p.format_help())
        sys.exit(0)

    return options[0]


def generateJson():
    options = setup()
    ecoList = options.dest.split(',')
    data = {}

    for eco in ecoList:
        destEco = eco[0]
        destOS = eco[1:]
        pattern = '*%s*%s*' % (options.cname, options.cver)

    data['components'] = [{'name': options.cname, 'version': options.cver, 'ecosytems': []}]
    data['components'][0]['ecosytems'] = {'version': '4.x'}

    print json.dumps(data)

    with open('test.json', 'w') as fh:
        json.dump(data, fh, sort_keys=True, indent=4, ensure_ascii=False)


def doComponentCopy():
    options = setup()
    print('Doing component copy: %s' % options.component)
    cname, cver = options.component.split('-')
    ecoList = options.dest.split(',')

    for eco in ecoList:
        destEco = eco[0]
        destOS = eco[1:]
        pattern = '*%s*%s*' % (cname, cver)

        for operSys in destOS:
            print('Copying %s-%s to Ecosystem %s.x -> %s' % (cname, cver, destEco, OS_LIST[operSys]))
            # Remove existing files of the same component/version
            WORKDIR = '%s/%s' % (ECO_DIR_DICT[destEco], PACKAGETYPE_DICT[OS_LIST[operSys]])
	    os.chdir(WORKDIR)
            rm('-fv', sh.glob(pattern), _out=log)
            # Rsync over the new files
            RSYNC_SRC = '%s/%s/%s' % (RELEASE_DIR, PKG_DICT[operSys], pattern)
            rsync(sh.glob('%s' % RSYNC_SRC), '.')
    return 0


if __name__ == "__main__":
    setup()
    # options = p.parse_known_args()
