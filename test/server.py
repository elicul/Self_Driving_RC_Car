from PIL import Image
from datetime import datetime
from time import sleep

import io
import socket
import struct
import numpy as np
import time
import base64
import xlsxwriter


workbook = xlsxwriter.Workbook('Server_time.xlsx')
worksheet = workbook.add_worksheet()

def current_mili_time():
  return int(round(time.time() * 1000))

def Main():
  server_socket = socket.socket()
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
  server_socket.bind(('127.0.0.1', 8080))
  server_socket.listen(0)
    
  connection = server_socket.accept()[0]

  row = 0
  worksheet.write(row, 0, 'Start time')
  worksheet.write(row, 1, 'End time')
  row += 1

  try:    
    while True:
        now = datetime.utcnow()
        worksheet.write(row, 0, "%s" % (now.microsecond)) 
        # Receve image size
        image_len = connection.recv(4)
        image_size = struct.unpack('!i', image_len)[0]
        image_base64 = ''
        print(image_size)
        #Receve image
        while image_size > 0:
          if image_size >= 4096:
            data = connection.recv(4096)
            image_size -= len(data)  
            image_base64 += data.decode('utf-8')              
          else:
            data = connection.recv(image_size)
            image_size -= len(data)
            image_base64 += data.decode('utf-8')                
        # Decode image        
        image = open('pi_image.jpg', 'wb')
        image.write(base64.b64decode(image_base64))
        image.close()
        # Tensorflow
        sleep(0.150)
        data = 'idle'
        connection.send(data.encode())
        now = datetime.utcnow()
        worksheet.write(row, 1, "%s" % (now.microsecond)) 
        row += 1           
  finally:
    workbook.close()
    connection.close()
    server_socket.close()

if __name__ == '__main__':
  Main()