import os
import string
import random
import numpy as np
from sklearn.mixture import GMM
from sklearn import cross_validation


class KeyEvent:
    """This class records all the useful keyevent information. Including keydown time and keyup time"""
    keyCount = 0;

    def __init__(self, index, key, which, time_D, time_U):
        self.index = index;  ## The index of pressing sequence
        self.key = key;
        self.which = which;  ## Keycode
        self.time_D = time_D;
        self.time_U = time_U;
        KeyEvent.keyCount += 1;

class MakeAuth:
    """This class provides the main methods which make the final authentication result. The main class of the file"""

    def __init__(self, Profiles, mean, std):
        self.Profiles = Profiles;
        self.global_Mean, self.global_Std = mean, std;


    def make_Auth(self, model, threshold, feature):
        score = model.score(feature);
        if(score < threshold):
            return [False, score[0], threshold];
        else:
            return [True, score[0], threshold];


    def main_Authentication(self, username, password, Username_keyMap, Password_keyMap):

        if (not self.Profiles.has_key(username)):
            print "This user doesn't exist";
            return 2;
        elif (self.Profiles[username]["Password"] != password):
            print "Password is not correct";
            return 3;

        Username = username;
        Password = password;

        ## Password.append("Enter"); ## Because we should let the password be compatible with CMU password

        Username_keyevent = [KeyEvent(Username_keyMap['index'][i], Username_keyMap['key'][i],
                                      Username_keyMap['which'][i], Username_keyMap['time_D'][i],
                                      Username_keyMap['time_U'][i]) for i in range(len(Username_keyMap['index']))];

        Password_keyevent = [KeyEvent(Password_keyMap['index'][i], Password_keyMap['key'][i],
                                      Password_keyMap['which'][i], Password_keyMap['time_D'][i],
                                      Password_keyMap['time_U'][i]) for i in range(len(Password_keyMap['index']))];

        ## Deal with typing mistake and generate feature vector
        ## sort by pressed index. The orginal vector is in sequence of release
        Press_Sequence_Username = sorted(Username_keyevent, key=lambda keyevent: keyevent.index);
        Press_Sequence_Password = sorted(Password_keyevent, key=lambda keyevent: keyevent.index);

        # RemoveMistake(Press_Sequence_Username);
        # RemoveMistake(Press_Sequence_Password);

        ## Look for user's correct password as reference according to its username
        ## The real password is used as the reference which helps us to extract the keystroke feature
        Username_Keystroke = KeyExtract.extract_Feature(Press_Sequence_Username, Username);
        Password_Keystroke = KeyExtract.extract_Feature(Press_Sequence_Password, Password);

        ## Generate feature vectors for each sub-feature,
        ## four kinds of sub-features: hold-time, DDKL, UDKL, UUKL
        H_time_Username = [(Username_Keystroke[i].time_U - Username_Keystroke[i].time_D) / 1000
                           for i in range(len(Username_Keystroke))];
        H_time_Password = [(Password_Keystroke[i].time_U - Password_Keystroke[i].time_D) / 1000
                           for i in range(len(Password_Keystroke))];

        DDKL_Username = [(Username_Keystroke[i + 1].time_D - Username_Keystroke[i].time_D) / 1000
                         for i in range(len(Username_Keystroke) - 1)];
        DDKL_Password = [(Password_Keystroke[i + 1].time_D - Password_Keystroke[i].time_D) / 1000
                         for i in range(len(Password_Keystroke) - 1)];

        UDKL_Username = [(Username_Keystroke[i + 1].time_D - Username_Keystroke[i].time_U) / 1000
                         for i in range(len(Username_Keystroke) - 1)];
        UDKL_Password = [(Password_Keystroke[i + 1].time_D - Password_Keystroke[i].time_U) / 1000
                         for i in range(len(Password_Keystroke) - 1)];

        # UUKL_Username = [(Username_Keystroke[i + 1].time_U - Username_Keystroke[i].time_U) / 1000
        #                  for i in range(len(Username_Keystroke) - 1)];
        # UUKL_Password = [(Password_Keystroke[i + 1].time_U - Password_Keystroke[i].time_U) / 1000
        #                  for i in range(len(Password_Keystroke) - 1)];

        ## Feature_Vector is the final feature vector which is used to verify user's keystroke
        ## Generate feature's vector used for authentication
        Feature_Vector = [];
        for i in range(len(H_time_Password)):
            Feature_Vector.append(H_time_Password[i]);
            if (i < len(DDKL_Password)):
                Feature_Vector.append(DDKL_Password[i]);
                Feature_Vector.append(UDKL_Password[i]);

        ## Feature normalization
        for i in range(len(Feature_Vector)):
            Feature_Vector[i] = (Feature_Vector[i] - self.global_Mean[i]) / self.global_Std[i];

            ## Make the keystroke authentication
            #     print "Make authentication";
            #     if(make_Authentication(Profiles[Username]['Profile']['model'],
            #                            Profiles[Username]['Profile']['threshold'],
            #                            np.array(Feature_Vector).reshape(1,-1))):
            #         return 0;
            #     else:
            #         return 1;

        ## For demo and testing phase
        result = self.make_Auth(self.Profiles[Username]['Keystroke']['model'],
                                self.Profiles[Username]['Keystroke']['threshold'],
                                np.array(Feature_Vector).reshape(1, -1));
        return result;


class KeyExtract:

    """This class provides all the methods which extract the keystroke feature from the front-end's raw data"""
    def __init__(self):
        self

    def isPrintable(self, text):
        printset = set(string.printable);
        return set(text).issubset(printset);

    def RemoveMistake(self, Content):
        ## Deal with typing mistake and generate feature vector
        ## Backspace:
        length = len(Content);
        i = 0;
        while (i < length):
            item = Content[i];
            if (item.which == 8):
                ## remove Backspace and other keys that user deletes because of mistake
                ## if find a Backspace, delete the Backspace and the key in front of it
                ## additional Backspace: only remove Backspace
                if (i == 0):
                    del Content[i];
                    length -= 1;
                    i -= 1;
                ## remove the Backspace and wrong characters
                else:
                    ## remove all the other non-printable char before the Backspace
                    while (not self.isPrintable(Content[i - 1].key)):
                        del Content[i - 1];
                        i -= 1;
                        length -= 1;

                    ## remove the printable char that should be remove by this Backspace
                    del Content[i - 1:i + 1];
                    length -= 2;
                    i -= 2;
            i += 1;

    def extract_Feature(self, Press_Sequence, Reference):
        Press_Sequence = self.RemoveMistake(Press_Sequence);

        Feature = [];
        i = len(Press_Sequence) - 1;
        j = len(Reference) - 1;
        ## match the sequence from the backward
        while (i >= 0 and j >= 0):
            if (Press_Sequence[i].key == Reference[j]):
                ## if the char is in upper case, and the previous pressed key is 'shift'
                ## if so, take the 'shift' into the feature vector
                if (Press_Sequence[i].key.isupper() and Press_Sequence[i - 1].which == 16):
                    print Press_Sequence[i].key;
                    Feature.append(Press_Sequence[i - 1]);

                Feature.append(Press_Sequence[i]);
                j -= 1;
            i -= 1;

        Feature.reverse();
        return Feature;