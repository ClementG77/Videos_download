import requests
import m3u8
import sys
import subprocess
import os
from pathlib import Path

url = "https://be6721.rcr72.waw04.cdn112.com/hls2/01/04942/9ue7ydn44fzo_,n,h,x,.urlset/master.m3u8?t=QMb_p8F_AShYTwz1fDTY-wN4VH8aqrRf7Bs4guntGeQ&s=1699790386&e=43200&f=24714141&srv=51&asn=5410&sp=2500"

url2 = "https://s22.anime-sama.fr/videos/Ragna%20Crimson/Ragna_Crimson_7_VOSTFR.mp4"

url3 =  "https://be4242.rcr52.ams03.cdn112.com/hls2/01/04789/koyx85eljobz_,n,h,x,.urlset/master.m3u8?t=4PPfsQ-vOa4Sw64szuCXvTMh-N5jPSNE6rMUiSwDRZw&s=1699797647&e=43200&f=23945958&srv=46&asn=5410&sp=2500"

def downloadVideoFromURL(url: str, filename: str):
    r = requests.get(url)
    m3u8_master = m3u8.loads(r.text)
    print(m3u8_master.data['playlists'])
    playlist_url = m3u8_master.data['playlists'][0]['uri']
    r = requests.get(playlist_url)
    playlist = m3u8.loads(r.text)
    with open(filename,'wb') as f:
        for segment in playlist.data['segments']:
            print("Donwloading : " + segment['uri'])
            url = segment['uri']
            r = requests.get(url)
            f.write(r.content)
    subprocess.run(['ffmpeg','-i',filename,filename.replace(".ts","HD.mp4")])
    print(filename)
    print("VIDEO : " + filename.replace(".ts","HD.mp4") + " is downloaded.")
    # os.replace(filename,os.path.join(Path(filename).absolute(),"/static/download/"))
    # os.remove(filename)

def changelocation(path):
    os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

def main():
    if len(sys.argv) < 2:
        print('Usage: python videoDownloader.py "[master_url]" [output_video_name]')
        sys.exit(1)
    master_url = sys.argv[1]
    output_video_name = sys.argv[2] +".ts"
    downloadVideoFromURL(master_url, output_video_name)
    



if __name__ == "__main__":
    main()