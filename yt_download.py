import sys
from pytube import YouTube


def download_video_from_youtube(link, path):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    # download the video
    video.download(path)


def main():
    if len(sys.argv) < 2:
        print('Usage: python videoDownloader.py "[master_url]" [output_video_name]')
        sys.exit(1)
    master_url = sys.argv[1]
    output_video_name = sys.argv[2] +".ts"
    download_video_from_youtube(master_url, output_video_name)



if __name__ == "__main__":
    main()