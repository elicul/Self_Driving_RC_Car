import socket
import pygame
import pygame.font
import io

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
    display_size = (300, 400)
    screen = pygame.display.set_mode(display_size)
    background = pygame.Surface(screen.get_size())
    color_white = (255, 255, 255)
    display_font = pygame.font.Font(None, 40)
    pygame.display.set_caption('RC Car Interactive Control')
    text = display_font.render('Use arrows to move', 1, color_white)
    text_position = text.get_rect(centerx=display_size[0] / 2)
    background.blit(text, text_position)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def interactive_control(mySocket):
    """Runs the interactive control"""
    setup_interactive_control()
    clock = pygame.time.Clock()
    while True:
        up_key, down, left, right, change, accelerate, decelerate, stop = get_keys()
        if stop:
            command = 'stop'
            mySocket.send(command.encode())
            break
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
            print(command)
            mySocket.send(command.encode())
            data = mySocket.recv(1024).decode()
            print ('Received from server: ' + data)
        clock.tick(30)
    pygame.quit()

def Main():
    host = '127.0.0.1'
    port = 5000
        
    mySocket = socket.socket()
    mySocket.connect((host,port))
        
    interactive_control(mySocket)
                
    mySocket.close()
 
if __name__ == '__main__':
    Main()