import os
import sys
import subprocess
from moviepy.editor import VideoFileClip

def rotate_video(input_file,output_folder):
    
    command = f'ffmpeg -i {input_file} -vf "transpose=1" {output_folder}'
    subprocess.call(command,shell=True)
    # 0 = 90° counterclockwise and vertical flip (default)
    # 1 = 90° clockwise
    # 2 = 90° counterclockwise
    # 3 = 90° clockwise and vertical flip


if len(sys.argv) < 2:
    print("Usage: python rotatePreview.py [input_file] [output_file] ")
    sys.exit(1)


input_file = sys.argv[1]
output_file = sys.argv[2]


rotate_video(input_file, output_file)
