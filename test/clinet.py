from PIL import Image
from datetime import datetime
from io import BytesIO
from time import sleep

import io
import socket
import struct
import time
import base64
import xlsxwriter

workbook = xlsxwriter.Workbook('Client_time.xlsx')
worksheet = workbook.add_worksheet()

def current_mili_time():
  return int(round(time.time() * 1000))

def Main():
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 8080))
    stream = io.BytesIO()

    row = 0
    worksheet.write(row, 0, 'Start time')
    worksheet.write(row, 1, 'End time')
    row += 1

    try:
        while True:
            start_time = datetime.utcnow()
            worksheet.write(row, 0, "%s" % (start_time.microsecond/1000))        
            # Capture image
            sleep(0.017)            
            image = Image.open('test.jpg')
            g_image = image.convert('L')
            g_image.save(stream, 'JPEG')  
            stream.seek(0)            
            image_base64 = base64.b64encode(stream.read())
            # Send image
            image_len = struct.pack('!i', len(image_base64))
            client_socket.send(image_len)
            client_socket.send(image_base64)
            # Receve tensorflow data
            data = client_socket.recv(4096)
            data = data.decode('utf-8')
            print ('Received: ', data)
            # Send data to motors
            sleep(0.001)
            now = datetime.utcnow()
            #worksheet.write(row, 1, "%s" % (now.microsecond/1000))                                               
            stream.seek(0)
            stream.truncate()     
            delay = ((start_time.microsecond/1000)+331)-(now.microsecond/1000)
            if delay > 1000:
                delay -= 1000
            sleep(delay/1000)
            now = datetime.utcnow()
            worksheet.write(row, 1, "%s" % (now.microsecond/1000))  
            row += 1                        
    finally:
        workbook.close()    
        client_socket.close()

if __name__ == '__main__':
    Main()