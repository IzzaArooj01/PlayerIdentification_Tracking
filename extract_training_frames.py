import os
import glob
import subprocess
def extract_frames(video_dir, output_dir, frame_interval=30):
    os.makedirs(output_dir, exist_ok=True)
    video_files = glob.glob(os.path.join(video_dir, "*.mp4"))
    
    for video in video_files:
        video_name = os.path.splitext(os.path.basename(video))[0]
        frame_dir = os.path.join(output_dir, video_name)
        os.makedirs(frame_dir, exist_ok=True)
        
        cmd = (
            f"ffmpeg -i {video} -vf 'select=not(mod(n\\,{frame_interval}))' "
            f"-vsync vfr {frame_dir}/frame_%04d.jpg -hide_banner"
        )
        subprocess.run(cmd, shell=True)
        print(f"Extracted frames for {video} into {frame_dir}")

video_dir = "training_videos/elclassico"
output_dir = "frames/elclassico"
extract_frames(video_dir, output_dir)
