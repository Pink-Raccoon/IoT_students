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


    File:          Actuator.py
    

    Purpose:       Base class for all the
                   actuators that are going
                   to be attached to the
                   device ("thing").

                   To observe the state
                   of an actuator value, 
                   an actuator IS A 
                   observable resource.
                   
                   Class is based on
                   observable resource
                   of the aiocoap package.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.

                   - Some functions are just
                     abstract in this base
                     class and have to be
                     overridden in the derived
                     class.

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

import grovepi
import aiocoap.resource as resource

class Actuator( resource.ObservableResource ):

  def __init__( self, connector, logger, nuances_resolution = int( 2 ) ):
    super( Actuator, self ).__init__()
    self.connector = connector
    self.logger = logger
    self.nuances_resolution = nuances_resolution
    grovepi.pinMode( connector, "OUTPUT" )

  
  # Function has to be overridden in derived class.
  def __enter__( self ):
    pass

  
  # Function has to be overridden in derived class.
  def __exit__( self, exc_type, exc_value, traceback ):
    pass

  
  # Function has to be overridden in derived class.
  def set_actuator( self, value ):
    pass

  
  # Function has to be overridden in derived class.
  def input_valid( self, input ):
    pass
		
  
  # Function has to be overridden in derived class.
  def is_equal( self, a, b ):
    pass


