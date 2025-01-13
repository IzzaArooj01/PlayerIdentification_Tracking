import os
import shutil
import glob

def copy_videos(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all video files sorted alphabetically
    video_files = sorted(glob.glob(os.path.join(input_dir, "*.mp4")))
    if len(video_files) < 2:
        print("Not enough videos found to copy. At least two videos are required.")
        return

    # Determine the videos to copy
    first = video_files[0]
    second = video_files[1]  # Ensures there are at least two videos
    middle = video_files[len(video_files) // 2]
    last = video_files[-1]
    
    # Copy the selected videos
    for video in [first, second, middle, last]:
        if os.path.exists(video):  # Ensure the video exists before copying
            shutil.copy(video, os.path.join(output_dir, os.path.basename(video)))
            print(f"Copied {video} to {output_dir}")
        else:
            print(f"File {video} not found!")

# Define input and output directories
input_dir = "output_videos/elclassico"
output_dir = "training_videos/elclassico"

# Call the function
copy_videos(input_dir, output_dir)
