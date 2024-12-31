import sys
from os import path
import cv2
import datetime
import json
from pathlib import Path
from Utils import FrameCollector, get_scene_changes, APICaller, crop_rectangles

# Contains the main logic of the video splitting process
def Process_Video(video_path, image_path, out_path, API_key='00000000-0000-0000-0000-000000000002', recognization_threshold=0.90, adaptive_threshold=2.9, crop_face=True):
    video_path = path.abspath(video_path)
    image_path = path.abspath(image_path)
    out_path = path.abspath(out_path)
    # Create the directory for storing the images
    Path(out_path).mkdir(parents=True, exist_ok=True)
    
    # Create the APICaller
    api_caller = APICaller(API_key, threshold=0.8)
    # Setup by adding the image of the face at image_path to CompreFace using APICaller
    api_caller.setup_subject(image_path)

    # Get the index of the frames that contain a scene change
    scene_changes = get_scene_changes(video_path, adaptive_threshold=adaptive_threshold)
    change_index = 0

    # Create the VideoCapture and FrameCollector
    cap = cv2.VideoCapture(video_path)
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_collector = FrameCollector(video_path, out_path, width, height, fps)

    # Main loop
    # metadata is a list of entries (dictionaries) for each cut
    # Each dictionary contains the keys "path", "start_time", "end_time", "frames"
    # "frames" is a nested list where each element is [[x, y, width, height], [x, y, width, height]] for the case where the face appears multiple times in a scene. 
    metadata = []
    metadata_frames = []
    start_index = None
    frame_index = 0
    scene_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            # End the final scene
            # If there exists a scene, then write an entry to metadata
            if frame_collector.end_scene():
                curr_entry = {
                    "path": out_path + '/' + str(scene_index) + '.mp4', 
                    "start_time": str(datetime.timedelta(seconds=start_index / fps)),
                    "end_time": str(datetime.timedelta(seconds=frame_index / fps)),
                    "frames": metadata_frames,
                }
                metadata.append(curr_entry)
                metadata_frames = []
                start_index = None
                scene_index += 1
            break
        # Use the APICaller to get the results of the current frame.
        result = api_caller.recognize_numpy(frame).json()
        # If frame_index is in scene_changes, or if there are no matching faces, then we end the current scene. We do not add the frame to the frame_collector or start a new scene if there are no matching faces.
        # Process the results and find any matching faces.
        contains_face = False
        metadata_frame = None
        if 'result' in result:
            for face in result['result']:
                similarity = face['subjects'][0]['similarity']
                if similarity >= recognization_threshold:
                    contains_face = True
                    if metadata_frame is None:
                        metadata_frame = []
                    box = face['box']
                    x_min = box['x_min']
                    x_max = box['x_max']
                    y_min = box['y_min']
                    y_max = box['y_max']
                    metadata_frame.append([x_min, y_min, x_max - x_min, y_max - y_min])

        # Increment change_index so that it alligns with the current frame.
        while change_index < len(scene_changes) and scene_changes[change_index] < frame_index:
            change_index += 1
        
        # If frame_index is in scene_changes, or if there are no matching faces, then we end the current scene.
        if (not contains_face) or scene_changes[change_index] == frame_index:
            if frame_collector.end_scene():
                curr_entry = {
                    "path": out_path + '/' + str(scene_index) + '.mp4', 
                    "start_time": str(datetime.timedelta(seconds=start_index / fps)),
                    "end_time": str(datetime.timedelta(seconds=frame_index / fps)),
                    "frames": metadata_frames,
                }
                metadata.append(curr_entry)
                metadata_frames = []
                start_index = None
                scene_index += 1
        
        # If the target face exists, then we perform the crop and add it to the FrameCollector, and add the metadata to their respective positions.
        if contains_face:
            if start_index is None:
                start_index = frame_index
            if crop_face:
                frame_collector.add_frame(crop_rectangles(frame, metadata_frame))
            else:
                frame_collector.add_frame(frame)
            metadata_frames.append(metadata_frame)

        frame_index += 1
    cap.release()

    # Save the metadata as a json file called metadata.json
    with open(out_path + '/metadata.json', "w") as f:
        json.dump(metadata, f)

def main():
    arguments = sys.argv[1:]
    Process_Video(arguments[0], arguments[1], arguments[2])

if __name__ == "__main__":
    main()