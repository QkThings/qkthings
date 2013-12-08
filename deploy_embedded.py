#!/usr/bin/python

import os, platform, shutil
import subprocess

OUTPUT_DIR = "output"
# DEPLOY
# make clean
# make TARGET=<target>
# cp lib/<project>.a output/lib/<target>

# TEST
# make clean
# make test MAIN=<test> TARGET=<target>
# cp bin/<project>.bin output/test/<target>
# mv 

def generateLib(project, target):
	print " --- generate %s.a for %s" % (project,target)
	build_dir = os.path.join("embedded",project,"build")
	lib_dir = os.path.join(build_dir,"lib");
	subprocess.call(["make","clean"], cwd=build_dir)	
	subprocess.call(["make","TARGET=%s" % (target)], cwd=build_dir)
	lib =  "%s.a" % (project)
	src = os.path.join(lib_dir, lib)
	dest = os.path.join(OUTPUT_DIR, "embedded", "lib", target)
	os.makedirs(dest)
	shutil.copy(src,dest)
	print " --- %s copied to %s" % (src,dest)

def generateTest(main, target):
	print " --- generate test with %s.a for %s" % (main,target)
	build_dir = os.path.join("embedded",project,"build")
	lib_dir = os.path.join(build_dir,"lib");
	subprocess.call(["make","clean"], cwd=build_dir)	
	subprocess.call(["make","test","MAIN=%s" % (main),"TARGET=%s" % (target)], cwd=build_dir)

if __name__ == "__main__":
	targets = ["arduino"]
	projects = ["qkprogram"]

	if os.path.isdir(OUTPUT_DIR):
		shutil.rmtree(OUTPUT_DIR)

	for target in targets:
		for project in projects:
			generateLib(project,target)



