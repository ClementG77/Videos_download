import os
import sys
import subprocess
from moviepy.editor import VideoFileClip

def preview_video(input_file):
    command = f'ffplay {input_file} -fs -vf crop=ih*(9/16):ih -af "volume=0.05"'
    subprocess.call(command,shell=True)



if len(sys.argv) < 2:
    print("Usage: python resize.py [input_file] [output_file] ")
    sys.exit(1)


input_file = sys.argv[1]


preview_video(input_file)



