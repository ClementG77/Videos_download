import os
import sys
import subprocess

def cut_video(input_file, output_folder, durationParts):
    title = os.path.basename(input_file).split(".")[0]
    duration = get_video_duration(input_file)
    part_duration = durationParts
    num_parts = int(duration / durationParts)
    remaining_duration = duration % part_duration  # Calculate the remaining duration

    if remaining_duration > 0:  # If there's a remaining duration, add an extra part
        num_parts += 1

    os.makedirs(output_folder, exist_ok=True)
    filenames = []

    for i in range(num_parts):
        start_time = i * part_duration
        if i == num_parts - 1 and remaining_duration > 0:  # Adjust the end time for the last part
            part_duration = remaining_duration
        output_file = os.path.join(output_folder, f"{title}_part{i+1}.mp4")
        command = f"ffmpeg -ss {start_time} -i {input_file} -t {part_duration} -c copy -y {output_file}"
        subprocess.call(command, shell=True)
        filenames.append(output_file)
    return filenames

def get_video_duration(input_file):
    command = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input_file}"
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    duration = float(output)
    return duration



if len(sys.argv) < 2:
    print("Usage: python cut.py [input_file] [output_folder] [Optionnal : PartDuration]")
    sys.exit(1)

input_file = sys.argv[1]
output_folder = sys.argv[2]
durationParts = sys.argv[3] if len(sys.argv) >= 4 else 60

cut_video(input_file, output_folder, int(durationParts))