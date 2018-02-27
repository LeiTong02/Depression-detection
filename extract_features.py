import nltk;

import os;
def get_csv(path):
    txt_path=[]

    fileList = os.listdir(path)
    for filename in fileList:
        file_path = os.path.join(path, filename)
        if filename[-4:].upper() == '.CSV':
            txt_path.append(file_path)
    return txt_path


'''keyword == nouns,adjective,adverb'''
def findKeyword(file_path):
    keyword_list =[]
    with open(file_path, 'r', encoding="utf-8",errors="ignore") as f:
        
        word_list= nltk.word_tokenize(f.read().lower())
        pos_tag = nltk.pos_tag(word_list)
        for i in range(len(pos_tag)):
            if pos_tag[i][1] == 'JJ' or pos_tag[i][1] == 'JJR' or pos_tag[i][1] == 'JJR' or pos_tag[i][1] == 'JJS' or pos_tag[i][1] == 'NN' or pos_tag[i][1] == 'NNS' or pos_tag[i][1] == 'NNP' or pos_tag[i][1] == 'NNPS' or pos_tag[i][1] == 'RB' or pos_tag[i][1] == 'RBR' or pos_tag[i][1] == 'RBS':
                if len(pos_tag[i][0])>=3:

                    keyword_list.append(pos_tag[i][0])
        
    return keyword_list

def save_model(name,data):
    filename = name +'.txt'
    path = os.path.join("/home/charles/tool/Depression_detection/tweet-ubuntu/",filename)
    with open(path,'w',encoding='utf-8',errors='ignore') as f:
        f.write(str(data))

if __name__=='__main__':
    ##Linux address /home/charles/tool/Depression_detection/tweet-ubuntu/negative-undepressed/txt
    pos_path = get_csv("/home/charles/tool/Depression_detection/test_tweet/positive/csv")
    neg_path = get_csv("/home/charles/tool/Dcsv")
    ##Mac address
    ''' 
    pos_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/positive-depressed/txt")
    neg_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/negative-undepressed/txt")
    '''
    pos_words = []
    neg_words = []

    for i in pos_path:
        print("positive = ",pos_path.index(i))
        pos_words.append(findKeyword(i))

    print(pos_words)
    save_model('positive',pos_words)

    '''
    for i in neg_path:
        print("negative = ", neg_path.index(i))
        neg_words.append(findKeyword(i))
    print(neg_words)
    save_model('negative', neg_words)
    print("finish")
    '''

