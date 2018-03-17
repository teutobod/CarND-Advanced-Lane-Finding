import os
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from moviepy.editor import VideoFileClip

from find_lanes import LineFitter
from calibration import Calibration
from perspective import Transformer
from pipeline import Pipeline

calibration = Calibration()
calibration.calibrate('camera_cal')

transform = Transformer()
line_fitter = LineFitter()

pipeline = Pipeline(calibration,transform,line_fitter)

test_images = 'test_images/*.jpg'

for img_name in glob.glob(test_images):
    img = mpimg.imread(img_name)

    pipeline.process_image(img, debug=True)
    plt.show()
    break

output_videos_folder = 'output_videos'
if not os.path.exists(output_videos_folder):
    os.makedirs(output_videos_folder)

video_output = output_videos_folder + '/project_video_ouput.mp4'
clip = VideoFileClip("videos/project_video.mp4")

white_clip = clip.fl_image(pipeline.process_image)
white_clip.write_videofile(video_output, audio=False)