
## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
import threading
from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024);
        cur_thread = threading.current_thread();
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999;

    my_server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler);
    ip, port = my_server.server_address;

    server_thread = threading.Thread(target=my_server.serve_forever());
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True;
    server_thread.start();
    print "Sever is running\n";



