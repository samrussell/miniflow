#!/usr/bin/python

# Written by Sam Russell in July 2013

import unittest
import sys
import os.path
from copy import copy
sys.path.append(os.path.dirname(__file__) + "/../..")

from miniflow import *
import struct
import Queue
import socket
import asyncore



class miniflow_test(unittest.TestCase):
    
    def createsocket(self, ip, port):
        return socket.create_connection((ip, port), 1)
    
    
    def test_dummyswitch(self):
        # start the server
        threadq = Queue.Queue()
        thread.start_new_thread(BackgroundServer, (threadq,))
        
        # make a client connection
        clientsocket = self.createsocket("localhost", 6633)
        
        # send hello
        hellomsg = struct.pack('!BBHL', 1, ofp_type['OFPT_HELLO'], 8, 0x12345677)
        clientsocket.sendall(hellomsg)
        
        # get reply hello
        clientsocket.settimeout(5.0)
        reply = clientsocket.recv(8000)
        expected = struct.pack('!BBHL', 1, ofp_type['OFPT_HELLO'], 8, 0x12345678)
        actual = reply
        self.assertEquals(expected, actual, "Testing messages: expected %(expected)s (but is %(actual)s)" % locals())
        
        # kill the server
        threadq.put("quit")
    
    
    
    def test_processopenflowmessage(self):
        #enum ofp_type {
        #    /* Immutable messages. */
        #    OFPT_HELLO, /* Symmetric message */
        #    OFPT_ERROR, /* Symmetric message */
        #    OFPT_ECHO_REQUEST, /* Symmetric message */
        #    OFPT_ECHO_REPLY, /* Symmetric message */
        #    OFPT_VENDOR, /* Symmetric message */
        #    /* Switch configuration messages. */
        #    OFPT_FEATURES_REQUEST, /* Controller/switch message */
        #    OFPT_FEATURES_REPLY, /* Controller/switch message */
        #    OFPT_GET_CONFIG_REQUEST, /* Controller/switch message */
        #    OFPT_GET_CONFIG_REPLY, /* Controller/switch message */
        #    OFPT_SET_CONFIG, /* Controller/switch message */
        #    /* Asynchronous messages. */
        #    OFPT_PACKET_IN, /* Async message */
        #    OFPT_FLOW_REMOVED, /* Async message */
        #    OFPT_PORT_STATUS, /* Async message */
        #    /* Controller command messages. */
        #    OFPT_PACKET_OUT, /* Controller/switch message */
        #    OFPT_FLOW_MOD, /* Controller/switch message */
        #    OFPT_PORT_MOD, /* Controller/switch message */
        #    /* Statistics messages. */
        #    OFPT_STATS_REQUEST, /* Controller/switch message */
        #    OFPT_STATS_REPLY, /* Controller/switch message */
        #    /* Barrier messages. */
        #    OFPT_BARRIER_REQUEST, /* Controller/switch message */
        #    OFPT_BARRIER_REPLY, /* Controller/switch message */
        #    /* Queue Configuration messages. */
        #    OFPT_QUEUE_GET_CONFIG_REQUEST, /* Controller/switch message */
        #    OFPT_QUEUE_GET_CONFIG_REPLY /* Controller/switch message */
        #};
        ofp_type = {
            'OFPT_HELLO' : 0,
            'OFPT_ERROR' : 1,
            'OFPT_ECHO_REQUEST' : 2,
            'OFPT_ECHO_REPLY' : 3,
            'OFPT_VENDOR' : 4,
            # /* Switch configuration messages. */
            'OFPT_FEATURES_REQUEST' : 5,
            'OFPT_FEATURES_REPLY' : 6,
            'OFPT_GET_CONFIG_REQUEST' : 7,
            'OFPT_GET_CONFIG_REPLY' : 8,
            'OFPT_SET_CONFIG' : 9,
            # /* Asynchronous messages. */
            'OFPT_PACKET_IN' : 10,
            'OFPT_FLOW_REMOVED' : 11,
            'OFPT_PORT_STATUS' : 12,
            # /* Controller command messages. */
            'OFPT_PACKET_OUT' : 13,
            'OFPT_FLOW_MOD' : 14,
            'OFPT_PORT_MOD' : 15,
            # /* Statistics messages. */
            'OFPT_STATS_REQUEST' : 16,
            'OFPT_STATS_REPLY' : 17,
            # /* Barrier messages. */
            'OFPT_BARRIER_REQUEST' : 18,
            'OFPT_BARRIER_REPLY' : 19,
            # /* Queue Configuration messages. */
            'OFPT_QUEUE_GET_CONFIG_REQUEST' : 20,
            'OFPT_QUEUE_GET_CONFIG_REPLY' : 21,
        }
        sampleoutputs = [
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_HELLO'], 8, 0x12345678), b""),
                {"output" : None}
            ), # no reply - we sent a HELLO when the connection started
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_ERROR'], 12, 0x12345678), b"\x00\x00\x00\x00"),
                {"output" : None}
            ), # we don't reply to ERROR but should accept it fine
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_ECHO_REQUEST'], 16, 0x12345678), b"\x12\x34\x56\x78\x9a\xbc\xde\xf0"),
                {"output" : (struct.pack('!BBHL', 1, ofp_type['OFPT_ECHO_REPLY'], 16, 0x12345678),  b"\x12\x34\x56\x78\x9a\xbc\xde\xf0")}
            ), # ECHO_REQUEST packets need a reply
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_ECHO_REPLY'], 16, 0x12345678), b"\x12\x34\x56\x78\x9a\xbc\xde\xf0"),
                {"output" : None}
            ), # ECHO_REPLY just needs to be accepted
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_FEATURES_REPLY'], 32, 0x12345678), b"\x00\x00\x00\x12\x34\x56\x78\x90\x00\x00\x00\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
                {"output" : None}
            ), # FEATURES_REPLY with nothing enabled - need a few of these (maybe time to split into individual tests?)
            (
                (struct.pack('!BBHL', 1, ofp_type['OFPT_FEATURES_REPLY'], 80, 0x12345678), b"\x00\x00\x00\x12\x34\x56\x78\x90\x00\x00\x00\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" # features header
                                                                                         + b"\x00\x01\x00\x00\x22\x23\x24\x25\x26123456789abcdef\x00\x00\x00\x00\x00\x00\x03\x00\x00" # ofp_phy_port
                                                                                         + b"\xbf\x00\x00\x00\xbf\x00\x00\x00\xbf\x00\x00\x00\xbf\x00\x00\x00" # features omg
                                                                                         ),
                {"output" : None}
            ), # FEATURES_REPLY with nothing enabled - need a few of these (maybe time to split into individual tests?)
        ]
            # make a set of tests that should throw exceptions?
            #(
            #    (struct.pack('!BBHL', 1, ofp_type['OFPT_FEATURES_REQUEST'], 16, 0x12345678), b"\x12\x34\x56\x78\x9a\xbc\xde\xf0"),
            #    {"output" : None}
            #), # 
        for one, two in sampleoutputs:
            actual = ProcessOpenFlowMessage(*one)
            expected = two # some function likely
            self.assertEquals(expected, actual, "Testing messages: expected %(expected)s (but is %(actual)s)" % locals())



if __name__ == '__main__':
  unittest.main()