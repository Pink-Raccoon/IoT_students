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


    File:          ButtonResource.py


    Purpose:       Derived class from the
                   sensor class that
                   implements the concrete
                   behaviour of a GrovePi
                   button.

                   Class is based on
                   the abstract sensor
                   class.


    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - the GrovePi module has
                     to be installed to 
                     interact with the GrovePi
                     hardware.

                   - A sensor can have atuators.
                     Those can be notified if
                     the state/value of a sensor
                     changes.

                     The idea is based on the
                     observer pattern.

                   - A sensor has a list of
                     actuator uris (coap://...)
                     wich are going
                     to be notified if the
                     state of a sensor value
                     changes.


    Author:        P. Leibundgut <leiu@zhaw.ch>


    Date:          08/2019

'''

import asyncio

import aiocoap
import aiocoap.resource as resource

import grovepi

from Sensor import Sensor

class ButtonResource( Sensor ):

  def __init__( self, connector, loop, logger, \
                polling_interval, sampling_resolution ):
    super( ButtonResource, self ).__init__( connector, loop, logger, \
                                            polling_interval, sampling_resolution )

    # set Contenttype to text/plain
    self.ct = int( 0 )
    self.value = False
    self.actuator_uris = [ "coap://localhost:5683/actuators/led0" ]

    self.poll_sensor()


  def __enter__( self ):
    pass


  def __exit__( self, exc_type, exc_value, traceback ):
    pass


  def read_sensor( self ):
    new_value = bool( False )

    try:
      new_value = bool( grovepi.digitalRead( self.connector ) )
    except IOError:
      self.logger.debug( "Error in reading sensor at pin " + str( self.connector ) )

    if not self.is_equal( self.value, new_value ):
      self.value = new_value
      self.notify_all_actuators()
      self.updated_state()
      self.logger.debug( "------------------read_sensor called in ButtonResource instance" )


  def is_equal( self, a, b ):
    return a == b


  @asyncio.coroutine
  def notify_actuator( self, act_uri ):
    payload = str( self.value ).encode( 'ascii' )
    yield from super( ButtonResource, self ).notify_actuator( act_uri, payload )

