## This server communicate with the java servlet
## Receive the factor information and send the verification result back

import SocketServer
import threading
import json
import MySQLdb
import os
import csv
from sklearn.externals import joblib

from makeAuth import MakeAuth
from data_process import DataProcess
from progressivePassword import ProgressivePassword

## setting of database
host_DB = "localhost"
username_DB = "root"
password_DB = "ypu123123"
name_DB = "mydb1"
port_DB = 3306

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(10240);
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
            keystroke_profile = "../Dataset/New Users/" + username + ".pkl";
            keystroke_logfile = "../Dataset/New Users/" + username + "_clp.csv";

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
            DB = MySQLdb.connect(host_DB, username_DB, password_DB, name_DB, port=port_DB);
            cursor = DB.cursor();
            sql = "SELECT * FROM users WHERE username = '%s'" %(username);
            try:
                cursor.execute(sql);
                results = cursor.fetchall();
                for row in results:
                    print "User's data in the DB: ", row;
                    email = row[3]
                    signInTimes = row[5]
                    threshold = row[34]
                    print "threshold: ", threshold
                    # if press < (row[5]+800) and press > (row[5]-800):
                    #     user_score += 2.5;
                    # if closetab == row[6]:
                    #     user_score += 2.5;
                    # if tabindex == row[7]:
                    #     user_score += 2.5;
                    user_score = self.FuzzyAuth(userinfo=json_rpc, dbinfo=row)

                    ## TODO: how to initialized factor variables, let the factors be consistent to the Database
                # print "Environmental Factors: " \
                #       "press=%d, closetab=%d, tabindex=%d, userscore=%d" %(press, closetab, tabIndex, user_score);
            except (ValueError, KeyError) as e:
                print "Error: unable to fetch data ", e.message;
            finally:
                DB.close();

            ## Keystroke Authentication (Machine Learning Part, Biometrics Authentication)
            Profile = None;
            if(os.path.isfile(keystroke_profile)): ## check whether user's keystroke profile exists
                ## Read the model and keystroke_threshold from the DB
                Profile = dict({'model': joblib.load(keystroke_profile), 'threshold': keystroke_threshold});

            ## keystroke profile and keystroke typed are available for authentication
            ## Then do the keystroke authentication, otherwise not
            if Profile is not None and Keystroke is not None:
                print "\n***** Keystroke Authentication *****";
                auth = MakeAuth(mean=DataProcess.global_Mean, std = DataProcess.global_Std)
                keystroke_result = auth.keystroke_Authentication(Profile=Profile, String=officeID, Keystroke=Keystroke)
                print "Keystroke result: ", keystroke_result
                if str(keystroke_result[0]) == 'True':
                    user_score += 8.0

            ## According whether user score reaches the threshould, system gets the authentication result
            ## keystroke and one of three factors are correct or three other factors are true
            print "User Score: ", user_score
            if user_score >= 12.0: ## TODO: replace it with threshold from database
             # if user_score >= threshold:
                result = True;
            ## Send back the authentication result
            print "Send back the authentication result: ", result;
            self.request.sendall(str(result).encode('utf-8'));

            ## Update User's Profile, the functionality of Progressive Password.
            ## Include update user's keystroke profile, and other Environmental Login factors.
            ## After updating, server would send a notification email to the user.
            if(result):
                ## Do the functionality of Progressive Password (updating profile) cost time
                ## We build a thread to take care of progressive password
                DB = MySQLdb.connect(host_DB, username_DB, password_DB, name_DB, port=port_DB);
                ProgressivePassword("ProgressivePassword", signInTimes,
                                    Keystroke, Keystroke_Imposter, keystroke_logfile, keystroke_profile,
                                    username, userID, officeID, email, DB).start();
            else:
                print "*****Environmental Login is failed. User's credential is not correct*****"
                ## Maybe there will be other operation in this part in the future

        except (ValueError, KeyError) as e:
            print "Error: received message is not encoded in correct format: ", e.message;
            print "Send back: ", "False";
            self.request.sendall("False");

    def FuzzyAuth(self, userinfo, dbinfo):
        score = 0; i = 9
        processor, memory, os, chrome, storage = userinfo['processor'], userinfo['memory'], userinfo['os'], userinfo['chrome'], userinfo['storage']
        locIP, pubIP, country, region, zip = userinfo['locIP'], userinfo['pubIP'], userinfo['country'], userinfo['region'], userinfo['zip']
        charge, removable, transition, priv, url = userinfo['charge'], userinfo['removable'], userinfo['transition'], userinfo['priv'], userinfo['url']
        width, height, zoom, click, detach = userinfo['width'], userinfo['height'], userinfo['zoom'], userinfo['click'], userinfo['detach']
        selected, lastCharacter, bookmarkChange, volumeChange = userinfo['selected'], userinfo['lastCharacter'], userinfo['bookmarkChange'], userinfo['volumeChange']
        volume, muted, paused, speedChange = userinfo['volume'], userinfo['muted'], userinfo['paused'], userinfo['speedChange']
        currentTime, ended, seek = userinfo['currentTime'], userinfo['ended'], userinfo['seek']
        press, closetab, tabIndex = userinfo['press'], userinfo['closetab'], userinfo['tabIndex']

        print "Score: ", score
        if dbinfo[i] is not None and dbinfo[i+1] is not None and dbinfo[i+2] is not None and dbinfo[i+3] is not None and dbinfo[i+4] is not None:
            if processor == dbinfo[i] and memory==dbinfo[i+1] and os==dbinfo[i+2] and chrome==dbinfo[i+3] and storage==dbinfo[i+4]:
                score += 3; print "hardware factor:3 "
        if dbinfo[i+5] is not None and dbinfo[i+6] is not None:
            if locIP == dbinfo[i+5] and pubIP==dbinfo[i+6]:
                score += 3; print "IP factor: 3"
        if dbinfo[i+7] is not None and dbinfo[i+8] is not None and dbinfo[i+9] is not None:
            if country==dbinfo[1+7] and region==dbinfo[i+8] and zip==dbinfo[i+9]:
                score += 3; print "Region factor: 3"
        if dbinfo[i+10] is not None:
            if charge == dbinfo[i+10]:
                score += 1; print "Charge factor: 1"
        if dbinfo[i+11] is not None:
            if tabIndex == dbinfo[i+11]:
                score += 4; print "tabIndex: 4"
        if dbinfo[i+12] is not None:
            if removable == dbinfo[i+12]:
                score += 1; print "Removable: 1"
        if dbinfo[i+13] is not None:
            if transition == dbinfo[i+13]:
                score += 2; print "Transition: 2"
        if dbinfo[i+14] is not None:
            if priv == dbinfo[i+14]:
                score += 1; print "Priv: 1"
        if dbinfo[i+15] is not None:
            if width == dbinfo[i+15]:
                score += 2; print "Width: 2"
        if dbinfo[i+16] is not None:
            if height == dbinfo[i+16]:
                score += 2; print "Height: 2"
        if dbinfo[i+17] is not None:
            if url == dbinfo[i+17]:
                score += 4; print "Url: 4"
        if dbinfo[i+18] is not None:
            if press <= dbinfo[i+18]+800 and press >= dbinfo[i+18]-800:
                score += 4; print "Press: 4"
        if dbinfo[i+19] is not None:
            if zoom == dbinfo[i+19]:
                score += 2; print "Zoom: 2"
        if dbinfo[i+20] is not None:
            if click == dbinfo[i+20]:
                score += 2; print "Click: 2"
        if dbinfo[i+21] is not None:
            if selected == dbinfo[i+21]:
                score += 2; print "Selected: 2"
        if dbinfo[i+22] is not None:
            if lastCharacter == dbinfo[i+22]:
                score += 2; print "lastCharacter: 2"
        if dbinfo[i+23] is not None:
            if detach == dbinfo[i+23]:
                score += 1; print "detach: 1"
        if dbinfo[i+24] is not None:
            if closetab == dbinfo[i+24]:
                score += 4; print "closetab: 4"
        if dbinfo[i+25] is not None:
            if bookmarkChange == dbinfo[i+25]:
                score += 1; print "bookmarkChange: 1"
        if dbinfo[i+26] is not None:
            if volumeChange == dbinfo[i+26]:
                score += 1; print "volumeChange: 1"
        if dbinfo[i+27] is not None:
            if volume == dbinfo[i+27]:
                score += 2; print "volume: 2"
        if dbinfo[i+28] is not None:
            if muted == dbinfo[i+28]:
                score += 1; print "muted: 1"
        if dbinfo[i+29] is not None:
            if paused == dbinfo[i+29]:
                score += 1; print "paused: 1"
        if dbinfo[i+30] is not None:
            if speedChange == dbinfo[i+30]:
                score += 1; print "speedChange: 1"
        if dbinfo[i+31] is not None:
            if currentTime <= dbinfo[i+31]+1 and currentTime >= dbinfo[i+31]-1:
                score += 3; print "currentTime: 3"
        if dbinfo[i+32] is not None:
            if ended == dbinfo[i+32]:
                score += 1; print "Ended: 1"
        if dbinfo[i+33] is not None:
            if seek == dbinfo[i+33]:
                score += 1; print "seek: 1"
        print "Score: ", score
        return score

if __name__ == "__main__":
    print "Main procedure";
    HOST, PORT = "localhost", 19999;

    my_server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler);
    ip, port = my_server.server_address;

    ## Load universal dataset to create imposters (Here means CMU dataset)
    CMUData = DataProcess("../Dataset/Kevin and Maxion/DSL-StrongPasswordData_new.csv");
    CMUData.processOnCMU();
    Keystroke_Imposter = CMUData.imposter;

    server_thread = threading.Thread(target=my_server.serve_forever());
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True;
    server_thread.start();
    print "Sever is running\n";
