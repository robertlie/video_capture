#!/usr/bin/env python3
# Copyright (c) 2021 Mobilefish.com

import cv2
import settings
import os

# ----------------------------------------------------------------------------------------
# Extracted image from video information
# ----------------------------------------------------------------------------------------
# Bit depth specifies how much color information is available for each pixel in an image.
# RGB mode images are made of three color channels.
# An 8‑bit per pixel RGB image has 256 possible values for each channel which means it has over 16 million
# possible color values.
# 256 x 256 x 256 = 16.777.216
# If the depth is 4 it means Alpha channel. But OpenCV VideoCapture removes alpha channel from video.

img_video_file = os.path.join(settings.image_folder, 'image1.bmp')
img = cv2.imread(img_video_file)
height, width, depth = img.shape

print('*** Extracted image information from video ***')
print('File: ', img_video_file)
print('Width: ', width)
print('Height:', height)
print('Depth (number of bytes):', depth)

# ----------------------------------------------------------------------------------------
# Logo image information
# ----------------------------------------------------------------------------------------

img_logo_file = os.path.join(settings.image_folder, 'logo_modified.bmp')

img = cv2.imread(img_logo_file)
height, width, depth = img.shape

print('*** Logo image information ***')
print('File: ', img_logo_file)
print('Width: ', width)
print('Height:', height)
print('Depth (number of bytes):', depth)
