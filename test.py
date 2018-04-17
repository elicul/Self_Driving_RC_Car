#!/usr/bin/env python
"""Run the car autonomously"""
import time
import sys
import io
import configuration
from PIL import Image
from io import BytesIO
from predict import Predictor
import utils.image as image_helper
import sys  
from configuration import PICAMERA_RESOLUTION_HEIGHT, PICAMERA_RESOLUTION_WIDTH

def autonomous_control(model):
    """Run the car autonomously"""
    predictor = Predictor(model)

    img = Image.open('./right/1.image-forward_right-1468922074.56.jpg').convert('L')
    output = BytesIO()
    img.save(output, format='jpeg')
    #output.seek(0)
    img2 = Image.open(output)
    img2.show()
    direction = predictor.predict(output)
    print(direction)

def main():
    """Main function"""
    model = None
    if len(sys.argv) > 1:
        model = sys.argv[1]
    autonomous_control(model)

if __name__ == '__main__':
    main()
