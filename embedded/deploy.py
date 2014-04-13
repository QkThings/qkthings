#!/usr/bin/python

from os import getcwd, chdir, path, environ
from subprocess import call

def unset_all():
	environ["TARGET"] = ""
	environ["LIB"] = ""
	environ["TEST"] = ""
	environ["APP"] = ""

def deploy():
	print " ### Deploy embedded"
	rootdir = getcwd()

	targets = []
	targets.append("arduino.uno")
	targets.append("efm32.g_olimex")

	libs = []
	libs.append("qkprogram")

	for target in targets:
		for lib in libs:
			chdir(path.join(rootdir,lib))
			call(["python", "deploy.py"])		
			chdir(rootdir)
			unset_all()
			print " === Build LIB=%s for TARGET=%s" % (lib, target)
			call(["make","clean","LIB=%s" % lib,"TARGET=%s" % target])
			call(["make","lib","LIB=%s" % lib,"TARGET=%s" % target])


if __name__ == "__main__":
	deploy();
