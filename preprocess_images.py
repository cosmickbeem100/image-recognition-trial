#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob

def scratch_image(img, flip=True, thr=True, filt=True):
	# set generation methods in an array
	methods = [flip, thr, filt]
	
	# make filters to modify images
	filter1 = np.ones((3, 3))
	
	# save the original image data in an array
	images = [img]
	
	# functions to apply the modification
	scratch = np.array([
	lambda x: cv2.flip(x, 1),
	lambda x: cv2.threshold(x, 100, 255, cv2.THRESH_TOZERO)[1],
	lambda x: cv2.GaussianBlur(x, (5, 5), 0)])
	
	# generate new image that is merged the original image and the modified image
	doubling_images = lambda f, imag: np.r_[imag, [f(i) for i in imag]]
	for func in scratch[methods]:
		images = doubling_images(func, images)
	return images

# read images in ./face_image directory
in_dir = "./face_image/*"
in_jpg = glob.glob(in_dir)
img_file_name_list = os.listdir("./face_image/")

for i in range(len(in_jpg)):
	print(str(in_jpg[i]))
	img = cv2.imread(str(in_jpg[i]))
	scratch_face_images = scratch_image(img)
	
	for num, im in enumerate(scratch_face_images):
		fn, ext = os.path.splitext(img_file_name_list[i])
		file_name = os.path.join("./face_scratch_image",
								 str(fn+"."+str(num)+".jpg"))
		cv2.imwrite(str(file_name), im)
