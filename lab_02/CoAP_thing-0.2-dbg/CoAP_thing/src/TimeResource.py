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


    File:          TimeResource.py
    

    Purpose:       Derived class from the
                   observable resource class
                   of the aiocoap package.
                   
                   This resource's pupose
                   is to get the operating
                   system's time and provide
                   it under a coap uri.
                   The refresh interval of
                   the resource is currently
                   set to 60 seconds.
                   
    
    Remarks:       - python3 is required due
                     to the asyncio and aiocoap
                     libraries.
                     The aiocoap library makes
                     use of coroutines.


    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          09/2016

'''

import asyncio


import asyncio

import aiocoap
import aiocoap.resource as resource

import datetime


class TimeResource( resource.ObservableResource ):
    
  """
  Example resource that can be observed. The `notify` method keeps scheduling
  itself, and calles `update_state` to trigger sending notifications.
  """
    
  def __init__( self, logger ):
    super( TimeResource, self ).__init__()
    
    self.logger = logger

    self.notify()
  
  
  def __enter__( self ):
    pass


  def __exit__( self, exc_type, exc_value, traceback ):
    pass


  def notify( self ):
    self.updated_state()
    asyncio.get_event_loop().call_later( float( 60.0 ), self.notify )


  @asyncio.coroutine
  def render_get( self, request ):
    payload = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M" ).encode( 'ascii' )
    return aiocoap.Message( code = aiocoap.CONTENT, payload = payload )

