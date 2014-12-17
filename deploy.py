#!/usr/bin/python

from os import getcwd, chdir, path
import os, platform, shutil, datetime, tarfile, distutils.core
from distutils.dir_util import copy_tree, remove_tree, mkpath
import subprocess
from subprocess import call
import argparse
import os, tarfile, datetime
import time

from qkthings.utils import cmd, os_name, make_tarfile
	
def deploy():
	if os_name() == "":
		return

	parser = argparse.ArgumentParser()
	parser.add_argument("--dist", action="store_true", help='create distributable tarball')
	args = parser.parse_args()
	
	print "! Deploying QkThings for %s %s %s" % (os_name(), platform.release(), platform.version())
	print "The whole process may take a while. Be patient."
	
	root_dir     = getcwd()
	release_dir  = path.expanduser("~/qkthings/dev/release")
	qkthings_dir = path.join(release_dir, "qkthings_" + time.strftime("%Y%m%d"))
	dist_dir     = path.join(release_dir, "dist")
	
	qkthings_local_build = path.expanduser("~/qkthings_local/build")

	if not path.exists(qkthings_dir):
		mkpath(qkthings_dir)
	else:
		print "! Cleaning", qkthings_dir
		remove_tree(qkthings_dir)

	if not path.exists(dist_dir):
		mkpath(dist_dir)
	
	'''
	print "! Deploying QkIDE..."
	chdir("software/qkide")
	call(["python", "deploy.py", "--clean", "--emb", "--toolchain"])
	chdir(root_dir)
	'''

	print "! Deploying QkDaemon..."
	chdir("software/qkdaemon")
	cmd(["python", "deploy.py", "--clean"])
	chdir(root_dir)

	print "! Deploying QkAPI..."
	chdir("software/qkdaemon")
	cmd(["python", "deploy.py", "--clean"])
	chdir(root_dir)


	#print "! Copying QkIDE..."
	#copy_tree("software/qkide/release", qkthings_dir + "/qkide")

	print "! Copying QkDaemon..."
	copy_tree(qkthings_local_build + "/qt/qkdaemon/release", qkthings_dir + "/qkdaemon")

	print "! Copying QkAPI..."
	copy_tree("software/qkapi/python", qkthings_dir + "/qkapi/python")

	print "! Copying Qt platforms..."
	#copy_tree("dev/deploy/linux/qt/platforms", qkthings_dir + "/qkide/platforms")
	copy_tree("dev/deploy/linux/qt/platforms", qkthings_dir + "/qkdaemon/platforms")

	print "! Copying libraries..."
	copy_tree(qkthings_local_build + "/qt/qkcore/release", qkthings_dir + "/shared/lib")
	copy_tree(qkthings_local_build + "/qt/qkwidget/release", qkthings_dir + "/shared/lib")
	copy_tree(qkthings_local_build + "/qt/qkapi/release", qkthings_dir + "/shared/lib")
	copy_tree("dev/deploy/linux/qt/lib", qkthings_dir + "/shared/lib")

	if args.dist:
		tar_name = "qkthings_bundle_" + os_name() + "_" + time.strftime("%Y%m%d") + ".tar.gz"
		print "! Creating distributable tarball", tar_name
		make_tarfile(qkthings_dir, dist_dir + "/" + tar_name)
		

if __name__ == "__main__":
	deploy();



