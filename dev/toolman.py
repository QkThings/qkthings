#!/usr/bin/python

from os import path
import os, platform, shutil, datetime, tarfile, distutils.core
from distutils.dir_util import copy_tree, remove_tree, mkpath
import argparse
import os, tarfile, datetime
import urllib

targets_available = ["efm32", "arduino"]
get_cb = {}

TOOLCHAIN_FORGE = "http://qkthings.com/files/shared/toolchain/"

def check_path(dir, args):
	if path.exists(dir) and args.clean:
		print "! Cleaning", dir
		remove_tree(dir)
	if not path.exists(dir):
		mkpath(dir)
		return False
	else:
		return True

def download(url, dest):
	print "! Downloading %s to %s" % (url,dest)
	if urllib.urlopen(url).getcode() == 200:	
		urllib.urlretrieve(url, dest)
		return True
	else:
		print "! URL not found:", url
		return False

def extract(file, dest):
	print "! Extracting %s to %s" % (file, dest)
	tar = tarfile.open(file)
	tar.extractall(path=dest)
	tar.close()

def create_name(list, separator="_", suffix="", prefix=""):
	return (separator.join(["%s"] * len(list))+suffix) % tuple(list)

def create_path(list):
	return path.join(create_name(list, separator="/", suffix="/"))
	
def get_toolchain(tree, args):
	archive = create_name(tree, suffix=".tar.bz2")
	tree.insert(0, args.root)
	dir = path.join(create_path(tree))
	archive_dir = path.join(dir, archive)
	
	if not check_path(dir, args):
		if download(TOOLCHAIN_FORGE + archive, archive_dir):
			extract(archive_dir, dir)
			if not args.keep_archive:
				os.remove(archive_dir)
	else:
		print "! %s already exists" % dir

def get_efm32(args):
	get_toolchain(["cpu", "arm", args.dist], args)
	get_toolchain(["platform", "efm32", "common"], args)
	
def get_arduino(args):
	get_toolchain(["cpu", "avr", args.dist], args)
	get_toolchain(["platform", "arduino", "common"], args)
	
def run(args):
	get_cb[args.target](args)

def toolman():
	get_cb["efm32"] = get_efm32
	get_cb["arduino"] = get_arduino
		
	parser = argparse.ArgumentParser()
	parser.add_argument("-t","--target", required=True, help='')
	parser.add_argument("-r","--root", required=True, help='toolchain root folder')
	parser.add_argument("--clean", action="store_true", default=False, help='clean')
	parser.add_argument("--dist", required=True, help='win or linux')
	parser.add_argument("--keep-archive", action="store_true", default=False, help='keep downloaded archives')
	parser.add_argument("--available", action="store_true", help='lists available targets')
	args = parser.parse_args()
	
	if args.available:
		print "ERROR: targets available:\n", targets_available
		return
		
	if args.target not in targets_available:
		print "ERROR: target not supported"
		return
		
	if args.dist not in ["win", "linux"]:
		print "ERROR: dist must be \"win\" or \"linux\""
		return

	run(args)

if __name__ == "__main__":
	toolman();
