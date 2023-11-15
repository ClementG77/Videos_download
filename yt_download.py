import sys, os
from pathlib import Path
from pytube import YouTube


def download_video_from_youtube(link, path, output_file):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    # download the video
    file = video.download(path)
    output_file = os.path.join(Path(path).absolute(),output_file)
    print(output_file)
    os.rename(file,output_file)



def main():
    if len(sys.argv) < 2:
        print('Usage: python videoDownloader.py "[master_url]" [output_video_name]')
        sys.exit(1)
    master_url = sys.argv[1]
    path = sys.argv[2] 
    output_file = sys.argv[3]
    download_video_from_youtube(master_url, path, output_file)



if __name__ == "__main__":
    main()