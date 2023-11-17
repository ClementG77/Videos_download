import sys
import subprocess
import os

def blur_video(input_file,output_file):
    command = f'ffmpeg -i {input_file} -i {input_file} -filter_complex ""[0:v]scale=2276:1280,boxblur=4[bg];[1:v]scale=720:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[tmp];[tmp]crop=720:1280:(2276-720)/2:0[out]"" -map [out] -map 0:a {output_file}'
    subprocess.call(command,shell=True)



def main():
    if len(sys.argv) < 2:
        print('Usage: python videoDownloader.py "[master_url]" [output_video_name]')
        sys.exit(1)
    master_url = sys.argv[1]
    output_file = sys.argv[2]
    blur_video(master_url, output_file)



if __name__ == "__main__":
    main()