#!/usr/bin/env python3

'''
                    ___           ___           ___
        ___        /\__\         /\  \         /\  \
       /\  \      /::|  |       /::\  \       /::\  \
       \:\  \    /:|:|  |      /:/\:\  \     /:/\ \  \
       /::\__\  /:/|:|  |__   /::\~\:\  \   _\:\~\ \  \
    __/:/\/__/ /:/ |:| /\__\ /:/\:\ \:\__\ /\ \:\ \ \__\
   /\/:/  /    \/__|:|/:/  / \:\~\:\ \/__/ \:\ \:\ \/__/
   \::/__/         |:/:/  /   \:\ \:\__\    \:\ \:\__\
    \:\__\         |::/  /     \:\ \/__/     \:\/:/  /
     \/__/         /:/  /       \:\__\        \::/  /
                   \/__/         \/__/         \/__/


    File:          toggle.py


    Purpose:       Trivial implementation
                   of a LED toggler on a
                   Raspberry Pi and a 
                   GrovePi board attached.


    Remarks:       - The grovepi module and all
                     its dependencies have to be
                     available on the system
                     this script has to be run.

                   - 2 LEDs connected to the
                     GrovePi board (pins see 
                     in globals section).

                   - 1 rotary angle sensor
                     connected to the GrovePi
                     board (pins see in 
                     globals section).

                   - Use the rotary angle sensor
                     (potentiometer) to adjust
                     the toggling interval of
                     the two LEDs.


    Author:        Your Name <--------@students.zhaw.ch>


    Date:          09/2016

'''

import math
import time

import grovepi

LED0_PIN = int( 3 )
LED1_PIN = int( 4 )

ROTARY_ANGLE_SENSOR_PIN = int( 0 )
ROTARY_ANGLE_SENSOR_RES = int( 1024 )

'''
maximum sleep time [ms] would be:
SLEEP_TIME_RESOLUTION * SLEEP_TIME_STEP_IN_MILLIS
'''
SLEEP_TIME_RESOLUTION      = int( 12 )
SLEEP_TIME_STEP_IN_MILLIS  = int( 200 )


# globals section
rotary_angle_sensor_raw = int( 0 )

grovepi.pinMode( ROTARY_ANGLE_SENSOR_PIN, "INPUT" )
grovepi.pinMode( LED0_PIN, "OUTPUT" )
grovepi.pinMode( LED1_PIN, "OUTPUT" )
time.sleep( float( 1.0 ) )


def read_rotary_angle_sensor():
  global rotary_angle_sensor_raw
  sleep_time = int( 0 ) 

  try:
    # ... read sensor here
    pass

  except IOError:
    print( "Error reading rotary angle sensor." )

  return sleep_time


def toggle_leds():

  # toggle the state of your leds here
  # and write the state to the digital pins
  pass


def main():

  while True:

    try:
      #read_rotary_angle_sensor()
      # This is the time delay of the minimum toggling interval
      time.sleep( 0.2 )

      # toggle the leds if time is up
      #toggle_leds()


    except KeyboardInterrupt:
      # set all output pins to low.
      grovepi.digitalWrite( LED0_PIN, int( 0 ) )
      grovepi.digitalWrite( LED1_PIN, int( 0 ) )
      print( "program was interrupted by key stroke. exiting ..." )
      break



if __name__ == "__main__":
    main()

