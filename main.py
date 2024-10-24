import bitbot_pro as turtle
from time import sleep

# This is a test script for the bitbot_pro library

# Set global speed
print("Setting speed to 50%")
turtle.speed(50)

# Test moving forward
print("Moving forward 20 cm")
turtle.forward(20)
sleep(1)

# Test moving backward
print("Moving backward 20 cm")
turtle.backward(20)
sleep(1)

# Test spinning left
print("Spinning left 90 degrees")
turtle.left(90)
sleep(1)

# Test spinning right
print("Spinning right 90 degrees")
turtle.right(90)
sleep(1)

# Test setting LED brightness
print("Setting LED brightness to 128")
turtle.set_led_brightness(128)

# Test setting all LEDs to red
print("Setting all LEDs to red")
turtle.set_led_color(255, 0, 0)
sleep(1)

# Test setting all LEDs to green
print("Setting all LEDs to green")
turtle.set_led_color(0, 255, 0)
sleep(1)

# Test setting all LEDs to blue
print("Setting all LEDs to blue")
turtle.set_led_color(0, 0, 255)
sleep(1)

# Test setting individual LED colors
print("Setting individual LEDs to different colors")
for i in range(turtle.NUM_LEDS):
    if i % 2 == 0:
        turtle.set_pixel_color(i, 30, 100, 200)
    else:
        turtle.set_pixel_color(i, 255, 210, 0)
sleep(4)

# Test clearing LEDs
print("Clearing all LEDs")
turtle.led_clear()
