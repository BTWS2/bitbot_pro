from microbit import pin1, sleep
import bitbot_pro as turtle

# Example usage: Sweep the servo from 0° to 180° and back
while True:
    for angle in range(0, 181, 10):
        print(angle)
        turtle.set_servo_angle(pin1, angle)
        sleep(500)
    for angle in range(180, -1, -10):
        print(angle)
        turtle.set_servo_angle(pin1, angle)
        sleep(500)
