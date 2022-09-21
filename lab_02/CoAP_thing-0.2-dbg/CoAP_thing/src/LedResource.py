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


    File:          LedResource.py
    

    Purpose:       Concrete implementation
                   class for a GrovePi
                   LED with digital output.

                   Class is based on
                   the abstract actuator
                   class.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - Actuators get notified
                     from sensors. Therefore
                     the input from the sensors
                     has to be parsed and verified,
                     according the needs
                     of the required parameters
                     between concrete sensors
                     and actuators.

                   - If the main program terminates
                     (Exception / Key stroke / ...)
                     an actuator has to be brought
                     into a save off state
                     e.g. all outputs to low, ...

                     Therefore the __exit__
                     function MUST be implemented
                     in each concrete actuator
                     implementation.
    

    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          09/2016

'''

import aiocoap
import aiocoap.resource as resource
import asyncio

import grovepi

from Actuator import Actuator

class LedResource( Actuator ):

  def __init__( self, connector, logger, nuances_resolution ):
    super( LedResource, self ).__init__( connector, logger, nuances_resolution )
		
    #set Contenttype to text/plain
    self.ct = 0
    self.value = False
		
    try:
      grovepi.analogWrite( self.connector, int( self.value ) )
    except IOError:
      self.logger.debug( "Error of initial digitalWrite call." )
 

  def __enter__( self ):
    pass
 

  def __exit__( self, exc_type, exc_value, traceback ):
    self.logger.debug( "tearing things down ..." )
    self.set_actuator( int( 0 ) )


  def set_actuator( self, value ):
    try:
      grovepi.digitalWrite( self.connector, int( value ) )
      self.updated_state()
    except IOError:
      self.logger.debug( "Error in writing to sensor at pin " + str( self.connector ) )  

		
		
  def str_to_bool( self, bool_as_str ):
    # Precondition: bool_as_str is either "True" or "False" nothing else
    return bool_as_str == "True"


  def is_equal( self, a, b ):
    return a == b


  def input_valid( self, input ):	
    return input in [ "True", "False" ]


  @asyncio.coroutine
  def render_get( self, request ):
    payload = ( str( self.value ) + "\n" ).encode( 'ascii' )
    response = aiocoap.Message( code = aiocoap.CONTENT, payload = payload )
    response.opt.content_format = self.ct
    return response


  @asyncio.coroutine
  def render_put( self, request ):
    payload = request.payload.decode( 'ascii', 'strict' )

    if self.input_valid( payload ):
      new_value = self.str_to_bool( payload )

      if not self.is_equal( new_value, self.value ):
        self.value = new_value
        self.set_actuator( new_value )
			
      response = aiocoap.Message( code = aiocoap.CHANGED, \
                 payload = "reqest payload was valid\n".encode( 'ascii' ) )

    else:
			
      response = aiocoap.Message( code = aiocoap.BAD_REQUEST, \
                 payload = "resource only supports True or False as payload\n".encode( 'ascii' ) )

    response.opt.content_format = self.ct
		
    return response

