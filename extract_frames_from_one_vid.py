import os
import subprocess

def extract_frames_from_video(video_path, output_dir, frame_interval=1):
    """
    Extract frames from a single video and save them into the specified directory.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Path to the output directory where frames will be saved.
        frame_interval (int): Interval of frames to extract (default is every frame).
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract the base name of the video file (without extension)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_dir = os.path.join(output_dir, video_name)
    os.makedirs(frame_dir, exist_ok=True)

    # Construct ffmpeg command
    cmd = (
        f"ffmpeg -i {video_path} -vf 'select=not(mod(n\\,{frame_interval}))' "
        f"-vsync vfr {frame_dir}/frame_%04d.jpg -hide_banner"
    )
    
    # Execute ffmpeg command
    subprocess.run(cmd, shell=True)
    print(f"Extracted frames for {video_path} into {frame_dir}")

# Example usage
video_path = "output_videos/elclassico/part_004.mp4"
output_dir = "frames/elclassico/testing"
extract_frames_from_video(video_path, output_dir, frame_interval=1)
