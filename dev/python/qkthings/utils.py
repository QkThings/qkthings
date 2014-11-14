#!/usr/bin/python

from os import getcwd, chdir, path
from distutils.dir_util import copy_tree, remove_tree, mkpath
from subprocess import call
import tarfile, datetime, urllib

devnull = open('/dev/null', 'w')

def cp(root_src,root_dest,rel_path):
	print "Copying %s from %s to %s" % (rel_path, root_src, root_dest)
	if not path.isdir(path.join(root_src, rel_path)):
		print "Warning: %s doesn't exist!" % path.join(root_src, rel_path)
	else:
		copy_tree(path.join(root_src, rel_path), path.join(root_dest, rel_path))	

def check_path(dir, clean = False):
	if path.exists(dir) and clean:
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

def cmd(line,verbose):
	if verbose:
		ret = call(line)
	else:
		ret = call(line, stdout=devnull, stderr=devnull)
	#print "return",ret