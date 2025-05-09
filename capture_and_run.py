import cv2
import time
import subprocess
import os
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

def capture_video(duration=3, fps=30, save_dir="input_videos"):
    """
    Capture video using libcamera-vid and convert it to MP4 format
    """
    import datetime

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    h264_file = f"{save_dir}/video_{timestamp}.h264"
    mp4_file = f"{save_dir}/video_{timestamp}.mp4"

    print(f"Recording video for {duration} seconds...")

    try:
        # Record using libcamera-vid
        subprocess.run([
            "libcamera-vid",
            "-t", str(duration * 1000),  # time in milliseconds
            "--width", "640",
            "--height", "480",
            "--framerate", str(fps),
            "-o", h264_file
        ], check=True)

        print("Converting to MP4 format...")

        # Convert to mp4 using MP4Box
        subprocess.run(["MP4Box", "-add", h264_file, mp4_file], check=True)

        os.remove(h264_file)  # optional cleanup
        print(f"Video saved as: {mp4_file}")
        return mp4_file

    except subprocess.CalledProcessError as e:
        print(f"Error during video capture or conversion: {e}")
        return False
def run_input_script():
    """Run the input.py script"""
    print("\nRunning input.py...")
    try:
        subprocess.run(["python", "input.py"], check=True)
        print("input.py completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running input.py: {e}")
        return False
    except FileNotFoundError:
        print("Error: input.py not found in the current directory.")
        return False

def main():
    print("Starting video capture process...")
    
    # Capture video for 3 seconds
    video_file = capture_video(duration=3)
    
    if video_file:
        print(f"\nSuccessfully captured video: {video_file}")
    else:
        print("Video capture failed.")
    
    # Run the input.py script
    run_input_script()

if __name__ == "__main__":
    main()
