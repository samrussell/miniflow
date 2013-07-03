#!/usr/bin/python

# Written by Sam Russell in July 2013
# MiniFlow - a minimal OpenFlow controller
# Because networking is hard

import socket
import thread
import struct

def ProcessOpenFlowMessage(header, length, payload):
    # make this return a dict, with a field for what to send out to what switch
    pass


def OpenFlowHeader(data):
    if(len(data) >=8):
        return struct.unpack("!BBHL", data)
    return None


def GetOpenFlowMessage(clientsocket):
    data = clientsocket.recv(8) # openflow standard says every message starts with 8-byte header
    header = OpenFlowHeader(data)
    # do a test for header == None and fail?
    (version, ofpt_type, length, xid) = header
    print "Version %d, type %d, length %d, xid %d" % (version, ofpt_type, length, xid)
    # read rest of header
    payload = clientsocket.recv(length-8)
    ProcessOpenFlowMessage(header, length, payload)


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