#!/usr/bin/python

# Written by Sam Russell in July 2013
# MiniFlow - a minimal OpenFlow controller
# Because networking is hard

import socket
import thread

def OpenFlowServer(clientsocket, address):
    ipaddress = address[0]
    port = address[1]
    print "Got connection from %s:%d" % (ipaddress, port)


def Listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("0.0.0.0", 6633))
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