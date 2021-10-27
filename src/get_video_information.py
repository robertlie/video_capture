#!/usr/bin/env python3
# Author: Robert Lie (mobilefish.com)

import settings
import cv2
import os


vidcap = cv2.VideoCapture(os.path.join(settings.video_folder, settings.video_filename))
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
framecount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
video_width, video_height = (int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
video_duration = framecount / fps

print('FPS = ', fps)
print('The number of frames = ', framecount)
print('Video width x height = ', str(video_width) + ' x ' + str(video_height))
print('Video duration (sec) = ', str(round(video_duration, 3)))
