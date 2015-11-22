#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'davinellulinvega'

from sphero_driver import sphero_driver
import pyautogui


# Create an instance of the sphero class
sphero = sphero_driver.Sphero(target_addr="68:86:E7:06:30:CB")
