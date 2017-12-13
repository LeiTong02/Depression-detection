import  numpy as np
import matplotlib.pyplot as plt
import  sklearn.svm as svm
from nltk.corpus import sentiwordnet as swn
import ast
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
    posData_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/positive_model.txt"
    negData_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/negative_model.txt"
    posData = ast.literal_eval(open_model(posData_path))
    negData = ast.literal_eval(open_model(negData_path))

    while [] in posData:
        posData.remove([])
    while [] in negData:
        negData.remove([])



    training_X= extract_features(posData)+extract_features(negData)
    training_y=[]
    for i in range(len(training_X)):
        if len(posData) >= (i + 1):
            training_y.append(1)
        else:
            training_y.append(0)
    clf = svm.SVC()
    clf.fit(training_X,training_y)

    ##test
    posTest_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/positive.txt"
    negTest_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/negative.txt"
    posTest = ast.literal_eval(open_model(posTest_path))
    negTest = ast.literal_eval(open_model(negTest_path))

    while [] in posTest:
        posTest.remove([])
    while [] in negTest:
        negTest.remove([])

    testing_X = extract_features(posTest) + extract_features(negTest)
    testing_y = []
    for i in range(len(testing_X)):
        if len(posTest) >= (i + 1):
            testing_y.append(1)
        else:
            testing_y.append(0)

    print (clf.score(testing_X,testing_y))
    

    '''
    posData = remove_repretion(posData)
    negData = remove_repretion(negData)

    max_pos = len(posData[0])
    max_neg = len(negData[0])
    max_length = compare(max_pos,max_neg)

    traing_X = posData+negData
    traing_y = []
    ## add 0
    for line in  range(len(traing_X)):
        if len(traing_X[line])<max_length:
            traing_X[line]+=list(np.zeros(max_length-len(traing_X[line])))
        if len(posData) <= (line+1) :
            traing_y.append(1)
        else:
            traing_y.append(0)

    '''


