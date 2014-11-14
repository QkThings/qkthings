#!/usr/bin/python

import argparse
from os import path
from utils import check_path, download, extract

TOOLCHAIN_FORGE = "http://qkthings.com/files/shared/toolchain/"

class Target:
	def __init__(self, cpu, platform):
		self.cpu = cpu
		self.platform = platform

targets = {
	"arduino" : Target("avr","arduino") ,
	"efm32"   : Target("arm","efm32")
}

def _create_name(list, separator="_", suffix="", prefix=""):
	return (separator.join(["%s"] * len(list))+suffix) % tuple(list)

def _create_path(list):
	return path.join(_create_name(list, separator="/", suffix="/"))
	
def _get_toolchain(tree, root, keep_archive=False, clean=False):
	archive = _create_name(tree, suffix=".tar.bz2")
	tree.insert(0, root)
	dir = path.join(_create_path(tree))
	archive_dir = path.join(dir, archive)
	
	if not check_path(dir, clean):
		if download(TOOLCHAIN_FORGE + archive, archive_dir):
			extract(archive_dir, dir)
			if not keep_archive:
				os.remove(archive_dir)
	else:
		print "! %s already exists" % dir
	
def run(target, dist, root, keep_archive=False, clean=False):
	_get_toolchain(["cpu",      targets[target].cpu, dist],          root, keep_archive, clean)
	_get_toolchain(["platform", targets[target].platform, "common"], root, keep_archive, clean)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-t","--target", required=True, help='')
	parser.add_argument("-r","--root", required=True, help='toolchain root folder')
	parser.add_argument("--clean", action="store_true", default=False, help='clean')
	parser.add_argument("-d","--dist", required=True, help='win or linux')
	parser.add_argument("--keep-archive", action="store_true", default=False, help='keep downloaded archives')
	parser.add_argument("--available", action="store_true", help='lists available targets')
	args = parser.parse_args()
	
	if args.available:
		print "Targets available:\n", targets.keys()
		return
		
	if args.target not in targets.keys():
		print "ERROR: target not supported"
		return
		
	if args.dist not in ["win", "linux"]:
		print "ERROR: dist must be \"win\" or \"linux\""
		return

	run(args.target, args.dist, args.root, args.keep_archive, args.clean)
