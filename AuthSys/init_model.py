import os
import string
import random
import numpy as np
from sklearn.mixture import GMM
from sklearn import cross_validation

class Init_model:
    """ This class provides methods to train the GMM model for user behavior analyse. Including searching the optimal parameters,
    and training model."""

    def __init__(self, imposters, train_data, index_user, profile = None):
        self.imposter_features = imposters; ## Imposter pool for search parameters
        self.train_data = train_data; ## The train data of one user
        self.index_user = index_user; ## The index of user in the whole database
        self.profile = profile;

    ## Grid search to find the optimal parameters for the GMM LOOM model
    ## A very important part in model training
    ## This function needs improvement in the future
    def __searchOfParameters(self, train_data, index_user):
        kf = cross_validation.KFold(len(train_data), n_folds=5, shuffle=True);
        train_index, test_index = next(iter(kf));
        train, test = train_data[train_index], train_data[test_index];
        if (len(train) < 50):
            trainSet = np.array(train_data);
            genuine_user = trainSet;
        else:
            trainSet = train;
            if (len(test) >= 100):
                genuine_user = test;
            else:
                genuine_user = train_data;

        n_components_range = range(1, 50);  ## num_components: 1~50
        K_range = np.arange(0.01, 2.01, 0.01);  ## 0.01~1.99, variance is 0.01
        # covariances = ['spherical', 'diag', 'full', 'tied'];
        covariances = ['diag'];  ## seems like the best covar_type is 'diag' surely

        Opt_n_components = dict((covar_type, 0) for covar_type in covariances);
        Opt_EER = dict((covar_type, 0) for covar_type in covariances);
        Opt_K = dict((covar_type, 0) for covar_type in covariances);

        ## Extract imposter from the imposter pool. Now, all the imposters are coming from CMU dataset
        ## Uniform the imposter_data's dimension with train_data's
        imposter_size = len(train_data[0]);
        imposter_user = np.concatenate((self.imposter_features[0:index_user],
                                        self.imposter_features[index_user + 1:])).reshape(250, imposter_size);
        genuine_user = np.array(genuine_user);

        loo = cross_validation.LeaveOneOut(len(trainSet));

        for covar_type in covariances:
            EER, K_Seq, FAR, FRR = [], [], [], [];

            for num_components in n_components_range:
                model = GMM(n_components=num_components, covariance_type=covar_type, init_params='wc', n_iter=20);
                min_dis = np.infty;  ## distance between FAR & FRR
                eer_k, eer_far, eer_frr = 0, 0, 0;  ## the value of LOOM K, FAR and FRR at EER point

                Scores = [];
                for train_index, test_index in loo:
                    train, test = trainSet[train_index], trainSet[test_index];
                    model.fit(train);
                    Scores.append(model.score(test));

                model.fit(trainSet);
                Scores = np.array(Scores).ravel();
                mean = np.mean(Scores);
                std = np.std(Scores);

                scores_imposter = [model.score(imposter_user[i].reshape(1, -1)) for i in range(len(imposter_user))];
                scores_genuine = [model.score(genuine_user[i].reshape(1, -1)) for i in range(len(genuine_user))];

                for K in K_range:
                    Seq = [Scores[j] for j in range(len(Scores)) if abs(Scores[j] - mean) < K * std];
                    if (not Seq):
                        threshold_user = mean - K * std;
                    else:
                        threshold_user = min(Seq);

                    reject, accept = 0, 0;
                    ## imposter test
                    for i in range(len(scores_imposter)):
                        if (scores_imposter[i] >= threshold_user):
                            accept = accept + 1;

                    ## genuine test
                    for i in range(len(scores_genuine)):
                        if (scores_genuine[i] < threshold_user):
                            reject = reject + 1;

                    far = (float(accept) / float(len(scores_imposter)));
                    frr = (float(reject) / float(len(scores_genuine)));
                    if (min_dis > abs(far - frr)):
                        min_dis = abs(far - frr);
                        ## eer = (far, frr);
                        eer = np.mean([far, frr]);  ## I am not sure whether it's approprate
                        eer_k, eer_far, eer_frr = K, far, frr;

                ### End of K Loop
                K_Seq.append(eer_k);
                EER.append(eer);
                FAR.append(eer_far);
                FRR.append(eer_frr);

            ###End of n_components Loop
            min_eer = min(EER);
            opt_pos = EER.index(min_eer);  ## n_components begins from 1
            Opt_K[covar_type] = K_Seq[opt_pos];  ## The K value of the minimal EER model
            Opt_n_components[
                covar_type] = opt_pos + 1;  ## The n_components of the model under this cover_type with minimal EER
            Opt_EER[covar_type] = min_eer;  ## The minimal EER under this cover_type in the n_components range(1,50)

        ### End of covar_type Loop
        covar_type = min(Opt_EER);  ## choose the minimal EER as the optimal situation
        print "Minimal EER: ", Opt_EER[covar_type];
        K = Opt_K[covar_type];
        n_components = Opt_n_components[covar_type];
        parameters = {'n_components': n_components, 'covar_type': covar_type, 'K': K};
        return parameters;

    def train_Model_GMM_LOOM(self, n_components=None, covar_type=None, k_loom=None, auto=True):
        if(auto):
            parameters = self.__searchOfParameters(self.train_data, self.index_user);
            model = GMM(n_components=parameters['n_components'], covariance_type=parameters['covar_type'],
                        init_params='wc', n_iter=20);
            k_loom = parameters['K'];
        else:
            model = GMM(n_components=n_components, covariance_type=covar_type,
                        init_params='wc', n_iter=20);

        ##LOOM Method
        loo = cross_validation.LeaveOneOut(len(self.train_data));
        Scores = [];
        for train_index, test_index in loo:
            train, test = self.train_data[train_index], self.train_data[test_index];
            model.fit(train);
            Scores.append(model.score(test));

        Scores = np.array(Scores).ravel();
        mean = np.mean(Scores);
        std = np.std(Scores);

        Seq = [Scores[i] for i in range(len(Scores)) if abs(Scores[i] - mean) < k_loom * std];
        if (not Seq):
            threshold = mean - k_loom * std;
        else:
            threshold = min(Seq);

        ## Train the GMM model. Profile includes a GMM model and a threshold
        model.fit(self.train_data);
        self.profile = dict({'model': model, 'threshold': threshold});
        print "Train size: ", len(self.train_data), " K_LOOM: ", k_loom, " profile: ", self.profile;
        return self.profile;