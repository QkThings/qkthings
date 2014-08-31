#!/usr/bin/python

from os import getcwd, chdir, path
import os, platform, shutil, datetime, tarfile, distutils.core
from distutils.dir_util import copy_tree, remove_tree, mkpath
import subprocess
from subprocess import call
import argparse
import os, tarfile, datetime
import time

DEPLOY_DIR="./deploy"

def make_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
	
def deploy():
	os_name = platform.system();
	os_str = ""
	if os_name == "Windows":
		os_str = "win"
	elif os_name == "Linux":
		os_str = "linux"
	else:
		print "OS not supported"
		return

	parser = argparse.ArgumentParser()
	parser.add_argument("--dist", action="store_true", help='create distributable tarball')
	args = parser.parse_args()
	
	print "! Deploying QkThings for %s %s %s" % (os_name, platform.release(), platform.version())
	print "The whole process may take a while. Be patient."
	
	root_dir     =  getcwd()
	deploy_dir   =  path.expanduser(DEPLOY_DIR)
	qkthings_dir =  path.join(deploy_dir, "qkthings")
	dist_dir     =  path.join(deploy_dir, "dist")
	

	if not path.exists(qkthings_dir):
		mkpath(qkthings_dir)
	else:
		print "! Cleaning", qkthings_dir
		remove_tree(qkthings_dir)

	if not path.exists(dist_dir):
		mkpath(dist_dir)
	

	print "! Deploying QkIDE..."
	chdir("software/qkide")
	call(["python", "deploy.py", "--clean", "--emb", "--toolchain"])
	chdir(root_dir)

	print "! Deploying QkDaemon..."
	chdir("software/qkdaemon")
	call(["python", "deploy.py", "--clean"])
	chdir(root_dir)

	print "! Deploying QkAPI..."
	chdir("software/qkdaemon")
	call(["python", "deploy.py", "--clean"])
	chdir(root_dir)


	print "! Copying QkIDE..."
	copy_tree("software/qkide/release", qkthings_dir + "/qkide")

	print "! Copying QkDaemon..."
	copy_tree("software/qkdaemon/release", qkthings_dir + "/qkdaemon")

	print "! Copying QkAPI..."
	copy_tree("software/qkapi/python", qkthings_dir + "/qkapi/python")

	print "! Copying Qt platforms..."
	copy_tree("deploy/linux/qt/platforms", qkthings_dir + "/qkide/platforms")
	copy_tree("deploy/linux/qt/platforms", qkthings_dir + "/qkdaemon/platforms")

	print "! Copying libraries..."
	copy_tree("software/qkcore/release", qkthings_dir + "/shared/lib")
	copy_tree("software/qkwidget/release", qkthings_dir + "/shared/lib")
	copy_tree("software/qkapi/qt/release", qkthings_dir + "/shared/lib")
	copy_tree("deploy/linux/qt/lib", qkthings_dir + "/shared/lib")

#	print "! Deploying toolchain..."
#	copy_tree("embedded/shared/toolchain/common", "software/qkide/resources/embedded/toolchain/common")
#	copy_tree("embedded/shared/toolchain/" + os_str, "software/qkide/resources/embedded/toolchain/" + os_str)

	if args.dist:
		tar_name = "qkthings_bundle_" + os_str + "_" + time.strftime("%Y%m%d") + ".tar.gz"
		print "! Creating distributable tarball", tar_name
		make_tarfile(qkthings_dir, dist_dir + "/" + tar_name)
		

	
if __name__ == "__main__":
	deploy();



