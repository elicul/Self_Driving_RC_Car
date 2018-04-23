#!bin/bash
rsync -avz --progress -e ssh pi@192.168.0.187:/home/pi/Self_Driving_RC_Car/images /home/elicul/Documents/GitRepos/Self_Driving_RC_Car
echo "Transfer of images successfully finished!"