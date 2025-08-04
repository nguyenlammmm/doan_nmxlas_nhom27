def get_frame(video_capture):
    ret, frame = video_capture.read()
    return frame
