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

pyautogui.FAILSAFE = False


# Define a function for processing IMU data
def on_imu(data):
    """
    Process the IMU data to move the mouse around the screen.
    :param data: a dictionary containing information from the IMU sensor
    :return: Nothing
    """

    # Declare some variables for ease of reading
    pitch = float(data['IMU_PITCH_FILTERED'])  # Translate in a displacement on Y axis
    roll = float(data['IMU_ROLL_FILTERED'])  # Translate in a displacement on X axis

    x = 60 * (roll / 180)
    y = 60 * (pitch / 180)

    # Move the mouse on the screen
    pyautogui.scroll(x)
    pyautogui.hscroll(y)


# Create an instance of the sphero class
sphero = sphero_driver.Sphero(target_addr="68:86:E7:06:30:CB")
# Connect to the robot
sphero.connect()

# Disable the stabilization
sphero.set_stablization(0x00, False)

# Set the heading to 0
sphero.set_heading(0x00, False)
# Put the robot into the 0 position
sphero.roll(0x00, 0x00, 0x00, False)

# Set the data streaming
sphero.set_data_strm(200, 1,
                     sphero_driver.STRM_MASK1['IMU_PITCH_FILTERED'] | sphero_driver.STRM_MASK1['IMU_YAW_FILTERED'] |
                     sphero_driver.STRM_MASK1['IMU_ROLL_FILTERED'], 0, 0, False)

# Add the callbacks for processing imu and collision data/events
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
