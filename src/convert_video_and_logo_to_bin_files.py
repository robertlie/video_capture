#!/usr/bin/env python3
# Author: Robert Lie (mobilefish.com)

import cv2
import os
import settings
import sys


def calculate_ratio(width, height):
    return width / height


def resize_height(img, screen_height):
    h, w = img.shape[:2]
    ratio = screen_height/h
    img = cv2.resize(img, (int(w*ratio), int(h*ratio)))

    return img


def resize_width(img, screen_width):
    h, w = img.shape[:2]
    ratio = screen_width / w
    img = cv2.resize(img, (int(w * ratio), int(h * ratio)))

    return img


def resize_image(img, screen_width, screen_height):

    h, w = img.shape[:2]

    ratio = calculate_ratio(w, h)
    screen_ratio = calculate_ratio(screen_width, screen_height)

    if ratio >= screen_ratio:
        # Resize height first, then width
        img = resize_height(img, screen_height)
        img = resize_width(img, screen_width)
    else:
        # Resize width first, then height
        img = resize_width(img, screen_width)
        img = resize_height(img, screen_height)

    return img


def add_border(img, screen_width, screen_height, border_color):
    h, w = img.shape[:2]

    if h < screen_height:
        delta_h = (screen_height - h) / 2
        img = cv2.copyMakeBorder(img, int(delta_h), int(delta_h), 0, 0, cv2.BORDER_CONSTANT, value=border_color)

    if w < screen_width:
        delta_w = (screen_width - w) / 2
        img = cv2.copyMakeBorder(img, 0, 0, int(delta_w), int(delta_w), cv2.BORDER_CONSTANT, value=border_color)

    return img


def get_video_frames(t_msec, counter):

    # CAP_PROP_POS_MSEC: Current position of the video file in milliseconds.
    # Set video start time position
    vidcap.set(cv2.CAP_PROP_POS_MSEC, t_msec)

    hasframes, img = vidcap.read()
    if hasframes:

        # Resize image
        img = resize_image(img, settings.screen_width, settings.screen_height)

        # Add border around image, if resized image is smaller than the screen size
        img = add_border(img, settings.screen_width, settings.screen_height, settings.border_color)

        # save frame as bmp file
        cv2.imwrite(os.path.join(settings.image_folder, 'image' + str(counter) + '.bmp'), img)
    return hasframes


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------
    # Check if settings values are valid
    # ----------------------------------------------------------------------------------------
    if not os.path.isdir(settings.image_folder):
        sys.exit('Folder ' + settings.image_folder + ' does not exists.')
    if not os.path.isdir(settings.bin_folder):
        sys.exit('Folder ' + settings.bin_folder + ' does not exists.')
    if not os.path.isdir(settings.video_folder):
        sys.exit('Folder ' + settings.video_folder + ' does not exists.')
    if not os.path.isdir(settings.logo_folder):
        sys.exit('Folder ' + settings.logo_folder + ' does not exists.')

    file = os.path.join(settings.video_folder, settings.video_filename)
    if not os.path.isfile(file):
        sys.exit('File ' + file + ' can not be found.')

    file = os.path.join(settings.logo_folder, settings.logo_filename)
    if not os.path.isfile(file):
        sys.exit('File ' + file + ' can not be found.')

    blue_value = settings.border_color[0]
    green_value = settings.border_color[1]
    red_value = settings.border_color[2]

    if not (isinstance(blue_value, int) and 0 <= blue_value <= 255):
        sys.exit('border_color[0] must be an integer. Allowed values: 0-255')
    if not (isinstance(green_value, int) and 0 <= green_value <= 255):
        sys.exit('border_color[1] must be an integer. Allowed values: 0-255')
    if not (isinstance(red_value, int) and 0 <= red_value <= 255):
        sys.exit('border_color[2] must be an integer. Allowed values: 0-255')

    if not (isinstance(settings.fps_new, int) and settings.fps_new >= 1):
        sys.exit('fps_new must be a integer. Allowed values: >= 1 and <= current fps')

    if not (isinstance(settings.start_time_sec, float) and settings.start_time_sec >= 0.0):
        sys.exit('start_time_sec must be a float. Allowed values: >=0.0')

    if not (isinstance(settings.stop_time_sec, float) and settings.stop_time_sec >= 0.0):
        sys.exit('stop_time_sec must be an float. Allowed values: >=0.0')

    if settings.stop_time_sec != 0.0 and settings.start_time_sec > settings.stop_time_sec:
        sys.exit('start_time_sec can not be larger than stop_time_sec')

    if not (isinstance(settings.screen_width, int) and settings.screen_width == 160):
        sys.exit('The screen_width must be an integer. Allowed value: 160')

    if not (isinstance(settings.screen_height, int) and settings.screen_height == 80):
        sys.exit('The screen_height must be an integer. Allowed value: 80')

    # ----------------------------------------------------------------------------------------
    # Remove all files from image_folder and bin_folder
    # ----------------------------------------------------------------------------------------
    # Remove all files from image_folder
    for filename in os.listdir(settings.image_folder):
        file_path = os.path.join(settings.image_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Remove all files from bin_folder
    for filename in os.listdir(settings.bin_folder):
        file_path = os.path.join(settings.bin_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # ----------------------------------------------------------------------------------------
    # Initialise
    # ----------------------------------------------------------------------------------------
    print('*** Initialise ***')

    # OpenCV VideoCapture removes alpha channel from video
    vidcap = cv2.VideoCapture(os.path.join(settings.video_folder, settings.video_filename))

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    framecount = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_end_time_sec = framecount / fps

    if settings.fps_new > fps:
        sys.exit('fps_new = ' + str(settings.fps_new) + ' is too large. It can not be larger than current fps = ' + str(int(fps)))

    print('fps=' + str(fps))
    print('fps_new=' + str(settings.fps_new))
    print('framecount=' + str(framecount))
    print('video_end_time_sec=' + str(video_end_time_sec))

    # If fps_new = 30, this means 30 frames per sec.
    # The time between each frame will be 1 / fps_new sec
    # Multiply by 1000 to convert the value into msec
    frame_duration_msec = 1 / settings.fps_new * 1000
    print('frame_duration_msec=' + str(frame_duration_msec))

    stop_time_sec_final = settings.stop_time_sec

    if settings.stop_time_sec == 0.0:
        stop_time_sec_final = video_end_time_sec
    elif settings.stop_time_sec != 0.0 and settings.stop_time_sec > video_end_time_sec:
        sys.exit('stop_time_sec can not be larger than video end time = ' + str(video_end_time_sec))

    stop_time_msec = int(stop_time_sec_final * 1000)
    time_msec = int(settings.start_time_sec * 1000)

    print('start_time_msec= ' + str(time_msec))
    print('stop_time_msec= ' + str(stop_time_msec))

    # ----------------------------------------------------------------------------------------
    # Create imageXXX.bmp files
    # ----------------------------------------------------------------------------------------
    print('*** Extracting images from video ***')
    print('Please be patient, make take several minutes to create imagexxx.bmp')

    count = 1
    success = get_video_frames(time_msec, count)
    print('Counter = ' + str(count) + ', at time = ' + str(time_msec) + ' msec')

    while success and vidcap.get(cv2.CAP_PROP_POS_MSEC) <= stop_time_msec:
        count = count + 1
        time_msec = int(vidcap.get(cv2.CAP_PROP_POS_MSEC) + frame_duration_msec)
        print('Counter = ' + str(count) + ', at time = ' + str(time_msec) + ' msec')
        success = get_video_frames(time_msec, count)

    total_images = count - 1

    print('Total bmp images generated: ' + str(total_images))

    # ----------------------------------------------------------------------------------------
    # Create bmp.bin file
    # ----------------------------------------------------------------------------------------
    print('*** Create bmp.bin ***')
    print('Please be patient, make take several minutes to store each imagexxx.bmp file into bmp.bin file.')

    # Remove bmp.bin
    if os.path.exists('bmp.bin'):
        os.remove('bmp.bin')

    count = 1
    while count <= total_images:
        file = os.path.join(settings.image_folder, 'image' + str(count) + '.bmp')
        os.system("python bmp2hex.py -kbin {0}".format(file))
        print('Store image' + str(count) + '.bmp in bmp.bin')
        count += 1

    # Move bmp.bin to bin_folder/bmp.bin
    file = os.path.join(settings.bin_folder, 'bmp.bin')
    os.rename("bmp.bin", file)

    # ----------------------------------------------------------------------------------------
    # Create logo_modified.bmp. Resize logo image if needed
    # ----------------------------------------------------------------------------------------
    print('*** Create logo_modified.bmp ***')

    # Resize image
    file = os.path.join(settings.logo_folder, settings.logo_filename)

    # Specify to load a color image. Any transparency of image will be neglected.
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    image = resize_image(image, settings.screen_width, settings.screen_height)

    # Add border around image, if resized image is smaller than the screen size
    image = add_border(image, settings.screen_width, settings.screen_height, settings.border_color)

    # save logo image as bmp file
    cv2.imwrite(os.path.join(settings.image_folder, 'logo_modified.bmp'), image)

    # ----------------------------------------------------------------------------------------
    # Create logo.bin file
    # ----------------------------------------------------------------------------------------
    print('*** Create logo.bin ***')
    file = os.path.join(settings.image_folder, 'logo_modified.bmp')
    os.system("python bmp2hex.py -kbin {0}".format(file))
    print('Store logo_modified.bmp in logo.bin')

    # Move bmp.bin to bin_folder/logo.bin
    file = os.path.join(settings.bin_folder, 'logo.bin')
    os.rename("bmp.bin", file)
