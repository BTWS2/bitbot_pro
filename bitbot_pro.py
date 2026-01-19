# Mini MicroPython module for 4tronix BitBot PRO robot
# https://4tronix.co.uk/bitbotpro/
# Based on https://github.com/4tronix/BitBot/blob/master/bitbot.ts
# Proof of concept for robot

from microbit import i2c, sleep
import sys
from utime import ticks_us, sleep_us

# I2C address of the ATmega microcontroller on the BitBot Pro
I2C_ATMEGA_ADDR = 0x22

# Command codes
DRIVEDIST = 24  # Drive a specific distance
SPINANGLE = 25  # Spin a certain angle
ACKNAK = 20  # Register to read for acknowledgment
I2C_ACK = 0x55  # Acknowledgment byte from the microcontroller

# LED command codes
FIREBRT = 1  # Set LED brightness
FIREUPDT = 2  # Update LEDs
SETPIXEL = 13  # Set pixels

NUM_LEDS = 12  # Number of LEDs
MODE_AUTO = 1  # Only support for auto mode

# Global variables
_speed = 60  # Default speed percentage (0-100)



def clamp(value, min_value, max_value):
    # type: (float|int, float|int, float|int) -> float|int
    """Clamps a value between a minimum and maximum value."""

    return max(min_value, min(value, max_value))


def speed(new_speed=None):
    # type: (float|int|None|str) -> float|int|None
    """Set the global speed for the robot."""

    global _speed
    speeds = {"fast": 10, "normal": 6, "slow": 3, "slowest": 1}
    if new_speed is None:
        return _speed
    if new_speed in speeds:
        new_speed = speeds[new_speed]
    _speed = clamp(abs(int(round(new_speed * 10))), 0, 100)


def send_command(command, params):
    # type: (int, list[int]) -> None
    """Sends a command with parameters to the robot via I2C."""

    # Prepare the data buffer
    data = bytearray([command] + [param & 0xFF for param in params])
    # Send the command to the microcontroller
    try:
        i2c.write(I2C_ATMEGA_ADDR, data)
    except OSError:
        print("The robot is not connected.")
        print("Please connect the robot.")
        sys.exit()


def wait_for_ack():
    # type: () -> None
    """Waits for an acknowledgment from the robot indicating the command is complete."""

    while True:
        try:
            # Write the ACKNAK register address
            i2c.write(I2C_ATMEGA_ADDR, bytearray([ACKNAK]))
            # Read two bytes
            response = i2c.read(I2C_ATMEGA_ADDR, 2)
            # Combine the two bytes to form the acknowledgment code
            ack = response[0] + (response[1] << 8)
            if ack == I2C_ACK:
                break
            sleep(10)
        except OSError:
            sleep(10)


def go_cm(speed, distance_cm):
    # type: (float|int, float|int) -> None
    """
    Moves the robot a specified distance in centimeters at a given speed.
    Parameters:
        speed (int): The speed at which the robot should move. Negative values indicate reverse direction.
        distance_cm (int or float): The distance in centimeters for the robot to travel. 
            - If the absolute value is less than 1, the function returns immediately and the robot does not move.
            - If distance_cm is negative, the robot moves in reverse.
    """

    # If int(distance_cm) == 0, robot moves indefinitely
    if abs(distance_cm) < 1:
        return
    
    # If distance is negative, reverse the speed
    if distance_cm < 0:
        speed = -speed

    # The bitbot expects a positive integer distance
    distance_cm = abs(int(distance_cm))

    # Divide distance_cm into low and high bytes for I2C transmission
    distance_low = distance_cm & 0xFF
    distance_high = (distance_cm >> 8) & 0xFF

    # Prepare the parameters as a list of bytes
    # This list is converted into a bytearray in send_command
    params = [speed, distance_low, distance_high]
    send_command(DRIVEDIST, params)

    # Wait for acknowledgment, indicating the command is executed
    wait_for_ack()


def forward(distance_cm):
    # type: (float|int) -> None
    """Move the robot forward a specified distance in cm."""

    go_cm(_speed, distance_cm)


def back(distance_cm):
    # type: (float|int) -> None
    """Move the robot backward a specified distance in cm."""

    go_cm(-_speed, distance_cm)


def spin_deg(speed, angle_deg):
    # type: (float|int, float|int) -> None
    """
    Spins the robot a specified angle in degrees at a given speed.

    Parameters:
        speed (int): The speed at which the robot should spin. Negative values indicate reverse direction
        angle_deg (int or float): The angle in degrees for the robot to spin.
            - If the absolute value is less than 1, the function returns immediately and the robot does not spin.
            - If angle_deg is negative, the robot spins in the opposite direction.
    """

    # If int(angle_deg) == 0, robot spins indefinitely
    if abs(angle_deg) < 1:
        return
    
    # If angle is negative, reverse the speed
    if angle_deg < 0:
        speed = -speed

    # The bitbot expects a positive integer angle
    angle_deg = abs(int(angle_deg))

    # Divide angle_deg into low and high bytes for I2C transmission
    angle_low = angle_deg & 0xFF
    angle_high = (angle_deg >> 8) & 0xFF

    # Prepare the parameters as a list of bytes
    # This list is converted into a bytearray in send_command
    params = [speed, angle_low, angle_high]
    send_command(SPINANGLE, params)

    # Wait for acknowledgment, indicating the command is executed
    wait_for_ack()


def left(angle_deg):
    # type: (float|int) -> None
    """Spin the robot left a specified angle in degrees."""

    spin_deg(_speed, angle_deg)


def right(angle_deg):
    # type: (float|int) -> None
    """Spin the robot right a specified angle in degrees."""

    spin_deg(-_speed, angle_deg)


def set_led_color(r, g, b):
    # type: (int, int, int) -> None
    """Sets all LEDs to a given color.
    
    Parameters:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
    """

    # Special case in set_pixel_color: if led_id == NUM_LEDS, all LEDs are set
    set_pixel_color(NUM_LEDS, r, g, b)


def set_pixel_color(led_id, r, g, b):
    # type: (int, int, int, int) -> None
    """Sets a single LED to a given color.
    
    Parameters:
        led_id (int): LED index (0 to NUM_LEDS-1).
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
    """

    led_id = clamp(int(led_id), 0, NUM_LEDS)
    r = clamp(int(r), 0, 255)
    g = clamp(int(g), 0, 255)
    b = clamp(int(b), 0, 255)
    params = [MODE_AUTO, led_id, r, g, b]
    send_command(SETPIXEL, params)


def set_led_brightness(brightness):
    # type: (int) -> None
    """Sets the brightness of the LEDs.
    
    Parameters:
        brightness (int): Brightness level (0-255)
    """

    brightness = clamp(int(brightness), 0, 255)
    send_command(FIREBRT, [brightness])


def led_clear():
    # type: () -> None
    """Clear all leds."""
    
    params = [MODE_AUTO, NUM_LEDS, 0, 0, 0]
    send_command(SETPIXEL, params)


def get_distance_cm(pin):
    # type: (microbit.pin) -> int
    """
    Get a distance reading in centimeters from an ultrasonic sensor, 
    connected to the specified pin.

    Parameters:
        pin (microbit.pin): The microbit.pin object to which the sensor is connected.

    Returns:
        int: Distance in centimeters.
    """

    # --- 1. Trigger the Sensor ---
    # Send a 10-microsecond HIGH pulse to the sensor to tell it to ping
    pin.write_digital(1)
    sleep_us(10)
    pin.write_digital(0)
    
    # Set pin to floating mode to prepare for the incoming echo signal
    pin.set_pull(pin.NO_PULL)

    # --- 2. Measure the Echo Pulse ---
    # Wait for the pin to go HIGH (this marks the start of the echo)
    while pin.read_digital() == 0:
        pass
    start = ticks_us() 

    # Wait for the pin to go LOW (this marks the end of the echo)
    while pin.read_digital() == 1:
        pass
    end = ticks_us()

    # --- 3. Calculate Distance ---
    # Calculate how long the pulse lasted (in microseconds)
    echo = end - start
    
    # Distance calculation explanation:
    # Speed of sound is ~343 m/s or 0.0343 cm/us.
    # We divide by 2 because the sound travels to the object AND back.
    # 0.0343 / 2 = 0.01715
    distance = int(0.01715 * echo)
    
    return distance


def set_servo_angle(pin, angle):
    # type: (microbit.pin, float|int) -> None
    """
    Set the angle of a servo motor connected to the specified pin.

    Parameters:
        pin (microbit.pin): The microbit.pin object to which the servo is connected.
        angle (float|int): The desired angle (0-180 degrees).
    """

    # Ensure the angle is within the valid range
    angle = clamp(angle, 0, 180)

    # Map the angle to a duty cycle between 0.5 ms (0°) and 2.5 ms (180°)
    # Corresponding to analog write values between 26 and 128
    duty_cycle_min = 26  # 0.5 ms / 20 ms * 1023
    duty_cycle_max = 128  # 2.5 ms / 20 ms * 1023
    duty_cycle = int(duty_cycle_min + (angle / 180) * (duty_cycle_max - duty_cycle_min))

    # Write the PWM signal to the servo
    pin.set_analog_period(20)
    pin.write_analog(duty_cycle)

# Alias for compatibility with the turtle module
fd = forward
bk = back
backward = back
rt = right
lt = left
# position = pos
# setpos = goto
# setposition = goto
# seth = setheading