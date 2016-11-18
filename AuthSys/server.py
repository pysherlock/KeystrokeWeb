
## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999;

    my_server = SocketServer.ThreadingTCPServer;



    print "Sever is running\n";

