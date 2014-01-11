#!/usr/bin/python

import os, platform, shutil, datetime, tarfile, distutils.core
import subprocess
import os, tarfile, datetime

DEPLOY_DIR="~"
QT_VER_STR="5.1"

def make_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
		
def main():
	output_dir = os.path.basename("qkthings_backup")
	date_and_ext = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".tar.gz"
	folders = ["qkthings", "qkthings_linux"]

	print "Creating qkthings backup on folder: " + output_dir
	for folder in folders:
		print folder, "..."
		make_tarfile(folder, os.path.join(output_dir, folder + "_" + date_and_ext))
	print "Done"
	
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
		
	print "Deploying qkide..."
	distutils.dir_util.copy_tree("software/shared/qt/" + QT_VER_STR + "/" + os_str, qkide_dir)
	distutils.dir_util.copy_tree("software/qkide/release", qkthings_dir + "/qkide")
	
	print "Deploying toolchain..."
	distutils.dir_util.copy_tree("embedded/shared/toolchain/common", qkide_dir + "/resources/embedded/toolchain/common")
	distutils.dir_util.copy_tree("embedded/shared/toolchain/" + os_str, qkide_dir + "/resources/embedded/toolchain/" + os_str)

	
if __name__ == "__main__":
	main();



