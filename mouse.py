#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'davinellulinvega'

from sphero_driver import sphero_driver
import pyautogui
from time import sleep


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

# Define a function for processing gyro data
def on_gyro(data):
    """
    Process the gyroscopic data to move the mouse around the screen.
    :param data: a dictionary containing information from the gyro sensor
    :return: Nothing
    """

    # For the moment simply print a message
    print("Gyro X: {}".format(data['GYRO_X_RAW']))
    print("Gyro Y: {}".format(data['GYRO_Y_RAW']))

# Create an instance of the sphero class
sphero = sphero_driver.Sphero(target_addr="68:86:E7:06:30:CB")
# Connect to the robot
sphero.connect()

# Disable the stabilization
sphero.set_stablization(0x00, False)

# Set the data streaming
sphero.set_data_strm(15, 1, sphero_driver.STRM_MASK1['GYRO_X_RAW'] | sphero_driver.STRM_MASK1['GYRO_Y_RAW'], 0, 0, False)

# Configure the collision detection
sphero.config_collision_detect(0x01, (0xff / 8), 0x00, (0xff / 8), 0x00, 10, False)

# Add the callbacks for processing gyro and collision data/events
sphero.add_async_callback(sphero_driver.IDCODE['COLLISION'], on_collision)
sphero.add_async_callback(sphero_driver.IDCODE['DATA_STRM'], on_gyro)

# Start the thread for data processing
sphero.start()

try:  # Encapsulate into a try catch to somehow be able to stop this infinite loop
    # Create an infinite loop to keep the program alive
    while True:
        # Yeah just sleep
        sleep(60)
except KeyboardInterrupt:
    print("The user asked us to stop")
    sphero.disconnect()
    sphero.join()
    print("Goodbye all you people")

