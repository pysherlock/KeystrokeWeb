import string
import numpy as np
from keystrokeExtract import collectKeystroke
from keystrokeExtract import KeyEvent
# from sklearn.mixture import GMM
# from sklearn import cross_validation

class MakeAuth:
    """This class provides the main methods which make the final authentication result. The main class of the file"""

    def __init__(self, Profiles=None, mean=None, std=None):
        self.Profiles = Profiles;
        self.global_Mean, self.global_Std = mean, std;

    def __make_Auth(self, model, threshold, feature):
        print "Make Auth";
        score = model.score(feature);
        if(score < threshold):
            return [False, score[0], threshold];
        else:
            return [True, score[0], threshold];

    def keystroke_Authentication(self, Profile, String, Keystroke):
        ## Get the raw keystroke feature
        KeystrokeFeature = collectKeystroke(String, Keystroke);

        ## Feature normalization
        for i in range(len(KeystrokeFeature)):
            KeystrokeFeature[i] = (KeystrokeFeature[i] - self.global_Mean[i]) / self.global_Std[i];

        print len(KeystrokeFeature);

        ## For demo and testing phase
        result = self.__make_Auth(Profile['model'],Profile['threshold'],
                                np.array(KeystrokeFeature).reshape(1, -1));
        return result;

    def main_Authentication(self, username, password, Username_keyDict, Password_keyDict):

        if (not self.Profiles.has_key(username)):
            print "This user doesn't exist";
            return "The user doesn't exist";
        elif (self.Profiles[username]["Password"] != password):
            print "Password is not correct";
            return "Password is not correct";

        Feature_Vector = collectKeystroke(String=password, Keystroke=Password_keyDict);
        Username_Vector = collectKeystroke(String=username, Keystroke=Username_keyDict);

        ## Feature normalization
        for i in range(len(Feature_Vector)):
            Feature_Vector[i] = (Feature_Vector[i] - self.global_Mean[i]) / self.global_Std[i];

        ## For demo and testing phase
        result = self.__make_Auth(self.Profiles[username]['Keystroke']['model'],
                                self.Profiles[username]['Keystroke']['threshold'],
                                np.array(Feature_Vector).reshape(1, -1));
        return result;
