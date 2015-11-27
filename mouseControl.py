#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'davinellulinvega'

import pyautogui
from sphero_driver import sphero_driver
from math import atan2
from math import sqrt
from math import pi


# Get the screen size
screen_w, screen_h = pyautogui.size()
half_w = float(screen_w / 2)
half_h = float(screen_h / 2)

# Initialize the position of the mouse
x, y = pyautogui.position()
# Avoid a division by 0
if x == 0:
    x = 1

# Create a sphero object
sphero = sphero_driver.Sphero(target_addr="68:86:E7:06:30:CB")
# Connect to the robot
sphero.connect()

# If we were able to connect to the robot
if sphero.is_connected:
    # Set the heading to 0
    sphero.set_heading(0x00, False)
    # Set the stabilization
    sphero.set_stablization(True, False)
    # Set the heading to 0 for the moment
    sphero.roll(0x00, 0x00, 0x00, False)
    # Turn the tail light on
    sphero.set_back_led(0x255, False)

    # Initialize the variables
    speed = 0
    heading = 0

    # No comes the fun part were we just take the position of the mouse and try to make the robot roll in
    # the right direction
    try:
        while True:
            # Compute the speed. 255 being the max speed for the robot.
            length = sqrt((x**2 + y**2))
            speed = (length / half_h) * 255
            # The height of the screen being less than the width there are cases were the speed will be more than
            # the maximum allowed
            if speed > 255:
                speed = 255
            # Compute the heading
            heading = atan2(y, x) * (180/pi)
            if heading < 0:
                heading += 360
            # Make sure the heading is between 0 and 359
            heading %= 360

            # Ask the robot to roll
            sphero.roll(int(speed), int(heading), 0x01, False)

            # Get the new mouse position
            x, y = pyautogui.position()

            # Cast to float so that the atan gives us the real angle
            x = float(x) - half_w
            # Y as a - in front so that the coordinates are in the standard positions x toward right and y going up
            y = - (float(y) - half_h)
            # Avoid the division by zero
            if x == 0:
                x = 1

    except KeyboardInterrupt:
        # Ask the robot to stop rolling
        sphero.roll(0x00, 0x00, 0x00, False)
        # Turn the tail light off
        sphero.set_back_led(0x00, False)
        # Disconnect from the robot
        sphero.disconnect()
        # Print a little message
        print("Goodbye all you people !!!")
