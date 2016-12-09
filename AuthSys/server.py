
## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
import threading
import json
from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(4096);
        cur_thread = threading.current_thread();
        print cur_thread," : ", data;

        try:
            PYData_clp = DataProcess("../Dataset/New Users/PUYang_clp.csv");
            CMUData = DataProcess("../Dataset/Kevin and Maxion/DSL-StrongPasswordData_new.csv");

            CMUData.processOnCMU();
            PYData_clp.process();

            json_rpc = json.loads(data);
            userID, officeID, Keystroke = json_rpc['id'], json_rpc['officeID'], json_rpc['keystroke'];
            print json.loads(str(Keystroke).replace("\\", ""));
            Keystroke = json.loads(str(Keystroke).replace("\\", ""));
            print type(Keystroke), Keystroke;
            print Keystroke['keystroke'];
            ## This part for keystroke json string is not enough reliable.
            ## We'd better to find a general way to deal with it

            ## For now, maybe user CMU dataset to make some fake imposters
            ## Cut the dimension coorespond to clp Data's dimension
            Imposter = CMUData.imposter[:, :, 0:len(PYData_clp.data[0])];
            print Imposter.shape;
            print PYData_clp.data.shape;
            model = Init_model(imposters=Imposter, train_data=PYData_clp.data, index_user=userID);
            Profile = model.train_Model_GMM_LOOM();

            ## Profile = pickle.loads(Keystroke model path);


            auth = MakeAuth(mean=DataProcess.global_Mean, std = DataProcess.global_Std);
            result = auth.keystroke_Authentication(Profile=Profile, String=officeID, keystroke=Keystroke['keystroke']);

            print "Send back: ", result;
            self.request.sendall(str(result[0]).encode('utf-8'));

        except (ValueError, KeyError) as e:
            print "Error: received message is not encoded in correct format: ", e.message;
            self.request.sendall("Server Error");

if __name__ == "__main__":
    print "Main procedure";
    HOST, PORT = "localhost", 19999;

    my_server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler);
    ip, port = my_server.server_address;

    server_thread = threading.Thread(target=my_server.serve_forever());
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True;
    server_thread.start();
    print "Sever is running\n";

