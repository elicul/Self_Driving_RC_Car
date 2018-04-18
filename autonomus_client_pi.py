import io
import socket
import struct
import time
import picamera
import configuration

def Main():
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    img_client_socket = socket.socket()
    img_client_socket.connect(('192.168.0.193', 8090))

    txt_client_socket = socket.socket()
    txt_client_socket.connect(('192.168.0.193', 8080))

    # Make a file-like object out of the img_connection
    img_connection = img_client_socket.makefile('wb')
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

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to img_connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                data = txt_client_socket.recv(1024).decode()
                print ('Received from server: ' + data)

                img_connection.write(struct.pack('<L', stream.tell()))
                img_connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                img_connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                if time.time() - start > 30:
                    break
                
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        img_connection.write(struct.pack('<L', 0))
    finally:
        img_connection.close()
        img_client_socket.close()
        txt_connection.close()
        txt_client_socket.close()

if __name__ == '__main__':
    Main()