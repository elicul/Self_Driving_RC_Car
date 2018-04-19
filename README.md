# Self Driving RC Car
## University of Rijeka Faculty of Engineering <br >
### Computer Science Final Year Project

<br >

### Dependencies
* Hardware
    - Raspberry Pi 3 
    - Raspberry Pi Camera Module v2
    - L293D DC motor driver module
    - Powerbank (20 000 mAh)
* Software
    - Rspbian Stretch 
    - Python 3.6
        - Numpy
        - Pygame
        - Picamera
        - Tensorflow
        - Pillow

<br >

### About
- tensorflow/
- ***retrain.py***: Retrain the existing tensorflow model with our new collected training data images from the images folder.

- utils/
  -	***image.py***: A utility script to save images.
  - ***motor_driver.py***: A utility script for controlling our RC car motors. 
    
- /
  -	***autonomus_client_pi.py***: Autonomous client which is used on our raspberry pi.
  - ***autonomus_server_pc.py***: Autonomous server runned on our pc.
  -	***train_client_pc.py***: Client used for collecting the training data, on our pc.
  - ***train_server_pi.py***: Server used for collecting the training data, on our raspberry pi.
  - ***configuration.py***: Configuration variables.