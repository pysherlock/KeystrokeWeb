import os
import csv
import random
import numpy as np
from sklearn import cross_validation

class DataProcess:
    """ This class provides all the methods that read and pre-process data to the usable format"""
    global_Mean = None;
    global_Std = None;

    def __init__(self, file_path, data=None, data_user=None, imposter=None):
        self.file_path = file_path;
        self.data = data;
        self.data_user = data_user;
        self.imposter = imposter;
        self.Mean, self.Std = [], []; ##record the mean and std for each feature over the whole dataset
        # self.data, self.data_user, self.imposter;

    def Z_normalize(self, data, mean, std):
        num_col = len(data[0]);
        num_row = len(data);

        for j in range(num_col):
            for i in range(num_row):
                data[i][j] = (data[i][j] - mean[j]) / std[j];
        return data;

    def cross_valid(self, data, fold, shuffle):

        kf = cross_validation.KFold(len(data), n_folds=fold, shuffle=shuffle);
        print kf;
        train_index, test_index = next(iter(kf));
        train, test = data[train_index], data[test_index];

        train_targets = train[:, 0:1].ravel();
        train_features = train[:, 3:];
        test_targets = test[:, 0:1].ravel();
        test_features = test[:, 3:];

        # return train_targets, train_features, test_targets, test_features;
        return train_features;

    def process(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file);
            self.data = np.array([row for row in reader]);
        self.data = np.array(self.data);
        self.data = self.data.astype(np.float);

        ## data normalization (z-score)
        num_feature = len(self.data[0]);
        for i in range(num_feature):
            self.Mean.append(np.mean(self.data[:, i]));
            self.Std.append(np.std(self.data[:, i]));

        ## Data normalization
        # if(DataProcess.global_Mean == None and DataProcess.global_Std == None):
        #     DataProcess.global_Mean, DataProcess.global_Std = self.Mean, self.Std;

        self.data = self.Z_normalize(self.data, DataProcess.global_Mean, DataProcess.global_Std);

    ## Now this function only deals with the CMU dataset
    def processOnCMU(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file);
            self.data = np.array([row for row in reader]);

        # self.data = np.delete(self.data, np.s_[31::1], 1);  ## Delete the "Enter"'s information
        self.data = np.delete(self.data, 0, 0);  ## Delete the first line
        num_feature = len(self.data[0]) - 3;

        # change username to index (0-50)
        for i in range(len(self.data)):
            self.data[i][0] = i/400;

        self.data = self.data.astype(np.float);

        ## data normalization (z-score)
        for i in range(num_feature):
            self.Mean.append(np.mean(self.data[:, 3 + i]));
            self.Std.append(np.std(self.data[:, 3 + i]));

        ##Set the mean and std of CMU dataset as global_Mean and global_Std
        DataProcess.global_Mean, DataProcess.global_Std =self.Mean, self.Std;

        ## Data normalization
        self.data[:, 3:] = self.Z_normalize(self.data[:, 3:], DataProcess.global_Mean, DataProcess.global_Std);
        ## Split data by different users
        self.data_user = np.array([self.data[i * 400:(i + 1) * 400] for i in range(51)]);

        ## build imposter pool
        imposter = np.array([self.data_user[i][0:5] for i in range(0, 51)]);
        # imposter_targets = imposter[:, :, 0];
        imposter_features = imposter[:, :, 3:];
        self.imposter = imposter_features;
