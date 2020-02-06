#!/usr/bin/env python3
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
import sys

port = int(sys.argv[1])
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(port, GPIO.OUT, initial=False)   # Set pin port to be an output pin and set initial value to low (off)

try:
    while True: # Run forever
       GPIO.output(port, True) # Turn on
       sleep(1)                  # Sleep for 1 second
       GPIO.output(port, False)  # Turn off
       sleep(1)                  # Sleep for 1 second
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
