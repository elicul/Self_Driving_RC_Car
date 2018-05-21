from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image

import io
import socket
import struct
import numpy as np
import tensorflow as tf
import time
import configuration
import pygame
import pygame.font
import base64
import xlsxwriter

PAUSE = False

workbook = xlsxwriter.Workbook('Server_time.xlsx')
worksheet = workbook.add_worksheet()

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def current_mili_time():
  return int(round(time.time() * 1000))

def get_keys():
  change = False
  stop = False
  key_to_global_name = {
      pygame.K_ESCAPE: 'QUIT',
      pygame.K_q: 'QUIT',
      pygame.K_p: 'PAUSE'
  }
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      stop = True
    elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
      if event.key in {pygame.K_q, pygame.K_ESCAPE}:
        stop = True
      else:
        down = (event.type == pygame.KEYDOWN)
        if event.key in key_to_global_name:
          globals()[key_to_global_name[event.key]] = down
  return (PAUSE, stop)

def pygame_init():
  """Setup the Pygame Interactive Control Screen"""
  pygame.init()
  display_size = (375, 559)
  screen = pygame.display.set_mode(display_size)  
  pygame.display.set_caption('RC Autonomous Drive Mode')
  background_image = pygame.image.load("instructions/autonomous.jpg").convert()  
  screen.blit(background_image, (0, 0))
  pygame.display.flip()

def Main():
  model_file = './tensorflow/car-model.pb'
  label_file = './tensorflow/car-labels.txt'
  input_height = 128
  input_width = 128
  input_mean = 128
  input_std = 128
  input_layer = 'Placeholder'
  output_layer = 'final_result'

  graph = load_graph(model_file)
  input_name = 'import/' + input_layer
  output_name = 'import/' + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  server_socket = socket.socket()
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
  server_socket.bind(configuration.PC_HOST_PORT)
  server_socket.listen(0)
    
  connection = server_socket.accept()[0]
  pygame_init()

  row = 0

  worksheet.write(row, 0, 'Receve image')
  worksheet.write(row, 1, 'Decode image')
  worksheet.write(row, 2, 'Tensorflow calculation')
  worksheet.write(row, 3, 'Send data')
  worksheet.write(row, 4, 'Full time')
  
  row += 1
  try:    
    while True:
      start_time = current_mili_time()      
      pause, stop = get_keys()
      if stop:
        print('Stop server')
        break
      if not pause:
        image_len = connection.recv(4)
        image_size = struct.unpack('!i', image_len)[0]
        image_base64 = ''

        img_time = current_mili_time()
        while image_size > 0:
          if image_size >= 4096:
            data = connection.recv(4096)
            image_size -= len(data)  
            image_base64 += data.decode('utf-8')              
          else:
            data = connection.recv(image_size)
            image_size -= len(data)
            image_base64 += data.decode('utf-8')                
        #print ('Receve image time:', current_mili_time() - img_time)
        worksheet.write(row, 0, current_mili_time() - img_time)
        
        img_time = current_mili_time()
        image = open(configuration.TMP_BUFFER_DIR + 'pi_image.jpg', 'wb')
        image.write(base64.b64decode(image_base64))
        image.close()
        #print ('Decode image time:', current_mili_time() - img_time)        
        worksheet.write(row, 1, current_mili_time() - img_time)
        
        tensor_time = current_mili_time()        
        t = read_tensor_from_image_file(
          configuration.TMP_BUFFER_DIR + 'pi_image.jpg',
          input_height=input_height,
          input_width=input_width,
          input_mean=input_mean,
          input_std=input_std)
        
        with tf.Session(graph=graph) as sess:
          results = sess.run(output_operation.outputs[0], {
              input_operation.outputs[0]: t
          })
        results = np.squeeze(results)
        top_k = results.argsort()[-1:][::-1]
        labels = load_labels(label_file)
        #print ('Tensorflow calculation time:', current_mili_time() - tensor_time)        
        worksheet.write(row, 2, current_mili_time() - tensore_time)

        img_time = current_mili_time()        
        for i in top_k:
          data = labels[i]
        connection.send(data.encode())
        #print ('Send data time:', current_mili_time() - img_time)        
        worksheet.write(row, 3, current_mili_time() - img_time)

        worksheet.write(row, 4, current_mili_time() - start_time)
        #print('Full server time: ', current_mili_time()-start_time) 
        row += 1           
    pygame.quit()
  finally:
    connection.close()
    server_socket.close()

if __name__ == '__main__':
  Main()