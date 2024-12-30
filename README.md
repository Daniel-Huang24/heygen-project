Take-Home project for HeyGen (https://www.heygen.com/)

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

The API key demo is created along with the account, and any other API keys can be created using the interface at http://localhost:8000/.

Some of the videos contain very difficult scenes comprised of multiple very small target faces, and CompreFace's Mobilenet often stuggles on some of the scenes. CompreFace's ArcFace performs much better.

The ProcessVideo algorithm also utilizes PySceneDetect (https://github.com/Breakthrough/PySceneDetect) to detect scene changes, which results in a new clip. The variable adaptive_threshold is the threshold used to detect jumpcuts. 

To duplicate the results in the folder processed_videos, run src/processvideos_test.py On a i9-13900HX with 24 cores and a NVIDIA RTX 4060 Laptop GPU, all the videos took approximately 32 minutes to run using CompreFace's ArcFace GPU build.

To run the code, download the Docker Compose file for CompreFace found at https://github.com/exadel-inc/CompreFace/releases/tag/v1.2.0

1. Enter the directory of the folder (CompreFace_1.2.0).
3. Enter the folder custom-builds and select the desired build. Information about the custom builds and detailed instructions can be found at https://github.com/exadel-inc/CompreFace/blob/master/custom-builds/README.md. The build used to generate the examples is SubCenter-ArcFace-r100-gpu. Enter the folder of the desired build and run docker-compose up -d 
4. Visit http://localhost:8000/login, create an account and login. An API key for the demo service is generated upon account creation, but new services can be created. Creating a new service is optional but creating an account is required. When creating a new service, make sure to select Recognition for the type. To use this API key, add it to processvideos_test.py and replace the parameters passed from api_key_demo to api_key.

To install the dependencies, enter the main directory (heygen-project), and run the command: pip install -r requirements.txt

To replicate the results in processed_videos_ArcFace, enter the /src directory and run the command: python processvideos_test.py