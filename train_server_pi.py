import socket
import time
import io
import picamera
import configuration
import utils.motor_driver as motor_driver_helper
import utils.image as image_helper
import RPi.GPIO as GPIO

def Main():
    motor_driver_helper.set_gpio_pins()
    host = "192.168.0.187"
    port = 8080
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    with picamera.PiCamera() as camera:
        # Camera configuration
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
        # Motors
        pwm = motor_driver_helper.get_pwm_imstance()
        motor_driver_helper.start_pwm(pwm)
        command = 'idle'
        duty_cycle = configuration.INITIAL_PWM_DUTY_CYCLE
        
        while True:
            data = conn.recv(1024).decode()
            print ("Received: " + str(data))  
            
            if str(data) == 'stop':
                break
            if str(data) == 'accelerate':
                duty_cycle = duty_cycle + 2 if (duty_cycle + 2) <= 100 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                print("RC Speed: " + str(duty_cycle))
            if str(data) == 'decelerate':
                duty_cycle = duty_cycle - 2 if (duty_cycle - 2) >= 0 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                print("RC Speed: " + str(duty_cycle))
            if str(data) == 'idle':
                command = 'idle'
                motor_driver_helper.set_idle_mode()
            elif str(data) == 'up':
                command = 'up'
                motor_driver_helper.set_forward_mode()
            elif str(data) == 'down':
                command = 'down'
                motor_driver_helper.set_reverse_mode()
            elif str(data) == 'left':
                command = 'left'
                motor_driver_helper.set_left_mode()
            elif str(data) == 'right':
                command = 'right'
                motor_driver_helper.set_right_mode()
            elif str(data) == 'up_left':
                command = 'left'
                motor_driver_helper.set_forward_mode()                    
                motor_driver_helper.set_left_mode()
            elif str(data) == 'up_right':
                command = 'right'
                motor_driver_helper.set_forward_mode()                    
                motor_driver_helper.set_right_mode()
            elif str(data) == 'down_left':
                command = 'left'
                motor_driver_helper.set_reverse_mode()                    
                motor_driver_helper.set_left_mode()
            elif str(data) == 'down_right':
                command = 'right'
                motor_driver_helper.set_reverse_mode()                    
                motor_driver_helper.set_right_mode()
            print ("Sending: " + str(command))
            conn.send(data.encode())
            
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            image_helper.save_image_with_direction(stream, command)
            stream.flush()

        GPIO.cleanup()
             
    conn.close()
     
if __name__ == '__main__':
    Main()