#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'davinellulinvega'

from sphero_driver import sphero_driver
import pyautogui
from time import sleep

# Define the size of the screen
width, height = pyautogui.size()
half_width = width / 2
half_height = height / 2


# Define a function for processing collision detection
def on_collision(data):
    """
    Each time the robot detect a collision, triggers a click on the mouse
    :param data: a dictionary containing information on the collision (irrelevant in our case)
    :return: Nothing
    """

    # Simply click on the present location
    pyautogui.click()
    print("Just clicked")


# Define a function for processing IMU data
def on_imu(data):
    """
    Process the IMU data to move the mouse around the screen.
    :param data: a dictionary containing information from the IMU sensor
    :return: Nothing
    """

    # Declare some variables for ease of reading
    pitch = data['IMU_PITCH_FILTERED']  # Translate in a displacement on Y axis
    roll = data['IMU_ROLL_FILTERED']  # Translate in a displacement on X axis

    # Pitch and roll are in the range [-179, 180], thus dividing by 180 gives us a ratio applied to half the width or
    # height of the screen
    x = half_width + (half_width * (roll / 180))
    y = half_height + (half_height * (pitch / 180))

    # Move the mouse on the screen
    pyautogui.moveTo(x, y)


# Create an instance of the sphero class
sphero = sphero_driver.Sphero(target_addr="68:86:E7:06:30:CB")
# Connect to the robot
sphero.connect()

# Disable the stabilization
sphero.set_stablization(0x00, False)

# Set the data streaming
sphero.set_data_strm(400, 1,
                     sphero_driver.STRM_MASK1['IMU_PITCH_FILTERED'] | sphero_driver.STRM_MASK1['IMU_YAW_FILTERED'] |
                     sphero_driver.STRM_MASK1['IMU_ROLL_FILTERED'], 0, 0, False)

# Configure the collision detection
sphero.config_collision_detect(0x01, 0x0C, 0x00, 0x0C, 0x00, 10, False)

# Add the callbacks for processing imu and collision data/events
sphero.add_async_callback(sphero_driver.IDCODE['COLLISION'], on_collision)
sphero.add_async_callback(sphero_driver.IDCODE['DATA_STRM'], on_imu)

# Turn the back led on
sphero.set_back_led(0xff, False)

# Start the thread for data processing
sphero.start()

try:  # Encapsulate into a try catch to somehow be able to stop this infinite loop
    # Create an infinite loop to keep the program alive
    while True:
        # Yeah just sleep
        sleep(60)
except KeyboardInterrupt:
    print("The user asked us to stop")
    # Switch the back led off
    sphero.set_back_led(0x00, False)
    # Disconnect from the robot
    sphero.disconnect()
    # Wait for all threads to stop
    sphero.join()
    print("Goodbye all you people")
