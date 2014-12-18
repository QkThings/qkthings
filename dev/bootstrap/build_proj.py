
from os import getcwd, chdir, path, environ
import argparse

from qkthings.utils import cmd, check_path, qt_build

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--clean", action="store_true", help='clean')
	parser.add_argument("--verbose", action="store_true", default=False, help='verbose')
	args = parser.parse_args()

	qkthings_dir = environ["QKTHINGS_DIR"]
	qkthings_local = environ["QKTHINGS_LOCAL"]

	build_dir = path.join(qkthings_local, "build/qt")
	sw_dir = path.join(qkthings_dir, "software")

	qt_build(sw_dir + "/qkloader/efm32_loader", build_dir + "/efm32_loader", args.clean, args.verbose)

if __name__ == "__main__":
	main()