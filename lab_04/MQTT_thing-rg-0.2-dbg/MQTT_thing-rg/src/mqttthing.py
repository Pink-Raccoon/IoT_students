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


    File:          mqttthing.py
    

    Purpose:       Exemplarily implementation
                   of a "thing" that uses
                   the MQTT protocol to
                   interact with other devices.
                   
                   This is the main file and
                   program entry point.

                   The pins of connected 
                   hardware to the GrovePi
                   board should be declared
                   here as well as the
                   topics (sensors and
                   actuators) this device/
                   "thing" should publish
                   or subscribe to.
                   
    
    Remarks:       - This application
                     uses the paho-mqtt-module.
                     Be sure it is installed
                     on the device you want
                     to run this application.

                   - A running MQTT broker
                     is required to provide
                     a working communitcation
                     of the MQTT protocol.

                   - Run this program as root/
                     sudoer if a permission 
                     issue occurs. The program 
                     wants to get access to 
                     system information like 
                     IP addresses.
    

    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          10/2016

'''

import sys
import signal
import threading

import log
from tools import get_ip_address_by_if_name
from tools import get_hw_address_by_if_name
import mqttconfig


from RandomSpammerResource import RandomSpammerResource


# connected hardware
NETWORK_INTERFACE = "eth0"

LOCAL_IP = get_ip_address_by_if_name( NETWORK_INTERFACE )

# globals

# logging setup
logger = log.setup_custom_logger( "mqtt_thing_main" )

lock = threading.Lock()
resources = { }
mqtt_client = mqttconfig.setup_mqtt_client( LOCAL_IP )


# signal handler to perform a proper shutdown of the application.
def signal_handler( *args ):
  logger.debug( "\n\n\n\n\n" + \
                "+--------------------------------------------------------------------+\n" + \
                "| Thing was interrupted by key stroke. Thats all, folks! Exiting ... |\n" + \
                "+--------------------------------------------------------------------+" )

  # stop the clock resource
  lock.acquire()
  ( resources[ 'random0' ] ).running = False
  lock.release()

  mqtt_client.loop_stop()
  mqtt_client.disconnect()


def main():

  signal.signal( signal.SIGINT, signal_handler )

  # add all resources to the application

  resources[ 'random0' ] = RandomSpammerResource( lock = lock, \
                                                  mqtt_client = mqtt_client, \
                                                  running = True, \
                                                  pub_topic = "iot/labs/04/randomspammer", \
                                                  client_id = get_hw_address_by_if_name( NETWORK_INTERFACE ) )


  # start random spammer resource
  ( resources[ 'random0' ] ).start()


  '''
  if not called here running threads
  are not affected by Ctrl + C
  because the main thread finishes
  here and its child threads
  become orphans ...
  '''
  signal.pause() 


if __name__ == "__main__": 
  main()

