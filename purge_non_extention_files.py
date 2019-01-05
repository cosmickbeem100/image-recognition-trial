#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import glob
import os
import re

MATCHING_PATTERN = "\.jpg$"

def main(dir:str) -> None:
	files = [p for p in glob.glob(dir+"*") 
	         if not re.search(MATCHING_PATTERN, p)]
	print("[ delete < " + str(len(files)) + " > files ]")
	for i in files:
		print("  delete " + i)
		os.remove(i)
	
if __name__ == "__main__":
	dir = "./images/"
	main(dir)
