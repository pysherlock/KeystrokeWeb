
## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
import threading
import json
import MySQLdb
import os
from sklearn.externals import joblib
from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess
from profileUpdate import ProfileUpdate

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(4096);
        cur_thread = threading.current_thread();
        print cur_thread, " : ", data;

        try:
            json_rpc = json.loads(data);
            username, userID = json_rpc['username'], json_rpc['id'];
            officeID, Keystroke = json_rpc['officeID'], json_rpc['keystroke'];
            keystroke_threshold = json_rpc['keystroke_threshold'];
            keystroke_filePath = "../Dataset/New Users/" + username + ".pkl";

            Keystroke = json.loads(str(Keystroke).replace("\\", ""))['keystroke'];
            print type(Keystroke), Keystroke;
            for i in range(len(Keystroke)):
                Keystroke[i]['key'] = Keystroke[i]['key'].upper();
            print Keystroke;
            ## This part for keystroke json string is not enough reliable.
            ## We'd better to find a uniform way to deal with it

            ## Fuzzy Measure Part
            db = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
            cursor = db.cursor();
            sql = "SELECT * FROM users WHERE username = '%s'" %(username);
            try:
                cursor.execute(sql);
                results = cursor.fetchall();
                print results;
                for row in results:
                    signInTimes = row[3];
                    press = row[4];
                    closetab = row[5];
                    tabindex = row[6];
                    ## TODO: how to initialized factor variables, let the factors be consistent to the Database

                print "press=%d, closetab=%d, tabindex=%d" %(press, closetab, tabindex);

            except:
                print "Error: unable to fetch data";

            db.close();

            ## keystroke authentication
            if(os.path.isfile(keystroke_filePath)): ## check whether user's keystroke profile exists
                ## Read the model and keystroke_threshold from the DB
                Profile = dict({'model': joblib.load(keystroke_filePath), 'threshold': keystroke_threshold});
            else: ## Can't read keystroke model, train a new profile for this user
                Data_clp = DataProcess("../Dataset/New Users/" + username + "_clp.csv");
                Data_clp.process();

                ## For now, maybe user CMU dataset to make some fake imposters
                ## Cut the dimension coorespond to clp Data's dimension
                Imposter = CMUData.imposter[:, :, 0:len(Data_clp.data[0])];
                print Imposter.shape;
                print Data_clp.data.shape;
                model = Init_model(imposters=Imposter, train_data=Data_clp.data, index_user=userID);
                Profile = model.train_Model_GMM_LOOM();
                joblib.dump(Profile['model'], keystroke_filePath);
                keystroke_threshold = round(Profile['threshold'], 4);

                ## Connect DB to update the keystroke threshold
                db = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
                cur = db.cursor();
                # print cursor.fetchone();
                print username;
                sql = "UPDATE users SET `keystroke threshold`=%f WHERE `username`='%s'" \
                      %(keystroke_threshold, username)

                print sql;
                try:
                    print "Write to DB";
                    cur.execute(sql);
                    db.commit();
                except:
                    print "Exception";
                    db.rollback();
                finally:
                    db.close();

            auth = MakeAuth(mean=DataProcess.global_Mean, std = DataProcess.global_Std);
            result = auth.keystroke_Authentication(Profile=Profile, String=officeID, Keystroke=Keystroke);

            ## Update User's Profile, the update functionality of Progressive Password
            if(signInTimes >= 10 and str(result[0])=='True'):
                DB = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
                profileupdate = ProfileUpdate(username=username, logfile="../Dataset/Users Log/" + username + "_Log.csv",
                                              database=DB);
                profileupdate.Update();

            print "Send back: ", result;
            self.request.sendall(str(result[0]).encode('utf-8'));

        except (ValueError, KeyError) as e:
            print "Error: received message is not encoded in correct format: ", e.message;
            ##self.request.sendall("Error");
            self.request.sendall("False");

if __name__ == "__main__":
    print "Main procedure";
    HOST, PORT = "localhost", 19999;

    my_server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler);
    ip, port = my_server.server_address;

    ## Load universal dataset (Here means CMU dataset)
    CMUData = DataProcess("../Dataset/Kevin and Maxion/DSL-StrongPasswordData_new.csv");
    CMUData.processOnCMU();

    server_thread = threading.Thread(target=my_server.serve_forever());
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True;
    server_thread.start();
    print "Sever is running\n";

