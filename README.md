Take-Home project for HeyGen (https://www.heygen.com/)

SetUp Instructions:

Setting up CompreFace, an open source facial recognition service: 

To run the code, download and extract the Docker Compose file for CompreFace found at https://github.com/exadel-inc/CompreFace/releases/tag/v1.2.0

1. Enter the directory of the folder (CompreFace_1.2.0).
3. Enter the folder custom-builds and select the desired build. Information about the custom builds and detailed instructions can be found at https://github.com/exadel-inc/CompreFace/blob/master/custom-builds/README.md. The build used to generate the examples found in processed_videos_ArcFace is located in the directory SubCenter-ArcFace-r100-gpu. Enter the folder of the desired build and run the command: docker-compose up -d 
Make sure to run this command in an elevated terminal.
The default port is 8000. If a different port is desired, the port number can be changed in the respective's folder's docker-compose file. If this is done, the port will need to be changed in src/Utils.py, and the login address in step 4 will be different.
4. Visit http://localhost:8000/login, create an account and login (the accounts are stored locally and the emails are not checked to be valid). Once logged in, you will be prompted to create a service. Make sure to select Recognition as the type of the service. An API key for the demo services are also generated upon account creation. These demo API keys are fixed, and are included in the script. To use the API key of the non-demo service, add it to processvideos_test.py and replace the parameters passed from api_key_demo to api_key.

Setting up other dependencies: 

To install the dependencies, enter the main directory (heygen-project), and run the command: pip install -r requirements.txt

Replicating Results:

To replicate the results in processed_videos_ArcFace, enter the /src directory and run the command: python processvideos_test.py

On a laptop with a i9-13900HX CPU with 24 cores and a NVIDIA RTX 4060 Laptop GPU, all the videos took approximately 32 minutes to run using CompreFace's ArcFace GPU build.

Command line calls are also supported for the default threshold values of recognization_threshold = 0.90
adaptive_threshold = 2.9
using the demo API key of '00000000-0000-0000-0000-000000000002'
To call the Process_Video function from a terminal, run the command:
python ProcessVideo.py "video path" "target path" "out path"

Where video path is the path to the video to be processed, target path is the path to an image of the target person, and out path is the name of the directory where the results will be wrote to.
To run ProcessVideo on videos/video1_480.mp4 with target image targets/target1_480.png with the outputs being written to processed_videos/video1_480, enter the src/ directory and run the command:
python ProcessVideo.py "../videos/video1_480.mp4" "../targets/target1_480.png" "../processed_videos/video1_480"

The function also creates a json file containing the metadata of each clip.
The metadata file is a list of dictionary objects. Each dictionary object corresponds to a clip, and they are in the order of the clips.
The clip dictionary contains the fields:
path: the absolute path of the clip
start_time: the start time of the clip with respect to the original video
end_time: the end time of the clip with respect to the original video
frames: a nested list containing the bounding box of faces recognized to be the target face
frames[i] is a list of bounding boxes for the ith frame.
frames[i][0] is a list of 4 elements: [x, y, width, height] respresenting the bounding box of a face recognized to be the target face.
frames[i] might contain more than 1 bounding box in the event of multiple faces being recognized as the target face. If this is the case, then frames[i][1] will be a list of 4 elements representing the bounding box of the second face etc.


About the Code

The main function for processing videos is located in src/ProcessVideo.py
The script to process the videos is src/processvideos_test.py.
The utility functions used in this function are located in Utils.py
The main function takes in the variables recognization_threshold, adaptive_threshold, and the api key along with the files of the video, target image, and output folder.

The folder videos contains some test videos to use. The test videos are HeyGen Advertisements with the links:
https://www.youtube.com/watch?v=Y3225dV0lyQ
https://www.youtube.com/watch?v=0AqxnXHcUes
https://www.youtube.com/watch?v=hXPV_twtuHY
https://www.youtube.com/watch?v=zxbSV98VnhY

The target images were screenshots taken from their respective videos. Some of the videos feature the target person in different poses with different outfits. 

The ProcessVideo algorithm uses CompreFace (https://github.com/exadel-inc/CompreFace) to detect faces in each frame and to recognize the target face. The variable recognization_threshold is used to detect the existence of the target face in the frame with a similarity score greater than or equal to the recognization threshold being accepted.

Some of the videos contain very difficult scenes comprised of multiple very small moving target faces, and CompreFace's Mobilenet often stuggled on some of the scenes. CompreFace's ArcFace performs much better.

The ProcessVideo algorithm also utilizes PySceneDetect (https://github.com/Breakthrough/PySceneDetect) to detect scene changes, which should result in a new clip. The variable adaptive_threshold is the threshold used to detect jumpcuts.

Assumptions and Limitations:

The repository was delevoped using Windows and the code has not been tested for any other architectures.

To run the functions in the terminal, the terminal will need to be in the directory of the function.

Any files in the out folder with the same name will be overwritten.
So far, mp4 is the only supported video format. The clips are compressed using mp4v.
The clips also do not include any audio.

The port number (8000) is hard-coded into the functions. If the port number is changed, the few instances in Utils.py will need to be changed. 

The threshold values used in CompreFace and PySceneDetect were arrived at through some experimentation. More optimal values might exist, and they might vary between videos. The thresholds can be changed in the functions in src/Utils.py

Time benchmarking has not been done with the CPU builds. They could potentially be much slower.
There is a trade-off between the speed and accuracy for the CompreFace builds. The ArcFace recognization model performs better with some of the more difficult examples, but it is slightly slower than the Mobilenet build. Sometimes, really small faces are not detected by both builds.




A potential direction to take this project in would be to implement parallelization with multiple workers interacting with their own CompreFace server to speed up the face recognition step.

Another direction would be to improve the detection step. Perhaps reducing the required threshold for a detected face in the current frame if the previous frame contained the target face with a bounding box nearby would improve the performance of the detection step.
