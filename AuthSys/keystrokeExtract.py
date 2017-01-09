import string

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

"""This file provides all the functions which extract the keystroke feature from the front-end's raw data"""

def isPrintable(text):
    printset = set(string.printable);
    return set(text).issubset(printset);

def RemoveMistake(Content):
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
                while (not isPrintable(Content[i - 1].key)):
                    del Content[i - 1];
                    i -= 1;
                    length -= 1;

                ## remove the printable char that should be remove by this Backspace
                del Content[i - 1:i + 1];
                length -= 2;
                i -= 2;
        i += 1;

def extract_Feature(Press_Sequence, Reference):
    RemoveMistake(Press_Sequence);

    Feature = [];
    i = len(Press_Sequence) - 1;
    j = len(Reference) - 1;
    ## match the sequence from the backward
    while (i >= 0 and j >= 0):
        if (Press_Sequence[i].key == Reference[j]):
            ## if the char is in upper case, and the previous pressed key is 'shift'
            ## options: 1. if so, take the 'shift' into the feature vector
            ## 2. instead of taking 'shift' into account, jump over the 'shift'
            # if (Press_Sequence[i].key.isupper() and Press_Sequence[i - 1].which == 16):
            #     Feature.append(Press_Sequence[i - 1]);

            Feature.append(Press_Sequence[i]);
            j -= 1;
        i -= 1;

    Feature.reverse();
    return Feature;

def collectKeystroke(String, Keystroke):
    KeyVector = [KeyEvent(Keystroke[i]['index'], Keystroke[i]['key'],
                          Keystroke[i]['which'], Keystroke[i]['time_D'],
                          Keystroke[i]['time_U']) for i in range(len(Keystroke))];

    ## Deal with typing mistake and generate feature vector
    ## sort by pressed index. The orginal vector is in sequence of release
    Press_Sequence_Keystroke = sorted(KeyVector, key=lambda keyevent: keyevent.index);
    print "Length of Keystroke's Keyevent Pressed Sequence: ", len(Press_Sequence_Keystroke)

    ## Look for user's correct password as reference according to its username
    ## The real password is used as the reference which helps us to extract the keystroke feature
    Keystroke = extract_Feature(Press_Sequence_Keystroke, String);
    print "Length of well-processed Keystroke Keyevent Sequence: ", len(Keystroke);

    ## Generate feature vectors for each sub-feature,
    ## four kinds of sub-features: hold-time, DDKL, UDKL, UUKL
    H_time_Keystroke = [(Keystroke[i].time_U - Keystroke[i].time_D) / 1000
                        for i in range(len(Keystroke))];

    DDKL_Keystroke = [(Keystroke[i + 1].time_D - Keystroke[i].time_D) / 1000
                      for i in range(len(Keystroke) - 1)];

    UDKL_Keystroke = [(Keystroke[i + 1].time_D - Keystroke[i].time_U) / 1000
                      for i in range(len(Keystroke) - 1)];

    # UUKL_Password = [(Password_Keystroke[i + 1].time_U - Password_Keystroke[i].time_U) / 1000
    #                  for i in range(len(Password_Keystroke) - 1)];

    ## Feature_Vector is the final feature vector which is used to verify user's keystroke
    ## Generate feature's vector used for authentication
    Feature_Vector = [];
    for i in range(len(H_time_Keystroke)):
        ## Remain the first 4 digits after the decimal point
        Feature_Vector.append(round(H_time_Keystroke[i], 4));
        if (i < len(DDKL_Keystroke)):
            Feature_Vector.append(round(DDKL_Keystroke[i], 4));
            Feature_Vector.append(round(UDKL_Keystroke[i], 4));

    return Feature_Vector;