#!/usr/bin/python

import os, platform, shutil
from optparse import OptionParser

class Settings:
	def __init__(self):
		self.deploy_path = os.path.join(os.path.expanduser("~"),"QkThings")

	def read(self, path):
		if not os.path.exists(path):
			print "Unable to open settings file: %s" % path
			return False
		else:
			f = open(path,"r")
			content = f.readlines()
			for line in content:
				key = line.split("=")[0]
				value = line.split("=")[1].rstrip("\n")
				if key == "DEPLOY_PATH":
					print key, value
					self.deploy_path = os.path.expanduser(value);
			f.close()
			return True

	def validate(self):
#		if not os.path.exists(self.deploy_path):
#			return False
		return True

	def show(self):
		print "DEPLOY_PATH  = %s" % self.deploy_path
		print "EMB_INC_PATH = %s" % self.emb_inc_path
		print "EMB_LIB_PATH = %s" % self.emb_lib_path

	def apply(self):
		if not os.path.exists(self.deploy_path):
			os.makedirs(self.deploy_path)
		self.emb_inc_path = os.path.join(self.deploy_path,"embedded","include")
		self.emb_lib_path = os.path.join(self.deploy_path,"embedded","lib")

def createFolder(path):
	if not os.path.exists(path):
		os.makedirs(path)

def createFolders(settings):
	print "Creating folders..."
	root = settings.deploy_path
	if os.path.isdir(root):
		shutil.rmtree(root)
	createFolder(settings.deploy_path)
	createFolder(settings.emb_inc_path)
	createFolder(settings.emb_lib_path)

def copyFile(src,dest):
	fr = open(src, "r");
	fw = open(dest, "w");
	fw.write(fr.read())
	fr.close()
	fw.close()

def deployEmbedded(settings):
	print "Deploying embedded components..."

	for root, dirs, files in os.walk("embedded"):
		if "include" in root:
			for inc_file in files:
				src = os.path.join(root, inc_file)
				dest = os.path.join(settings.emb_inc_path, inc_file)
				copyFile(src, dest)
		if "lib" in root:
			for lib_file in files:
				src = os.path.join(root, lib_file)
				dest = os.path.join(settings.emb_lib_path, lib_file)
				copyFile(src, dest)

def deploySoftware():
	print "Deploying software apps..."

def main():
	print "---------------------------------------------------------------------"
	print "QkThings (qk-things.com)"
	print "Deploying on", platform.system(), platform.release()
	print "---------------------------------------------------------------------"

	settings = Settings()
	parser = OptionParser()
	parser.add_option("-q", "--quiet",
		              action="store_false", dest="verbose", default=True,
		              help="don't print status messages to stdout")
	(options, args) = parser.parse_args()

			
	if settings.validate() is False:
		print "Invalid settings"
		exit(1)
		
	settings.apply()
	settings.show()

	print "---------------------------------------------------------------------"
	createFolders(settings)
	deployEmbedded(settings)
	deploySoftware()
	print "---------------------------------------------------------------------"
	print "Done"

if __name__ == "__main__":
	main()

