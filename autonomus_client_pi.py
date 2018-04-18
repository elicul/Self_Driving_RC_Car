import io
import socket
import struct
import time
import picamera
import base64
import configuration

def Main():
    client_socket = socket.socket()
    client_socket.connect(('192.168.0.193', 8090))

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
                stream.seek(0)
                image_base64 = base64.b64encode(stream.read())
                #!Remove
                if time.time() - start > 30:
                    break
                
                image_len = struct.pack('!i', len(image_base64))
                client_socket.send(image_len)
                client_socket.send(image_base64)
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()

                data = client_socket.recv(4096)
                print(data.decode('utf-8'))
    finally:
        client_socket.close()

if __name__ == '__main__':
    Main()