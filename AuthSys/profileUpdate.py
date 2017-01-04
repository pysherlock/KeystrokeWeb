import csv
import numpy as np

ContinuousFactors = {'press', 'width', 'height', 'volume'};

class ProfileUpdate:

    def __init__(self, username, logfile, database):
        self.__username = username;
        self.__logfile = logfile;
        self.__database = database;

    def __WriteToDB(self, factor, value, dtype):
        cur = self.__database.cursor();
        if dtype == 'f':
            sql = "UPDATE users SET %s=%f WHERE `username`='%s'" \
              % (factor, value, self.__username);
        elif dtype == 's':
            sql = "UPDATE users SET %s=%s WHERE `username`='%s'" \
              % (factor, value, self.__username);

        print sql;
        try:
            print "Write to DB";
            cur.execute(sql);
            self.__database.commit();
        except:
            print "Exception";
            self.__database.rollback();
            self.__database.close();

    def Update(self):
        with open(self.__logfile, 'r') as file:
            reader = csv.reader(file);
            self.data = np.array([row for row in reader]);

        factors = self.data[0];
        values = np.delete(self.data, 0, 0);

        print "Factors: ", factors;
        print "Values: ", type(values), values;

        for i in range(len(factors)):
            if(factors[i] in ContinuousFactors): ## the continuous variables
                ## TODO: Find a way to deal with continuous variables(factors)
                new_value = np.mean(values[:, i].astype(float)); ## This method is not good
                print "New_value: ", type(new_value), new_value;
                self.__WriteToDB(factor=factors[i], value=new_value, dtype='f');

            else: ## the discrete variables and the boolean variables
                map = {};
                for value in values[:, i]:
                    if(map.has_key(value)):
                        map[value] += 1;
                    else:
                        map[value] = 1;

                sorted_map = sorted(map.items(), key=lambda element: element[1], reverse=True);
                first = sorted_map[0];

                if(float(first[1])/10.0 >= .8): ## choose the value which appears more than 80% to be the new value
                    new_value = first[0];
                    print "New_value: ", type(new_value), new_value;
                    self.__WriteToDB(factor=factors[i], value=new_value, dtype='s');

        self.__database.close();
