import  numpy as np
import matplotlib.pyplot as plt
import  sklearn.svm as svm
from sklearn.svm import LinearSVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from nltk.corpus import sentiwordnet as swn

from sklearn.ensemble import RandomForestClassifier

import pandas as pd

from sklearn.externals import joblib

def open_model(path):

    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        data=f.read()
    return data
## remove repetion data
'''
def remove_repretion(data):
    
    length = len(data)
    for i in range(length):

        data[i]=list(set(data[i]))

    while [] in data:
        data.remove([])

    return sorted(data,key = lambda x:len(x),reverse=True)

'''

def compare(a,b):
    max=0
    if a>=b:
        max =a
    else:
        max = b
    return max






if __name__ == '__main__':
    posData_path = "/Users/charles_tong/Desktop/Depression-detection/positive_model.csv"
    negData_path = "/Users/charles_tong/Desktop/Depression-detection/negative_model.csv"
    pos_csv = pd.read_csv(posData_path)
    neg_csv = pd.read_csv(negData_path)
    pos_model = np.array(pos_csv.iloc[:,2:15])
    neg_model = np.array(neg_csv.iloc[:,2:15])
    dataset= np.concatenate((pos_model,neg_model))
    target = np.append(np.ones(len(pos_model)),np.zeros(len(neg_model)))
    print(dataset.shape)
    print("Strating training...")

    X_train, X_test, y_train, y_test = train_test_split(dataset,
                                                        target, test_size=0.25)
    from sklearn.tree import DecisionTreeClassifier

    RF_estimator = RandomForestClassifier(n_estimators=100)
    RF_estimator.fit(X_train,y_train)
    print(RF_estimator.score(X_test,y_test))


    # svr = svm.SVC()
    # parameters = {'kernel': ('rbf', 'rbf'), 'C': [0.1,0.3,0.9,1,10], 'gamma': [0.125, 0.25, 0.5, 1, 2, 4]}

    # print(len(X_train))
    #
    # ##joblib.dump(clf,"/Users/charles_tong/Desktop/Depression-detection/classifier_model/svm.model")
    # clf = GridSearchCV(svr,parameters)
    # clf.fit(X_train,y_train)
    # print("over")
    # print(clf.best_params_)
    # print(clf.best_score_)
    # print("Test Accuracy: %f"%clf.score(X_test,y_test))











