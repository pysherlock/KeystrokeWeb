
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
        print cur_thread, " Received : ", data;
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

            try:
                ## Delete the redundant '\' in keystroke's json
                Keystroke = json.loads(str(Keystroke).replace("\\", ""))['keystroke'];
                # print type(Keystroke), Keystroke;
                for i in range(len(Keystroke)):
                    Keystroke[i]['key'] = Keystroke[i]['key'].upper();
            except: ## User doesn't type in his keystroke
                Keystroke = None

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
                    print "User's data in the DB: ", row;
                    email = row[2];
                    signInTimes = row[4];
                    if press < (row[5]+800) and press > (row[5]-800):
                        user_score += 2.5;
                    if closetab == row[6]:
                        user_score += 2.5;
                    if tabindex == row[7]:
                        user_score += 2.5;

                    ## TODO: how to initialized factor variables, let the factors be consistent to the Database
                print "Environmental Factors: " \
                      "press=%d, closetab=%d, tabindex=%d, userscore=%d" %(press, closetab, tabindex, user_score);
            except:
                print "Error: unable to fetch data";
            db.close();

            ## Keystroke Authentication (Machine Learning Part, Biometrics Authentication)
            Profile = None;
            if(os.path.isfile(keystroke_filePath)): ## check whether user's keystroke profile exists
                ## Read the model and keystroke_threshold from the DB
                Profile = dict({'model': joblib.load(keystroke_filePath), 'threshold': keystroke_threshold});

            ## keystroke profile and keystroke typed are available for authentication
            ## Then do the keystroke authentication, otherwise not
            if Profile is not None and Keystroke is not None:
                print "\n***** Keystroke Authentication *****";
                auth = MakeAuth(mean=DataProcess.global_Mean, std = DataProcess.global_Std)
                keystroke_result = auth.keystroke_Authentication(Profile=Profile, String=officeID, Keystroke=Keystroke)
                print "Keystroke result: ", keystroke_result
                if str(keystroke_result[0]) == 'True':
                    user_score += 5.0

            ## According whether user score reaches the threshould, system gets the authentication result
            ## keystroke and one of three factors are correct or three other factors are true
            if user_score >= 7.5:
                result = True;

            ## Send back the authentication result
            print "Send back the authentication result: ", result;
            self.request.sendall(str(result).encode('utf-8'));

            ## Update User's Profile, the functionality of Progressive Password.
            ## Include update user's keystroke profile, and other Environmental Login factors.
            ## After updating, server would send a notification email to the user.
            if(result):
                ## Record keystroke into user's keystroke log when authentication is successful
                if(Keystroke is not None):
                    with open(keystroke_logPath, 'ab') as csvfile:
                        print "\n***** Collecting the Keystroke that user typed just now *****"
                        spamwriter = csv.writer(csvfile);
                        spamwriter.writerow(collectKeystroke(String=officeID, Keystroke=Keystroke));
                        print "Collect keystroke to user's log file"

                ## User doesn't have a keystroke profile.
                ## Read user's keystroke log, if it has enough data, we train a new profile for this user
                if(os.path.isfile(keystroke_logPath)):
                    Data_clp = DataProcess(keystroke_logPath);
                    Data_clp.process();
                    keystroke_amount = len(Data_clp.data);
                    print "User Keystroke Data: ", Data_clp.data.shape;

                    if (keystroke_amount%50 == 0 and keystroke_amount != 0):
                        ## TODO: If every time system has to check the keystroke log file
                        ## TODO: In order to make sure whether this user has enough data to build a profile,
                        ## TODO: It would be too expensive. We need a more efficient way, maybe store keystroke amount in DB

                        ## If user's keystroke log file has 50 items keystroke data first time
                        ## We train a keystroke profile for this user
                        ## If user's keystroke log file has multiple 50(100, 150, 200...) items keystroke data
                        ## System would update user's keystroke profile.
                        ## For now, we use the keystroke dataset from CMU to make some fake imposters
                        ## Cut the dimension coorespond to clp Data's dimension
                        print "\n***** Generating Keystroke Profile *****";
                        Imposter = CMUData.imposter[:, :, 0:len(Data_clp.data[0])]
                        print "Keystroke Imposter: ", Imposter.shape

                        model = Init_model(imposters=Imposter, train_data=Data_clp.data, index_user=userID)
                        Profile = model.train_Model_GMM_LOOM()
                        joblib.dump(Profile['model'], keystroke_filePath)
                        keystroke_threshold = round(Profile['threshold'], 4)

                        ## Connect DB to update the keystroke threshold
                        db = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306)
                        cur = db.cursor()
                        sql = "UPDATE users SET `keystroke threshold`=%f WHERE `username`='%s'" \
                              % (keystroke_threshold, username)

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

                        if keystroke_amount == 50:
                            ## Notification Mail when keystroke is ready
                            SendNotificationMail(email, 1).run();
                        else:
                            ## Notification Mail when keystroke profile is updated
                            SendNotificationMail(email, 2).run();

                if(signInTimes >= 10):
                    # self.sendNotificationMail("pu.leo.yang@gmail.com", "pu.leo.yang@gmail.com", server='smtp.gmail.com');
                    ## Notification Mail when environmental factors are updated
                    print "\n***** Updating User's Environmental Factors *****";
                    SendNotificationMail(email).run();

                    DB = MySQLdb.connect("localhost", "root", "ypu123123", "mydb1", port=3306);
                    profileupdate = ProfileUpdate(username=username,
                                                  logfile="../Dataset/Users Log/" + username + "_Log.csv",
                                                  database=DB);
                    profileupdate.Update();
            else:
                print "*****Environmental Login is failed. User's credential is not correct*****"
                ## Maybe there will be other operation in this part in the future

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
