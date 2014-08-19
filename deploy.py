#!/usr/bin/python

from os import getcwd, chdir, path
import os, platform, shutil, datetime, tarfile, distutils.core
import subprocess
from subprocess import call
import os, tarfile, datetime

DEPLOY_DIR="./deploy"
	
def main():
	os_name = platform.system();
	os_str = ""
	if os_name == "Windows":
		os_str = "win"
	elif os_name == "Linux":
		os_str = "linux"
	else:
		print "OS not supported"
		return
	
	print "DEPLOY qkthings for %s %s %s" % (os_name, platform.release(), platform.version())
	print "The whole process may take a while. Be patient."
	
	deploy_dir = os.path.expanduser(DEPLOY_DIR)
	qkthings_dir = os.path.join(deploy_dir, "qkthings")
	qkide_dir = os.path.join(qkthings_dir, "qkide")
	
	if os.path.exists(qkthings_dir):
		print "Cleaning..."
		distutils.dir_util.remove_tree(qkthings_dir)


	rootdir = getcwd()
	EMBEDDED_DIR  = path.join(rootdir, "embedded")
	SOFTWARE_DIR = path.join(rootdir, "software")
	QKIDE_DIR = path.join(SOFTWARE_DIR, "qkide");

	print "Deploying qkide"
	chdir(QKIDE_DIR)
	call(["python", "deploy.py"])
	chdir(rootdir)
	distutils.dir_util.copy_tree("software/qkide/release", qkthings_dir + "/qkide")
	distutils.dir_util.copy_tree("software/qkdaemon/release", qkthings_dir + "/qkdaemon")
	distutils.dir_util.copy_tree("software/qkapi/python", qkthings_dir + "/qkapi/python")

	distutils.dir_util.copy_tree("deploy/linux/qt/platforms", qkthings_dir + "/qkide/platforms")
	distutils.dir_util.copy_tree("deploy/linux/qt/platforms", qkthings_dir + "/qkdaemon/platforms")
	

	print "Deploying libraries..."
	distutils.dir_util.copy_tree("software/qkcore/release", qkthings_dir + "/shared/lib")
	distutils.dir_util.copy_tree("software/qkwidget/release", qkthings_dir + "/shared/lib")
	distutils.dir_util.copy_tree("software/qkapi/qt/release", qkthings_dir + "/shared/lib")

	distutils.dir_util.copy_tree("deploy/linux/qt/lib", qkthings_dir + "/shared/lib")


	return
#	distutils.dir_util.copy_tree("software/shared/qt/" + QT_VER_STR + "/" + os_str, qkide_dir)
	distutils.dir_util.copy_tree("software/qkcore/release", qkthings_dir + "/shared")
#	distutils.dir_util.copy_tree("software/qkapi/release", qkthings_dir + "/shared")
	distutils.dir_util.copy_tree("software/qkwidget/release", qkthings_dir + "/shared")
	
	print "Deploying toolchain..."
	distutils.dir_util.copy_tree("embedded/shared/toolchain/common", qkide_dir + "/resources/embedded/toolchain/common")
	distutils.dir_util.copy_tree("embedded/shared/toolchain/" + os_str, qkide_dir + "/resources/embedded/toolchain/" + os_str)

	
if __name__ == "__main__":
	main();



