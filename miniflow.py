#!/usr/bin/python

# Written by Sam Russell in July 2013
# MiniFlow - a minimal OpenFlow controller
# Because networking is hard

import socket
import asyncore
import thread
import struct
import Queue
import sys

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

def ProcessOpenFlowFeaturesReply(header, payload):
    return {"output" : None}

ProcessOpenFlowMessageType = {
    ofp_type['OFPT_HELLO'] : ProcessOpenFlowHello,
    ofp_type['OFPT_ERROR'] : ProcessOpenFlowError,
    ofp_type['OFPT_ECHO_REQUEST'] : ProcessOpenFlowEchoRequest,
    ofp_type['OFPT_ECHO_REPLY'] : ProcessOpenFlowEchoReply,
    ofp_type['OFPT_FEATURES_REPLY'] : ProcessOpenFlowFeaturesReply,
}

def ProcessOpenFlowMessage(header, payload):
    # make this return a dict, with a field for what to send out to what switch
    (version, ofpt_type, length, xid) = OpenFlowHeaderUnpack(header)
    if ofpt_type in ProcessOpenFlowMessageType:
        return ProcessOpenFlowMessageType[ofpt_type](header, payload)
    return None

def OpenFlowHeader(data):
    if(len(data) >=8):
        return struct.unpack("!bbhl", data)
    return None


def GetOpenFlowMessage(clientsocket):
    header = clientsocket.recv(8) # openflow standard says every message starts with 8-byte header
    parsedheader = OpenFlowHeader(header)
    # do a test for header == None and fail?
    if parsedheader == None:
        return
    (version, ofpt_type, length, xid) = parsedheader
    print "Version %d, type %d, length %d, xid %d" % (version, ofpt_type, length, xid)
    # read rest of header
    print "Header size: %d, length: %d, rest: %d" % (8, length, length-8)
    if length > 8:
        payload = clientsocket.recv(length-8)
    else:
        payload = b""
    ProcessOpenFlowMessage(header, payload)


class OpenFlowThread(asyncore.dispatcher_with_send):
    
    def __init__(self, sock, address):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.address = address
        # start off by sending a hello message
        self.send(struct.pack('!BBHL', 1, ofp_type['OFPT_HELLO'], 8, 0x12345678))
    
    def handle_read(self):
        GetOpenFlowMessage(self)


class OpenFlowServer(asyncore.dispatcher):
    #code
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            print "New connection from %s" % repr(address)
            handler = OpenFlowThread(sock, address)
    

def BackgroundServer(threadq = None):
    server = OpenFlowServer("0.0.0.0", 6633)
    while 1:
        if threadq:
            try:
                message = threadq.get_nowait()
                # if we get here then something is kicking us out
                return
            except:
                pass
        asyncore.loop(timeout = 1)


def main():
    threadq = Queue.Queue()
    thread.start_new_thread(BackgroundServer, (threadq,))
    while 1:
        line = sys.stdin.readline()
        if(line.startswith("quit")):
            threadq.put(line)
            return
    


if __name__ == '__main__':
  main()