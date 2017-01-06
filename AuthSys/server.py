
## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
import threading
import json
import MySQLdb
import os
import csv
from sklearn.externals import joblib

from init_model import Init_model
from makeAuth import MakeAuth
from data_process import DataProcess
from profileUpdate import ProfileUpdate
from notificationMail import SendNotificationMail
from keystrokeExtract import collectKeystroke

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(4096);
        cur_thread = threading.current_thread();
        print cur_thread, " : ", data;
        result = False;

        try:
            ## Extract information from JSON
            json_rpc = json.loads(data);
            username, userID = json_rpc['username'], json_rpc['id'];
            ## other static factors
            press, closetab, tabindex = json_rpc['press'], json_rpc['closetab'], json_rpc['tabIndex'];
            signInTimes, email = -1, None;

            officeID, Keystroke = json_rpc['officeID'], json_rpc['keystroke'];
            keystroke_threshold = json_rpc['keystroke_threshold'];
            keystroke_filePath = "../Dataset/New Users/" + username + ".pkl";
            keystroke_logPath = "../Dataset/New Users/" + username + "_clp.csv";

            ## Delete the redundant '\' in keystroke's json
            Keystroke = json.loads(str(Keystroke).replace("\\", ""))['keystroke'];
            print type(Keystroke), Keystroke;
            for i in range(len(Keystroke)):
                Keystroke[i]['key'] = Keystroke[i]['key'].upper();
            print "Keystroke: ", Keystroke;

            ## TODO: Fuzzy Measure Authentication Part for Environmental Login Factors (Except for Keystroke)
            ## Now we begin with the naive way, only for the demostration
            user_score = 0.0;
            db = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
            cursor = db.cursor();
            sql = "SELECT * FROM users WHERE username = '%s'" %(username);
            try:
                cursor.execute(sql);
                results = cursor.fetchall();
                for row in results:
                    email = row[3];
                    signInTimes = row[4];
                    if press == row[5]:
                        user_score += 2.5;
                    if closetab == row[6]:
                        user_score += 2.5;
                    if tabindex == row[7]:
                        user_score += 2.5;

                    ## TODO: how to initialized factor variables, let the factors be consistent to the Database
                print "press=%d, closetab=%d, tabindex=%d" %(press, closetab, tabindex);

            except:
                print "Error: unable to fetch data";
            db.close();

            ## Keystroke Authentication (Machine Learning Part, Biometrics Authentication)
            Profile = None;
            if(os.path.isfile(keystroke_filePath)): ## check whether user's keystroke profile exists
                ## Read the model and keystroke_threshold from the DB
                Profile = dict({'model': joblib.load(keystroke_filePath), 'threshold': keystroke_threshold});
            else:
                ## User doesn't have a keystroke profile now.
                ## Read user's keystroke log, if it has enough data, we train a new profile for this user
                Data_clp = DataProcess(keystroke_logPath);
                Data_clp.process();
                print "User Data: ", Data_clp.data.shape;

                if(len(Data_clp.data) >= 50):
                    ## If user's log file has more than 50 items keystroke data
                    ## We train a keystroke profile for this user
                    ## For now, we use the keystroke dataset from CMU to make some fake imposters
                    ## Cut the dimension coorespond to clp Data's dimension
                    Imposter = CMUData.imposter[:, :, 0:len(Data_clp.data[0])];
                    print "Imposter: ", Imposter.shape;

                    model = Init_model(imposters=Imposter, train_data=Data_clp.data, index_user=userID);
                    Profile = model.train_Model_GMM_LOOM();
                    joblib.dump(Profile['model'], keystroke_filePath);
                    keystroke_threshold = round(Profile['threshold'], 4);

                    ## Connect DB to update the keystroke threshold
                    db = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
                    cur = db.cursor();
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

                    ## Notification Mail when keystroke is ready
                    SendNotificationMail(email, 1)

            ## keystroke is available for authentication
            if Profile is not None:
                auth = MakeAuth(mean=DataProcess.global_Mean, std = DataProcess.global_Std);
                keystroke_result = auth.keystroke_Authentication(Profile=Profile, String=officeID, Keystroke=Keystroke);
                print "Keystroke result: ", keystroke_result

                if str(keystroke_result[0]) == 'True':
                    user_score += 5.0;

                if user_score >= 7.5: ## keystroke and one of three factors are correct
                    result = True;
            else:
                if user_score >= 7.5: ## three factors are correct
                    result = True;

            ## Update User's Profile, the functionality of Progressive Password
            ## And send the notification email
            if(result):
                ## Record keystroke into user's keystroke log when authentication succeeds
                with open(keystroke_logPath, 'ab') as csvfile:
                    spamwriter = csv.writer(csvfile);
                    spamwriter.writerow(collectKeystroke(String=officeID, Keystroke=Keystroke));
                    print "Collect keystroke to user's log file"

                if(signInTimes >= 10):
                    # self.sendNotificationMail("pu.leo.yang@gmail.com", "pu.leo.yang@gmail.com", server='smtp.gmail.com');
                    SendNotificationMail(email).run();

                    DB = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
                    profileupdate = ProfileUpdate(username=username,
                                                  logfile="../Dataset/Users Log/" + username + "_Log.csv",
                                                  database=DB);
                    profileupdate.Update();

            ## Send back the authentication result
            print "Send back: ", result;
            self.request.sendall(str(result).encode('utf-8'));

        except (ValueError, KeyError) as e:
            print "Error: received message is not encoded in correct format: ", e.message;
            print "Send back: ", "False";
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
