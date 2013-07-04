#!/usr/bin/python

# Written by Sam Russell in July 2013
# MiniFlow - a minimal OpenFlow controller
# Because networking is hard

import socket
import thread
import struct

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

def OpenFlowHeaderUnpack(data):
    if(len(data) >=8):
        return struct.unpack("!BBHL", data)
    return None

def OpenFlowHeaderPack(version, ofpt_type, length, xid):
    if(length >=8):
        return struct.pack("!BBHL", version, ofpt_type, length, xid)
    return None

def ProcessOpenFlowHello(header, payload):
    return {"output" : None}

def ProcessOpenFlowError(header, payload):
    return {"output" : None}

def ProcessOpenFlowEchoRequest(header, payload):
    # just swap the message type and return
    (version, ofpt_type, length, xid) = OpenFlowHeaderUnpack(header)
    outheader = OpenFlowHeaderPack(version, ofp_type["OFPT_ECHO_REPLY"], length, xid)
    return {"output" : (outheader, payload)}

def ProcessOpenFlowEchoReply(header, payload):
    return {"output" : None}

ProcessOpenFlowMessageType = {
    ofp_type['OFPT_HELLO'] : ProcessOpenFlowHello,
    ofp_type['OFPT_ERROR'] : ProcessOpenFlowError,
    ofp_type['OFPT_ECHO_REQUEST'] : ProcessOpenFlowEchoRequest,
    ofp_type['OFPT_ECHO_REPLY'] : ProcessOpenFlowEchoReply,
}

def ProcessOpenFlowMessage(header, payload):
    # make this return a dict, with a field for what to send out to what switch
    (version, ofpt_type, length, xid) = OpenFlowHeaderUnpack(header)
    if ofpt_type in ProcessOpenFlowMessageType:
        return ProcessOpenFlowMessageType[ofpt_type](header, payload)
    return None

def GetOpenFlowMessage(clientsocket):
    header = clientsocket.recv(8) # openflow standard says every message starts with 8-byte header
    parsedheader = OpenFlowHeader(data)
    # do a test for header == None and fail?
    (version, ofpt_type, length, xid) = parsedheader
    print "Version %d, type %d, length %d, xid %d" % (version, ofpt_type, length, xid)
    # read rest of header
    payload = clientsocket.recv(length-8)
    ProcessOpenFlowMessage(header, payload)


def OpenFlowServer(clientsocket, address):
    ipaddress = address[0]
    port = address[1]
    print "Got connection from %s:%d" % (ipaddress, port)
    while 1:
        data = GetOpenFlowMessage(clientsocket)
        
    
    clientsocket.close()


def Listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("0.0.0.0", 6634))
    serversocket.listen(5)
    return serversocket


def main():
    
    serversocket = Listen()
    while 1:
        (clientsocket, address) = serversocket.accept()
        try:
            thread.start_new_thread(OpenFlowServer, (clientsocket, address))
        except:
            print "ERROR: Could not start new thread to serve (%s)" % address


if __name__ == '__main__':
  main()