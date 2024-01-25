from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp

def convert_to_gif():
    input_video_path = 'test_video.mp4'
    output_gif_path = 'animation.gif'

    crop_region = ((190, 236), (80, 220))
    video_clip = VideoFileClip(input_video_path)

    cropped_clip = video_clip.crop(x1=crop_region[1][0], x2=crop_region[1][1], y1=crop_region[0][0], y2=crop_region[0][1])
    cropped_clip.write_gif(output_gif_path, fps=24)

    video_clip.close()
