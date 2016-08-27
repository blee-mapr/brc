import os
import sys
import configargparse
from sh import cp, rm, rsync
import sh

rsync = rsync.bake('-av')

def setup():
	p = configargparse.getArgumentParser()
	try:
		options = p.parse_known_args()
	except Exception, e:
		print e
		sys.exit(1)

	return options[0]

def doInstallerCopy():
	options = setup()
	INSTALLER_VER = 'installer-ui1.3'
	BASE_DIR = '/root/stage.mapr.com/backups/releases'
	RELEASE_DIR = '/home/MAPRTECH/share/packages'	
	RSYNC_EXTRA_OPTS = '--progress'

	# Put mapr-setup.sh on root for installer folder	
	output = rsync(RSYNC_EXTRA_OPTS, '%s/yum/qa/%s/mapr-setup.sh' % (RELEASE_DIR, INSTALLER_VER), '%s/installer/' % BASE_DIR)

	# Redhat
	RSYNC_SRC = '%s/yum/qa/%s/mapr-*' % (RELEASE_DIR, INSTALLER_VER)
	output = rsync(RSYNC_EXTRA_OPTS, sh.glob(RSYNC_SRC), '%s/installer/redhat/' % BASE_DIR)

	# Ubuntu
	RSYNC_SRC = '%s/qa/%s/mapr-*' % (RELEASE_DIR, INSTALLER_VER)
	output = rsync(RSYNC_EXTRA_OPTS, sh.glob(RSYNC_SRC), '%s/installer/ubuntu/' % BASE_DIR) 

	RSYNC_SRC = '%s/qa/%s/dists/binary/mapr-*' % (RELEASE_DIR, INSTALLER_VER)
	output = rsync(RSYNC_EXTRA_OPTS, sh.glob(RSYNC_SRC), '%s/installer/ubuntu/dists/binary/' % BASE_DIR) 


if __name__ == "__main__":
	setup()
	doInstallerCopy()