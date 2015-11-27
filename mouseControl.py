#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'davinellulinvega'

import pyautogui
from sphero_driver import sphero_driver
from math import atan


# Get the screen size
screen_w, screen_h = pyautogui.size()
half_w = float(screen_w / 2)
half_h = float(screen_h / 2)
# Initialize the position of the mouse
x, y = pyautogui.position()
x = float(x)
y = float(y)


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
            speed = (abs(x - half_w) / half_w) * 255
            # Compute the heading
            heading = atan(y/x)
            # Make sure the heading is between 0 and 359
            heading %= 360

            # Ask the robot to roll
            sphero.roll(int(speed), int(heading), 0x01, False)

            # Get the new mouse position
            x, y = pyautogui.position()
            x = float(x)
            y = float(y)

    except KeyboardInterrupt:
        # Ask the robot to stop rolling
        sphero.roll(0x00, 0x00, 0x00, False)
        # Turn the tail light off
        sphero.set_back_led(0x00, False)
        # Disconnect from the robot
        sphero.disconnect()
        # Print a little message
        print("Goodbye all you people !!!")
