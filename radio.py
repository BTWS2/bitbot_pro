from microbit import *
import radio


radio.config(group=42)  # Change group number to 1, 2, 3 or 4 as needed
radio.on()

master = False  # Change to True for master device

while True:
    if master:
        for i in range(10):
            message = str(i) + " from MicroBit"  # Change message as needed
            radio.send(message)
            print("sent: " + message)
            sleep(200)
        master = False
        radio.send("stop")
    else:
        while True:
            message = radio.receive()
            if not message:
                continue
            if message == "stop":
                master = True
                break
            print("received: " + message)
