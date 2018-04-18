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

RESUME = PAUSE = False

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
      pygame.K_r: 'RESUME',
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
        change = (event.key in key_to_global_name)
        if event.key in key_to_global_name:
          globals()[key_to_global_name[event.key]] = down
  return (change, RESUME, PAUSE, stop)

def pygame_init():
  """Setup the Pygame Interactive Control Screen"""
  pygame.init()
  display_size = (300, 400)
  screen = pygame.display.set_mode(display_size)
  background = pygame.Surface(screen.get_size())
  color_white = (255, 255, 255)
  display_font = pygame.font.Font(None, 40)
  pygame.display.set_caption('RC Autonomous Drive Mode')
  text = display_font.render('Press P for Pause and R for Resume', 1, color_white)
  text_position = text.get_rect(centerx=display_size[0] / 2)
  background.blit(text, text_position)
  screen.blit(background, (0, 0))
  pygame.display.flip()

def Main():
  """
  model_file = '../tensorflow/car-model.pb'
  label_file = '../tensorflow/car-labels.pb'
  input_height = 96
  input_width = 96
  input_mean = 0
  input_std = 255
  input_layer = 'Placeholder'
  output_layer = 'final_result'

  graph = load_graph(model_file)
  input_name = 'import/' + input_layer
  output_name = 'import/' + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)
  # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
  # all interfaces)
  """
  server_socket = socket.socket()
  server_socket.bind(('192.168.0.193', 8090))
  server_socket.listen(0)

  # Accept a single connection and make a file-like object out of it
  connection = server_socket.accept()[0].makefile('rb')
  try:
    #pygame_init()
    while True:
      #change, resume, pause, stop = get_keys()
      #print(get_keys())
      #if stop:
      #  print('stop server')
      #  break
      start_time = current_mili_time()
      # Read the length of the image as a 32-bit unsigned int. If the
      # length is zero, quit the loop
      image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
      if not image_len:
        break
      # Construct a stream to hold the image data and read the image
      # data from the connection
      image_stream = io.BytesIO()
      image_stream.write(connection.read(image_len))
      # Rewind the stream, open it as an image with PIL and do some
      # processing on it
      image_stream.seek(0)
      image = Image.open(image_stream).convert('RGB')
      image.save(configuration.TMP_BUFFER_DIR + 'pi_image.jpg','JPEG')
      print('Image is %dx%d' % image.size)
      image.verify()
      print('Image is verified')
      command = 'Complete'
      server_socket.send(command.encode())
      """
      image.show()
      t = read_tensor_from_image_file(
        configuration.TMP_BUFFER_DIR + 'pi_image.jpg',
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)
      start_time = current_mili_time()  
      with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
      print('Calculation time: ', current_mili_time()-start_time, ' ms')
      results = np.squeeze(results)
      top_k = results.argsort()[-1:][::-1]
      labels = load_labels(label_file)
      for i in top_k:
        data = labels[i]
      connection.send(data.encode())
      """
      print('Calculation time: ', current_mili_time()-start_time, ' ms')            
    #pygame.quit()
  finally:
    connection.close()
    server_socket.close()

if __name__ == '__main__':
  Main()