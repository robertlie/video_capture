#!/usr/bin/env python3
# Copyright (c) 2021 Mobilefish.com

# Enter your video filename in folder input_video
video_filename = 'toy_1280x740_48mb.mov'

# Enter your logo bitmap filename in folder input_logo
logo_filename = 'logo.bmp'

# fps_new is a int. Allowed values: >= 1 and <= current fps
fps_new = 29

image_folder = 'output_images'
bin_folder = 'output_bin'
video_folder = 'input_video'
logo_folder = 'input_logo'


# Color values are integers. Allowed values: 0 - 255
# black = [0, 0, 0]
# white = [255, 255, 255]
# blue = [255, 0, 0]
# green = [0, 255, 0]
# red = [0, 0, 255]
border_color = [0, 0, 0]

# start_time_sec is a float. Allowed values: >= 0.0
start_time_sec = 0.0

# stop_time_sec is a float. Allowed values: >= 0.0
# If stop_time_sec = 0.0, the video end time is used.
stop_time_sec = 0.0

# Do not change these values! Both values are integers.
screen_width = 160
screen_height = 80
