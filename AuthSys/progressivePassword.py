import threading
import csv
import os

from sklearn.externals import joblib
from init_model import Init_model
from data_process import DataProcess
from profileUpdate import ProfileUpdate
from notificationMail import SendNotificationMail
from keystrokeExtract import collectKeystroke


class ProgressivePassword (threading.Thread):
    def __init__(self, name, signInTimes, Keystroke, Keystroke_Imposter, keystroke_Logfile, keystroke_Profile,
                        username, userID, officeID, email, database):
        threading.Thread.__init__(self)
        self.name = name
        self.signInTimes = signInTimes
        self.Keystroke = Keystroke
        self.Keystroke_Imposter = Keystroke_Imposter
        self.keystroke_Logfile = keystroke_Logfile
        self.keystroke_Profile = keystroke_Profile
        self.username = username
        self.userID = userID
        self.officeID = officeID
        self.email = email
        self.database = database

    def run(self):
        print "\n***** Starting Thread: " + self.name + " *****"
        # Get lock to synchronize threads
        threadLock = threading.Lock()
        threadLock.acquire()
        self.__progressive_pwd()
        # Free lock to release next thread
        threadLock.release()
        print "\n***** Finish Thread: " + self.name + " *****"


    def __progressive_pwd(self):
        ## Record keystroke into user's keystroke log when authentication is successful
        if (self.Keystroke is not None):
            with open(self.keystroke_Logfile, 'ab') as csvfile:
                print "\n** Collecting the Keystroke that user typed just now **"
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(collectKeystroke(String=self.officeID, Keystroke=self.Keystroke))
                print "Collect keystroke to user's log file"

        ## User doesn't have a keystroke profile.
        ## Read user's keystroke log, if it has enough data, we train a new profile for this user
        if (os.path.isfile(self.keystroke_Logfile)):
            Data_clp = DataProcess(self.keystroke_Logfile);
            Data_clp.process();
            keystroke_amount = len(Data_clp.data);
            print "User Keystroke Data: ", Data_clp.data.shape;

            if (keystroke_amount % 50 == 0 and keystroke_amount != 0):
                ## TODO: If every time system has to check the keystroke log file
                ## TODO: In order to make sure whether this user has enough data to build a profile,
                ## TODO: It would be too expensive. We need a more efficient way, maybe store keystroke amount in DB

                ## If user's keystroke log file has 50 items keystroke data first time
                ## We train a keystroke profile for this user
                ## If user's keystroke log file has multiple 50(100, 150, 200...) items keystroke data
                ## System would update user's keystroke profile.
                ## For now, we use the keystroke dataset from CMU to make some fake imposters
                ## Cut the dimension coorespond to clp Data's dimension
                print "\n** Generating Keystroke Profile **";
                Imposter = self.Keystroke_Imposter[:, :, 0:len(Data_clp.data[0])]
                print "Keystroke Imposter: ", Imposter.shape

                model = Init_model(imposters=Imposter, train_data=Data_clp.data, index_user=self.userID)
                Profile = model.train_Model_GMM_LOOM()
                joblib.dump(Profile['model'], self.keystroke_Profile)
                keystroke_threshold = round(Profile['threshold'], 4)

                ## Connect DB to update the keystroke threshold
                cur = self.database.cursor()
                sql = "UPDATE users SET `keystroke threshold`=%f WHERE `username`='%s'" \
                      % (keystroke_threshold, self.username)

                print sql;
                try:
                    print "Write to DB";
                    cur.execute(sql);
                    self.database.commit();
                except:
                    print "Exception";
                    self.database.rollback();
                finally:
                    self.database.close();

                if keystroke_amount == 50:
                    ## Notification Mail when keystroke is ready
                    SendNotificationMail(self.email, 1).run();
                else:
                    ## Notification Mail when keystroke profile is updated
                    SendNotificationMail(self.email, 2).run();

        if (self.signInTimes >= 10):
            # self.sendNotificationMail("pu.leo.yang@gmail.com", "pu.leo.yang@gmail.com", server='smtp.gmail.com');
            ## Notification Mail when environmental factors are updated
            print "\n** Updating User's Environmental Factors **";
            SendNotificationMail(self.email).run();

            profileupdate = ProfileUpdate(username=self.username,
                                          logfile="../Dataset/Users Log/" + self.username + "_Log.csv",
                                          database=self.database);
            profileupdate.Update();