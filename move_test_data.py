#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import glob
import random
import shutil

TEST_RATE = 0.2  # this means how many percent of original files are taken for test data

def main(source : str, destination : str) -> None:
	source_files = glob.glob(source+"*")
	random.shuffle(source_files)
	for i in range(int(len(source_files)*TEST_RATE)):
		shutil.move(str(source_files[i]), destination)

if __name__ == "__main__":
	source = "./dataset/train/"
	destination = "./dataset/test/"
	main(source, destination)
