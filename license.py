import fnmatch
import os
import string

class LicenseGenerator():

	def __init__(self):
		self.license = "QkThings LICENSE\nCopyright (C) <http://qkthings.com>\n\n"
		self.files_to_match_c = ["*.c", "*.cpp","*.h"]
		self.files_to_match_make = ["Makefile", "*.mk"]
		self._matches_c = []
		self._matches_make = []
		self._create_license()

	def read(self, filename):
		with file(filename, 'r') as license_file:
			self.license = license_file.read()
		print self.license
		self._create_license()

	def _create_license(self):
		license_lines = self.license.splitlines(True)
		license_lines.pop() # removes the last (empty) line
		self.license_c = "/*\n"
		self.license_make = "#\n"
		for line in license_lines:
			if line != " ":
				self.license_c += " * " + line
				self.license_make += "# " + line
		self.license_c += " */\n"
		self.license_make += "#\n"				

	def _find_matches(self, path):
		matches_c = []
		matches_make = []
		for root, dirnames, filenames in os.walk(path):

			for file_to_match_c in self.files_to_match_c:
				for filename in fnmatch.filter(filenames, file_to_match_c):
					matches_c.append(os.path.join(root, filename))

			for file_to_match_make in self.files_to_match_make:
				for filename in fnmatch.filter(filenames, file_to_match_make):
					matches_make.append(os.path.join(root, filename))

		self._matches_c = matches_c
		self._matches_make = matches_make
		
		
	def create(self, path):
		self._find_matches(path)

		for filename in self._matches_c:
			print "Create license on: ", filename
			with open(filename, 'r') as original: data = original.read()
			with open(filename, 'w') as modified: modified.write(self.license_c + data)

		for filename in self._matches_make:
			print "Create license on: ", filename
			with open(filename, 'r') as original: data = original.read()
			with open(filename, 'w') as modified: modified.write(self.license_make + data)

	def remove(self, path):
		self._find_matches(path)
		#FIXME self.license may not be the same available on the file so line count will be different!
		license_line_count = self.license.count("\n") + 2;

		for filename in self._matches_c:
			with open(filename, 'r') as original: data = original.read().splitlines(True)
			for line in data[:license_line_count]:
				if "QkThings LICENSE" in line:
					print "Remove license from: ", filename
					with open(filename, 'w') as modified: modified.writelines(data[license_line_count:])

		for filename in self._matches_make:
			with open(filename, 'r') as original: data = original.read().splitlines(True)
			for line in data[:license_line_count]:
				if "QkThings LICENSE" in line:
					print "Remove license from: ", filename
					with open(filename, 'w') as modified: modified.writelines(data[license_line_count:])
		

if __name__ == "__main__":
	license_gen = LicenseGenerator()
	license_gen.read("LICENSE");
	folders = []
	folders.append("embedded/target");
	folders.append("embedded/qkprogram/include");
	folders.append("embedded/qkprogram/lib");
	folders.append("embedded/qkperipheral/include");
	folders.append("embedded/qkperipheral/lib");
	folders.append("embedded/qkdsp/include");
	folders.append("embedded/qkdsp/lib");
	folders.append("software/qkide/gui");
	folders.append("software/qkide/core");
	folders.append("software/qkdaemon/gui");
	folders.append("software/qkdaemon/core");
	folders.append("software/qkwidget");
	folders.append("software/qkcore");
	folders.append("software/qkloader");
	folders.append("software/qkapi");
	for folder in folders:
		license_gen.remove(folder)
		license_gen.create(folder)

