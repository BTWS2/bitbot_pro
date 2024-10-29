from microbit import pin15, display, sleep
import bitbot_pro as turtle

while True:
    dist = turtle.get_distance_cm(pin15)
    display.scroll(dist)
    print(dist)
    sleep(1000)
