#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import glob
import os
import random

class ImageReader:
	def get_image(self, path:str):
		return cv2.imread(path)

class ImageProcesser:
	#CASCADE_FILE = "./utils/opencv-4.0.1/opencv-4.0.1/data/haarcascade/haarcascade_frontalface_alt.xml"
	CASCADE_FILE = "./utils/haarcascade_frontalface_alt.xml"
	SCALE_FACTOR = 1.1
	NEIGHBORS = 2
	SIZE = 64
	
	def __init__(self, image):
		self.image = image
		
		# recognize faces in the image
		face_list = self.recognize_faces()
		
		# if a face or more are detected
		self.processed = self.extract_face(face_list)
	
	def recognize_faces(self):
		# change image's color to gray scale
		image_gs = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		cascade = cv2.CascadeClassifier(self.CASCADE_FILE)
		
		# recognize faces in the image taken below
		return cascade.detectMultiScale(image_gs, 
		                                scaleFactor=self.SCALE_FACTOR,
										minNeighbors=self.NEIGHBORS, 
										minSize=(self.SIZE, self.SIZE))
	
	def extract_face(self, face_list):
		# if no face is detected
		#print(face_list)
		if len(face_list) <= 0:
			print("no face")
			return None
		
		# extracts rectangles
		for rect in face_list:
			#print(rect)
			flag = self.resize(rect)
		if not flag:
			print("failed to detect a face")
			return None
		print("resized image size: " + str(self.image.shape[:2]))
		return self.image
	
	def resize(self, rect) -> bool:
		x, y, width, height = rect
		self.image = self.image[y:y+height, x:x+width]
		if self.image.shape[0] < self.SIZE:
			print("this image is too small")
			return False
		self.image = cv2.resize(self.image, (self.SIZE, self.SIZE))
		#self.image = cv2.resize(self.image, (64, 64))
		return True
	
	def get_processed(self):
		return self.processed

class ImageWriter:
	def write_data(self, data, dir:str, name:str):
		path = os.path.join(dir, name)
		cv2.imwrite(path, data)

class RecognitionManager:
	MATCH_PATTERN = "*"
	
	def __init__(self, source:str, destination:str):
		# get paths of all files in the given directory
		paths = glob.glob(os.path.join(source, self.MATCH_PATTERN))
		
		# process each image
		for p in paths:
			print("processing :" + p)
			self.process_image(p, destination)
	
	def process_image(self, path:str, destination:str) -> bool:
		# open the file
		raw = ImageReader().get_image(path)
		#raw = cv2.imread(str(path))
		if raw is None:
			print("can't read: " + path)
			return False 
		
		# process the file
		processed = ImageProcesser(raw).get_processed()
		if processed is None:
			print("can't process: " + path)
			return False 
		
		# save the file
		ImageWriter().write_data(processed, destination, 
								 self.get_name(path))
		return True
	
	def get_name(self, path:str) -> str:
		return os.path.basename(path)

def main():
	source = "./images"
	#source = "./working/origin_image"
	destination = "./dataset/train"
	RecognitionManager(source, destination)

if __name__ == "__main__":
	main()