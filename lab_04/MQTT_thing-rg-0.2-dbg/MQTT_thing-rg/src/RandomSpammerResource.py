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


    File:          RandomSpammerResource.py
    

    Purpose:       Derived class from the
                   python internal thread class.
                   
                   This resource's pupose
                   is to generate random data
                   and publish it under 
                   a MQTT topic.
                   The querying time interval of
                   the resource is currently
                   set to a random generated 
                   number.
                   
    
    Remarks:       - 


    Author:        P. Leibundgut <leiu@zhaw.ch>
    
    
    Date:          10/2016

'''

import threading
import time
import json

from random import randint

import log
import mqttconfig
import tools


MIN_SLEEP_TIME = int( 1 ) # unit is seconds
MAX_SLEEP_TIME = int( 6 ) # unit is seconds

MIN_SENSOR_VALUE = int(    0 )
MAX_SENSOR_VALUE = int( 1023 )


ALIVE_CHECK_INTERVAL_IN_MILLIS = int( 100 )
ALIVE_CHECK_INTERVAL_IN_S = float( ALIVE_CHECK_INTERVAL_IN_MILLIS / 1000 )


# logging setup
logger = log.setup_custom_logger( "mqtt_thing_random_spammer_resource" )


class RandomSpammerResource( threading.Thread ):
    
  def __init__( self, lock, \
                mqtt_client, \
                running, \
                pub_topic, \
                client_id ):
    
    # must be called ...
    threading.Thread.__init__( self )
       
    self.lock = lock
    self.mqtt_client = mqtt_client
    self.running = running
    self.pub_topic = pub_topic
    self.client_id = client_id


  def query_system_time( self ):
    keep_querying = bool( False )
    pub_interval_in_millis = int( 0 )
    possible_units = [ "K", "C", "F" ]

    unit                 = str( "" )
    value                = str( "" )
    current_pub_interval = float( 0.0 )

    sleep_periods = int( 0 )

    timestamp = str( "" )

    self.lock.acquire()
    keep_querying = self.running
    self.lock.release()

    while keep_querying:
      # create a little bit of random data ...
      unit                 = possible_units[ randint( int( 0 ), len( possible_units ) - 1 ) ]
      value                = str( randint( MIN_SENSOR_VALUE, MAX_SENSOR_VALUE ) )
      current_pub_interval = float( randint( MIN_SLEEP_TIME, MAX_SLEEP_TIME ) )

      pub_interval_in_millis = int( current_pub_interval * 1000 )
      sleep_periods = int( pub_interval_in_millis // ALIVE_CHECK_INTERVAL_IN_MILLIS )
      timestamp = str( int( round( time.time() * 1000 ) ) )

      payload = str( self.create_senml_json_string( value, unit, timestamp ) )
      self.mqtt_client.publish( self.pub_topic, str( payload ), \
                                mqttconfig.QUALITY_OF_SERVICE, False )

      for _ in range( 0, sleep_periods ):
        time.sleep( ALIVE_CHECK_INTERVAL_IN_S )
        self.lock.acquire()
        keep_querying = self.running
        self.lock.release()
        if not keep_querying:
          break


  def run( self ):
    self.query_system_time()


  def create_senml_json_string( self, value, unit, timestamp ):
  
    '''
    Mapping Python/JSON "Types"
    
    JSON              Python
    ============================
    object            dict
    array             list
    string            str
    number (int)      int
    number (real)     float
    true              True
    false             False
    null              None
    '''
    
    random_data = { }
    sensor_list = [ ]
    measurement = { }
    
    random_data[ 'sv' ] = value
    random_data[ 't' ]  = timestamp
    random_data[ 'u' ]  = unit
    random_data[ 'n' ]  = self.pub_topic

    sensor_list.append( random_data )

    measurement[ 'e' ]  = sensor_list
    measurement[ 'bn' ] = self.client_id 

    return json.dumps( measurement, sort_keys = False )

