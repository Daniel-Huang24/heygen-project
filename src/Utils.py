import cv2
from io import BytesIO, BufferedReader
import numpy as np
import requests
from scenedetect import detect, AdaptiveDetector, ThresholdDetector

# Manages the VideoWriter objects from OpenCV
class FrameCollector:
    def __init__(self, video_path, out_path, width, height, fps):
        self.video_path = video_path
        self.out_path = out_path
        self.vid_size = (width, height)
        self.fps = fps
        self.curr_vid_ct = 0
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.curr_vid_writer = None
    
    # Check whether the FrameCollector is in a scene
    def in_scene(self):
        return self.curr_vid_writer is not None

    # Add a new frame to the VideoWriter
    def add_frame(self, frame):
        if self.curr_vid_writer is None:
            self.curr_vid_writer = cv2.VideoWriter(self.out_path + '/' + str(self.curr_vid_ct) + '.mp4', self.fourcc, self.fps, self.vid_size)
        self.curr_vid_writer.write(frame)
    
    # A new scene requires a new video, change the VideoWriter and increment self.curr_vid_ct
    # If there is no scene, then do not increment self.curr_vid_ct
    def end_scene(self):
        if self.in_scene():
            self.curr_vid_writer.release()
            self.curr_vid_writer = None
            self.curr_vid_ct += 1
            return True
        return False




# Utility class for calling API's for CompreFace
# Contains methods for setting up the reference image, and for recognizing the image
class APICaller:
    # api_key: the api key to be used
    # threshold: the threshold for whether the image is a face
    def __init__(self, api_key='00000000-0000-0000-0000-000000000002', threshold=0.8):
        self.url_recognize = 'http://localhost:8000/api/v1/recognition/recognize'
        self.url_subjects = 'http://localhost:8000/api/v1/recognition/subjects'
        self.url_faces = 'http://localhost:8000/api/v1/recognition/faces'
        self.headers_dict = {
            'x-api-key': api_key, 
        }
        self.params_dict_rec = {
            'limit': '0', 
            'det_prob_threshold': str(threshold), 
            'prediction_count': '1', 
        }

    # Sets up the subject for recognition
    # Deletes all existing subjects, adds a single subject called 'person1', and adds the image at image_path as an example of 'person1'
    def setup_subject(self, image_path):
        # Delete all subjects
        response = requests.delete(self.url_subjects, headers=self.headers_dict)

        subject_dict = {
            'subject': 'person1',
        }
        # Adds a single subject called 'person1'
        response = requests.post(self.url_subjects, headers=self.headers_dict, json=subject_dict)
        # Adds the image at image_path as an example of 'person1', and returns the response as a dictionary
        with open(image_path, 'rb') as f:
            files_dict = {
                'file': f,
            }
            response = requests.post(self.url_faces, params=subject_dict, headers=self.headers_dict, files=files_dict)
        return response
        
    # Calls the recognization service on the frame, a numpy array
    def recognize_numpy(self, frame):
        # Converts frame to a in-memory jpg file to minimize io
        _, img = cv2.imencode('.jpg', frame)
        buf = BytesIO(img.tobytes())
        # Gives the buffer a name ending in .jpg so CompreFace knows that the file is in jpg format
        buf.__dict__['name'] = 'memory/frame.jpg'
        files_dict = {
            'file': buf, 
        }
        result = requests.post(self.url_recognize, params=self.params_dict_rec, headers=self.headers_dict, files=files_dict)
        return result




# Returns a list containing the frame number of the beginning of each scene change of the video at video_path
def get_scene_changes(video_path, adaptive_threshold=2.7, min_scene_len=15, window_width=6, min_content_val=12.0, threshold=12, fade_bias=0.0, add_final_scene=False):
    # Adaptive Detector detects quick scene changes
    adaptive_detector = AdaptiveDetector(adaptive_threshold=adaptive_threshold, min_scene_len=min_scene_len, window_width=window_width, min_content_val=min_content_val)
    # Threshold Detector detects fade ins/outs
    threshold_detector = ThresholdDetector(threshold=threshold, min_scene_len=min_scene_len, fade_bias=fade_bias, add_final_scene=add_final_scene)

    scenes_adapt = detect(video_path, adaptive_detector, stats_file_path=None, show_progress=False, start_time=None, end_time=None, start_in_scene=True)
    scenes_thresh = detect(video_path, threshold_detector, stats_file_path=None, show_progress=False, start_time=None, end_time=None, start_in_scene=True)

    # Merge the start frames
    frames_arr = []
    for scene in scenes_adapt:
        frames_arr.append(scene[0].get_frames())
    for scene in scenes_thresh:
        frames_arr.append(scene[0].get_frames())
    frames_arr = list(set(frames_arr))
    frames_arr.sort()
    return frames_arr

# Crops out all areas other than the areas in the rectangles.
# frame is a numpy array, and each rectangle in rectangles is represented by [x, y, width, height]
def crop_rectangles(frame, rectangles):
    # Create a mask with the same shape as frame
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    # Draw filled rectangles on the mask
    for x_min, y_min, width, height in rectangles:
        cv2.rectangle(mask, (x_min, y_min), (x_min + width, y_min + height), 255, -1)

    # Apply the mask to the image
    return cv2.bitwise_and(frame, frame, mask=mask)