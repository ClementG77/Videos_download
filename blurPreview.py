import os
import sys
import subprocess
from moviepy.editor import VideoFileClip

def preview_video(input_file):
    print(input_file)
    command = f'ffplay -i {input_file} -i {input_file} -filter_complex ""[0:v]scale=2276:1280,boxblur=4[bg];[1:v]scale=720:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[tmp];[tmp]crop=720:1280:(2276-720)/2:0[out]"" -map [out] -map 0:a '
    subprocess.call(command,shell=True)



if len(sys.argv) < 2:
    print("Usage: python resize.py [input_file] [output_file] ")
    sys.exit(1)


input_file = sys.argv[1]


preview_video(input_file)
