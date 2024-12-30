from ProcessVideo import Process_Video
import time

# Add an APIKey here
api_key = None
api_key_demo = '00000000-0000-0000-0000-000000000002'

# Thresholds
recognization_threshold = 0.90
adaptive_threshold = 2.9

def main():

    # Time the runtime
    start_time = time.time()

    # Process the first video with a first target
    target_path = '../targets/target0_0_1080.png'
    video_path = '../videos/video0_1080.mp4'
    out_folder = '../processed_videos/video0_0_1080'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    # Process the first video with the second target
    target_path = '../targets/target0_1_1080.png'
    video_path = '../videos/video0_1080.mp4'
    out_folder = '../processed_videos/video0_1_1080'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    # Process the second video (480p) with a corresponding target
    target_path = '../targets/target1_480.png'
    video_path = '../videos/video1_480.mp4'
    out_folder = '../processed_videos/video1_480'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    # Process the second video (1080p) with a corresponding target
    target_path = '../targets/target1_1080.png'
    video_path = '../videos/video1_1080.mp4'
    out_folder = '../processed_videos/video1_1080'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    # Process the third video with a corresponding target
    target_path = '../targets/target2_1080.png'
    video_path = '../videos/video2_1080.mp4'
    out_folder = '../processed_videos/video2_1080'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    # Process the fourth video with a corresponding target
    target_path = '../targets/target3_1080.png'
    video_path = '../videos/video3_1080.mp4'
    out_folder = '../processed_videos/video3_1080'
    Process_Video(video_path, target_path, out_folder, API_key=api_key_demo, recognization_threshold=recognization_threshold, adaptive_threshold=adaptive_threshold, crop_face=True)

    end_time = time.time()
    print("Elapsed Time: " + str((end_time - start_time) / 60.0) + " minutes")
    

if __name__ == "__main__":
    main()