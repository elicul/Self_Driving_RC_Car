import socket
import pygame
import pygame.font
import io
import configuration

UP = LEFT = DOWN = RIGHT = ACCELERATE = DECELERATE = False

def get_keys():
    """Returns a tuple of (UP, DOWN, LEFT, RIGHT, change, ACCELERATE,
    DECELERATE, stop) representing which keys are UP or DOWN and
    whether or not the key states changed.
    """
    change = False
    stop = False
    key_to_global_name = {
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',
        pygame.K_ESCAPE: 'QUIT',
        pygame.K_q: 'QUIT',
        pygame.K_w: 'ACCELERATE',
        pygame.K_s: 'DECELERATE'
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
    return (UP, DOWN, LEFT, RIGHT, change, ACCELERATE, DECELERATE, stop)

def setup_interactive_control():
    """Setup the Pygame Interactive Control Screen"""
    pygame.init()
    display_size = (375, 559)
    screen = pygame.display.set_mode(display_size)
    pygame.display.set_caption('RC Car Interactive Control')
    background_image = pygame.image.load("images/instructions/traning.jpg").convert()
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

def interactive_control(client_socket):
    """Runs the interactive control"""
    setup_interactive_control()
    clock = pygame.time.Clock()
    while True:
        up_key, down, left, right, change, accelerate, decelerate, stop = get_keys()
        if stop:
            command = 'stop'
            client_socket.send(command.encode())
            break
        if accelerate:
            command = 'accelerate'
            client_socket.send(command.encode())
        if decelerate:
            command = 'decelerate'
            client_socket.send(command.encode())
        if change:
            command = 'idle'
            if up_key:
                command = 'up'
            elif down:
                command = 'down'
            append = lambda x: command + '_' + x if command != 'idle' else x
            if left:
                command = append('left')
            elif right:
                command = append('right')
            client_socket.send(command.encode())
            data = client_socket.recv(1024).decode()
            print ('Received from server: ' + data)
        clock.tick(30)
    pygame.quit()

def Main():
    try:
        client_socket = socket.socket()
        client_socket.connect(configuration.PI_HOST_PORT)
        interactive_control(client_socket)
    
    finally:        
        client_socket.close()
 
if __name__ == '__main__':
    Main()