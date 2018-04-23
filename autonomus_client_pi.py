import io
from io import BytesIO
import socket
import struct
import time
import picamera
import base64
import configuration
import utils.motor_driver as motor_driver_helper
import RPi.GPIO as GPIO

from PIL import Image

def Main():
    motor_driver_helper.set_gpio_pins()
    client_socket = socket.socket()
    client_socket.connect(configuration.PC_HOST_PORT)

    try:
        with picamera.PiCamera() as camera:
            camera.resolution = configuration.PICAMERA_RESOLUTION
            camera.framerate = configuration.PICAMERA_FRAMERATE
            camera.iso = configuration.PICAMERA_ISO
            camera.brightness = configuration.PICAMERA_BRIGHTNESS
            camera.sharpness = 0
            camera.contrast = 0
            camera.saturation = 0
            camera.exposure_compensation = 0
            camera.exposure_mode = 'auto'
            camera.meter_mode = 'average'
            camera.awb_mode = 'auto'
            camera.image_effect = 'none'
            camera.color_effects = None
            time.sleep(configuration.PICAMERA_WARM_UP_TIME)

            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                stream.truncate()
                stream.seek(0)
                image = Image.open(stream)
                image = image.crop((0, configuration.PICAMERA_RESOLUTION_HEIGHT / 2, configuration.PICAMERA_RESOLUTION_WIDTH, configuration.PICAMERA_RESOLUTION_HEIGHT))
                stream = io.BytesIO()
                image.save(stream, 'JPEG')
                stream.seek(0)                
                image_base64 = base64.b64encode(stream)
                
                image_len = struct.pack('!i', len(image_base64))
                client_socket.send(image_len)
                client_socket.send(image_base64)
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()

                data = client_socket.recv(4096)
                data = data.decode('utf-8')
                print ('Received: ', data, time.strftime("%M:%S"))  
                
                if data == 'stop':
                    break
                elif data == 'accelerate':
                    duty_cycle = duty_cycle + 2 if (duty_cycle + 2) <= 100 else duty_cycle
                    motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                    print('RC Speed: ' + str(duty_cycle))
                elif data == 'decelerate':
                    duty_cycle = duty_cycle - 2 if (duty_cycle - 2) >= 0 else duty_cycle
                    motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                    print('RC Speed: ' + str(duty_cycle))
                elif data == 'idle':
                    motor_driver_helper.set_idle_mode()
                elif data == 'up':
                    motor_driver_helper.set_forward_mode()
                elif data == 'down':
                    motor_driver_helper.set_reverse_mode()
                elif data == 'left':
                    motor_driver_helper.set_forward_mode()                                        
                    motor_driver_helper.set_left_mode()
                elif data == 'right':
                    motor_driver_helper.set_forward_mode()                    
                    motor_driver_helper.set_right_mode()

    finally:
        GPIO.cleanup()
        client_socket.close()

if __name__ == '__main__':
    Main()