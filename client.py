#!/usr/bin/env python

import socket
import struct
import base64
import time 

ADDRESS = ("localhost", 12801)
SURFACE_SIZE = (640, 480)

s = socket.socket()
s.connect(ADDRESS)

try:
    running = True
    while running:
        # receive size
        len_str = s.recv(4)
        size = struct.unpack('!i', len_str)[0]
        print('size:', size)
        # receive string
        img_str = ''
        while size > 0:
            if size >= 4096:
                data = s.recv(4096)
                size -= len(data)  
                img_str += data.decode('utf-8')              
            else:
                data = s.recv(size)
                size -= len(data)
                img_str += data.decode('utf-8')                

        print('len:', len(img_str))
        # convert string to surface
        fh = open("imageToSave.jpg", "wb")
        fh.write(base64.b64decode(img_str))
        fh.close()
        data = 'I got the image'
        s.send(data.encode())
        time.sleep(0.5)
        

except Exception as e:
    print(e)
finally:
    # exit
    print("Closing socket and exit")
    s.close()