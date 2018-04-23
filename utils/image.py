"""Image helpers"""
import time
import configuration
from PIL import Image

def save_image_with_direction(stream, direction):
    """Save image"""
    stream.seek(0)
    image = Image.open(stream)
    image = image.crop((0, configuration.PICAMERA_RESOLUTION_HEIGHT / 2, configuration.PICAMERA_RESOLUTION_WIDTH, configuration.PICAMERA_RESOLUTION_HEIGHT))
    image.save('images/' + direction + '/image%s.jpg' % ("-" + direction + "-"+ str(time.time())), format="JPEG")
