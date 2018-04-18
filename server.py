#!/usr/bin/env python

import socket
import struct # to send `int` as  `4 bytes`
import time   # for test
import base64

from PIL import Image

ADDRESS = ("localhost", 12801)

s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDRESS)
s.listen(1)

print("Wait for connection")

try:
    sc, info = s.accept()
    print("Video client connected:", info)
    while True:
        # get image surface
        #image = self.cam.get_image()
        # convert surface to string
        with open("test.jpg", "rb") as imageFile:
            img_str = base64.b64encode(imageFile.read())

        print('len:', len(img_str))
        # send string size
        len_str = struct.pack('!i', len(img_str))
        sc.send(len_str)
        # send string image
        sc.send(img_str)
        # wait
        time.sleep(0.5)
        data = sc.recv(4096)
        print(data.decode('utf-8'))

except Exception as e:
    print(e)
finally:
    # exit
    print("Closing socket and exit")
    sc.close()
    s.close()