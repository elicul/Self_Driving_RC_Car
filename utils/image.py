"""Image helpers"""
import time
from PIL import Image

def save_image_with_direction(stream, direction):
    """Save image"""
    stream.seek(0)
    image = Image.open(stream)
    image = image.crop((0, PICAMERA_RESOLUTION_HEIGHT / 2, PICAMERA_RESOLUTION_WIDTH, PICAMERA_RESOLUTION_HEIGHT))
    image.save('images/' + direction + '/image%s.jpg' % ("-" + direction + "-"+ str(time.time())), format="JPEG")
