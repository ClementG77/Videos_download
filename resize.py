import os
import sys
import subprocess
from moviepy.editor import VideoFileClip

def resize_video(input_file, path,output_file):
  output_file = os.path.join(path, output_file)
  command = f'ffmpeg -i {input_file}  -r 60 -vf "crop=ih*(9/16):ih" -crf 21 -y {output_file}'
  subprocess.call(command, shell=True)

if len(sys.argv) < 2:
    print("Usage: python resize.py [input_file] [output_file] ")
    sys.exit(1)


input_file = sys.argv[1]
path = sys.argv[2]
output_file = sys.argv[3]


resize_video(input_file,path, output_file)

