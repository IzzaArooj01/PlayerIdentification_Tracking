import os
import subprocess
from math import ceil

def split_video(video_path, output_dir, segment_duration=300):
    os.makedirs(output_dir, exist_ok=True)
    # Get video duration
    cmd = f"ffprobe -i {video_path} -show_entries format=duration -v quiet -of csv=p=0"
    try:
        duration = float(subprocess.check_output(cmd, shell=True).decode().strip())
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return
    
    total_segments = ceil(duration / segment_duration)
    for i in range(total_segments):
        start_time = i * segment_duration
        output_file = os.path.join(output_dir, f"part_{i + 1:03d}.mp4")
        cmd = (
            f"ffmpeg -i {video_path} -ss {start_time} -t {segment_duration} -c copy {output_file} -y"
        )
        subprocess.run(cmd, shell=True)
        print(f"Created: {output_file}")

video_path = "input_videos/elclassico.mp4"  # Change this to your video path
output_dir = "output_videos/elclassico"
split_video(video_path, output_dir)
