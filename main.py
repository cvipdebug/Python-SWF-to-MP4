import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description='Convert SWF to MP4')
    parser.add_argument('-i', '--input', type=str, help='Input SWF file', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output MP4 file', required=True)
    parser.add_argument('-f', '--fps', type=int, help='Frame rate for the output video', default=30)

    args = parser.parse_args()

    swf_file = args.input
    final_video_file = args.output
    fps = args.fps

    audio_file = "out.mp3"
    image_folder = "images"
    mp4_file = "out.mp4"

    for file_path in [audio_file, mp4_file, final_video_file]:
        if os.path.exists(file_path):
            os.remove(file_path)

    # Extract audio from SWF to MP3 using ffmpeg
    ffmpeg_command = f'ffmpeg -i {swf_file} -vn -acodec libmp3lame -q:a 4 {audio_file}'
    subprocess.run(ffmpeg_command, shell=True, check=True)

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Convert SWF to images using ffmpeg
    ffmpeg_command = f'ffmpeg -i {swf_file} -vf "fps={fps}" {image_folder}/%d.png'
    subprocess.run(ffmpeg_command, shell=True, check=True)

    # Convert images to MP4 using ffmpeg
    ffmpeg_command = f'ffmpeg -framerate {fps} -i {image_folder}/%d.png -c:v libx264 -pix_fmt yuv420p {mp4_file}'
    subprocess.run(ffmpeg_command, shell=True, check=True)

    # Combine MP3 audio with MP4 video using ffmpeg
    ffmpeg_command = f'ffmpeg -i {mp4_file} -i {audio_file} -c:v copy -c:a aac -strict experimental {final_video_file}'
    subprocess.run(ffmpeg_command, shell=True, check=True)

    # Clean up: remove audio file, image folder, and temporary MP4 file
    os.remove(audio_file)
    for file_name in os.listdir(image_folder):
        os.remove(os.path.join(image_folder, file_name))
    os.rmdir(image_folder)
    os.remove(mp4_file)

    print(f"Conversion completed. Final video file saved as '{final_video_file}'")

if __name__ == "__main__":
    main()
