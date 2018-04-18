import io
import socket
import struct
import time
import picamera
import configuration

def Main():
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect(('192.168.0.193', 8090))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
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
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                #data = client_socket.recv(1024).decode()
                #print(data)
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                if time.time() - start > 30:
                    break
                
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
                txt_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not txt_len:
                    break
                txt_stream = io.BytesIO()
                txt_stream.write(connection.read(txt_len))
                txt_stream.seek(0)
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()

if __name__ == '__main__':
    Main()