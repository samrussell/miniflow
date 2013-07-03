#!/usr/bin/python

# Written by Sam Russell in July 2013

import unittest
import sys
import os.path
from copy import copy
sys.path.append(os.path.dirname(__file__) + "/../..")

from miniflow import *
import struct

class miniflow_test(unittest.TestCase):
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
        sampleoutputs = {
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
                {"output" : (struct.pack('!BBHL', 1, ofp_type['OFPT_ECHO_REPLY'], 16, 0x12345678), b"\x12\x34\x56\x78\x9a\xbc\xde\xf0")}
            ), # we don't reply to ERROR but should accept it fine
            
        }
        for one, two in sampleoutputs:
            expected = one
            actual = two # some function likely
            self.assertEquals(expected, actual, "Function(%(rrdfilename)s): expected %(expected)s (but is %(actual)s)" % locals())

