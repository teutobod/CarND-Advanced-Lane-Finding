#Advanced Lane Finding Project

### Camera Calibration and Image Processing Pipeline

The code and documentation of the camera calibration and the whole image processing pipeline
can be found inside this [jupiter notebook](./advanced_lane_finding.ipynb).

---

### Pipeline (video)
The final video is also included in the jupiter notebook mentioned above.
The video file can be found [here](./output_videos/project_video_ouput.mp4).

---

### Discussion

As shown by the video the pipeline really works well for most of the time, especially under ideal condition.
During the end it can be seen that the lane detection has some issues with dark shadows on the road and 
the detection lines are slightly wobbling.

To make the lane detection more robust in very shadow conditions, I guess the binary thresholding needs to improved.
I would need to investigate if any other combination of channels selection and/or fine tuning the threshold values
will lead to better results.

Another idea could be to vary the thresholding parameters depending on the properties of captured image.
To implement this approach each image would need to be further analyzed before the thresholding is applied.
Relevant properties could be the overall image brightness, contrast, etc.

