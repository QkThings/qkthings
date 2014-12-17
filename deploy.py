#!/usr/bin/python

from os import getcwd, chdir, path
import os, platform, shutil, datetime, tarfile, distutils.core
from distutils.dir_util import copy_tree, remove_tree, mkpath
import subprocess
from subprocess import call
import argparse
import os, tarfile, datetime
import time

from qkthings.utils import cmd, os_name, make_tarfile, check_path, deploy
	
def main():
	if os_name() == "":
		return

	parser = argparse.ArgumentParser()
	parser.add_argument("--dist", action="store_true", help='create distributable tarball')
	parser.add_argument("--verbose", action="store_true", help='verbose mode')
	args = parser.parse_args()
	
	print "! Deploying QkThings for %s" % (os_name())
	print platform.release(), platform.version()
	print "The whole process may take a while. Be patient."
	
	root_dir     = getcwd()
	build_dir    = path.expanduser("~/qkthings_local/build")
	release_dir  = path.expanduser("~/qkthings/dev/release")
	qkthings_dir = path.join(release_dir, "qkthings_" + time.strftime("%Y%m%d"))
	dist_dir     = path.join(release_dir, "dist")

	check_path(release_dir, True)
	check_path(dist_dir)
	check_path(qkthings_dir)

	print "! Deploying QkDaemon"
	deploy("software/qkdaemon", ["--clean"], args.verbose)

	print "! Deploying QkAPI"
	deploy("software/qkapi", ["--clean"], args.verbose)


	print "! Copying QkDaemon"
	copy_tree(build_dir + "/qt/qkdaemon/release", qkthings_dir + "/qkdaemon")

	print "! Copying QkAPI"
	copy_tree("software/qkapi/python", qkthings_dir + "/qkapi/python")

	print "! Copying Qt platforms"
	#copy_tree("dev/deploy/linux/qt/platforms", qkthings_dir + "/qkide/platforms")
	copy_tree("dev/deploy/linux/qt/platforms", qkthings_dir + "/qkdaemon/platforms")

	print "! Copying libraries"
	copy_tree(build_dir + "/qt/qkcore/release", qkthings_dir + "/shared/lib")
	copy_tree(build_dir + "/qt/qkwidget/release", qkthings_dir + "/shared/lib")
	copy_tree(build_dir + "/qt/qkapi/release", qkthings_dir + "/shared/lib")
	copy_tree("dev/deploy/linux/qt/lib", qkthings_dir + "/shared/lib")

	if args.dist:
		tar_name = "qkthings_bundle_" + os_name() + "_" + time.strftime("%Y%m%d") + ".tar.gz"
		print "! Creating distributable tarball", tar_name
		make_tarfile(qkthings_dir, dist_dir + "/" + tar_name)
		

if __name__ == "__main__":
	main();



