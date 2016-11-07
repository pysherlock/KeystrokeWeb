import os
import json
import random
import numpy as np
import tornado.ioloop
import tornado.websocket
import tornado.options
import webbrowser

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int);

import argparse


import SocketServer

from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "Handle GET request";
        self.write("Hello, world");

class WebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True;

    def open(self, *args, **kwargs):
        print options.port;
        print "WebSocket opened";

    def on_message(self, message):
        print "Handle websocket request"
        print "Received message: ", message;

        try:
            json_rpc = json.loads(message);
            print "JSON: ", json_rpc;
            print type(json_rpc);
            username, password = json_rpc['Username']['username'], json_rpc['Password']['password'];
            Username_Keyevent, Password_Keyevent = json_rpc['Username']['keyevent'], json_rpc['Password']['keyevent'];
            print "Username: ", username, " Password: ", password;
            print Username_Keyevent, Password_Keyevent;

            result = auth.main_Authentication(username=username, password=password, Username_keyDict=Username_Keyevent,
                                     Password_keyDict=Password_Keyevent);
            print result;
            self.write_message(str(result));
        except ValueError:
            print "Error: received message is not encoded in json";

    # self.write_message("You said: " + message);

    def on_close(self):
        print "WebSocket closed"


if __name__ == "__main__":
    try:
        ## Pre-process CMU data
        CMUData = DataProcess("../Dataset/Kevin and Maxion/DSL-StrongPasswordData_new.csv");
        PYData = DataProcess("../Dataset/New Users/PUYang.csv");
        CMUData.processOnCMU();
        PYData.process();
        print "Data pre-process on CMU dataset is finished";

        ## Build profiles from CMU Data (and my own data)
        Profiles = dict();
        for index in range(45, 50):
            print index;
            ## For now, use 50 features to do the training
            train_data = CMUData.cross_valid(data=CMUData.data_user[index], fold=2, shuffle=True);
            train_index = [random.randrange(0, len(train_data), 3) for i in range(50)];
            train_data = np.array([train_data[j] for j in train_index]);
            model = Init_model(imposters=CMUData.imposter, train_data=train_data, index_user=index);
            Profiles['User'+str(index)] = {"Password": ".tie5roanl", "Keystroke": model.train_Model_GMM_LOOM()}; ## K_LOOM could be set manually

        model = Init_model(imposters=CMUData.imposter, train_data=PYData.data, index_user=1);
        Profiles['User'+str(1)] = {"Password": ".tie5roanl", "Keystroke": model.train_Model_GMM_LOOM()};

        ## Build authentication class
        auth = MakeAuth(Profiles=Profiles, mean=DataProcess.global_Mean, std=DataProcess.global_Std);
        print "Build authentication class completed";

    except IOError:
        print "Error: can't open ", os.path.dirname(__file__) + "Dataset/Kevin and Maxion/DSL-StrongPasswordData.csv";

    ## Set up tornado server, communicate with front-end by websockets
    tornado.options.parse_command_line();
    handlers = [(r"/", MainHandler), (r"/websocket", WebSocket)];
    server = tornado.web.Application(handlers);
    server.listen(options.port,address="localhost");

    # webbrowser.open("http://localhost:%d/" % options.port, new=2)
    print "Tornado server is running now";
    tornado.ioloop.IOLoop.current().start();

