import  numpy as np
import matplotlib.pyplot as plt
import  sklearn.svm as svm
def open_model(path):

    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        data=f.read()
    return data
## remove repetion data
def remove_repretion(data):
    length = len(data)
    for i in range(length):
        data[i]=set(data[i])
        if len(data[i])==0:
            data.remove(data[i])
    return sorted(data,key = lambda x:len(x))[-1]



def compare(a,b):
    max=0
    if a>=b:
        max =a
    else:
        max = b
    return max



if __name__ == '__main__':
    posData_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/positive_model.txt"
    negData_path = "/home/charles/tool/Depression_detection/tweet-ubuntu/negative_model.txt"



    posData = open_model(posData_path)
    negData = open_model(negData_path)
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
            traing_X[line].append(list(np.zeros(max_length-len(traing_X[line]))))
        if len(posData) <= (line+1) :
            traing_y.append(1)
        else:
            traing_y.append(0)

    clf = svm.SVC()
    clf.fit(traing_X,traing_y)