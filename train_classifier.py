import  numpy as np
import matplotlib.pyplot as plt
import  sklearn.svm as svm
from sklearn.svm import LinearSVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from nltk.corpus import sentiwordnet as swn
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier

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
'''features:
the sum of words score,count(pos),
count(neg),count(neu),count(all words) '''
def extract_features(dataset):

    features=[]
    for line in dataset:
        sum_score = 0
        pos_count = 0
        neg_count = 0
        neu_count = 0
        all_count = 0
        all_count = len(line)

        for row in line:
            if len(list(swn.senti_synsets(row)))>0:
                word=[]
                for i in swn.senti_synsets(row):
                    word = i
                    break;
                pos_score = word.pos_score()
                neg_score = word.neg_score()
                neu_score = word.obj_score()
                max_score = max(pos_score,neg_score,neu_score)

                if max_score == neu_score:
                    neu_count+=1
                elif max_score == neg_score:
                    neg_count+=1
                    sum_score=sum_score+(-1)*max_score
                elif max_score == pos_score:
                    pos_count+=1
                    sum_score+=max_score
        features.append([sum_score,pos_count,neg_count,neu_count,all_count])

    return features





if __name__ == '__main__':
    posData_path = "/home/lt228/Desktop/Depression-detection/positive_model.csv"
    negData_path = "/home/lt228/Desktop/Depression-detection/negative_model.csv"
    pos_csv = pd.read_csv(posData_path)
    neg_csv = pd.read_csv(negData_path)
    pos_model = np.array(pos_csv.iloc[:,1:14])
    neg_model = np.array(neg_csv.iloc[:,1:14])
    dataset= np.concatenate((pos_model,neg_model))
    target = np.append(np.ones(len(pos_model)),np.zeros(len(neg_model)))
    print(dataset.shape)
    print("Strating training...")
    svr = svm.SVC()
    parameters = {'kernel': ('rbf', 'rbf'), 'C': [0.1,0.3,0.9,1,10], 'gamma': [0.125, 0.25, 0.5, 1, 2, 4]}
    X_train, X_test, y_train, y_test = train_test_split(dataset,
                                                        target,test_size=0.25)
    print(len(X_train))

    ##joblib.dump(clf,"/Users/charles_tong/Desktop/Depression-detection/classifier_model/svm.model")
    clf = GridSearchCV(svr,parameters)
    clf.fit(X_train,y_train)
    print("over")
    print(clf.best_params_)
    print(clf.best_score_)
    print("Test Accuracy: %f"%clf.score(X_test,y_test))








