import nltk;
import enchant;
import os;
def get_txt(path):
    txt_path=[]
    fileList = os.listdir(path)
    for filename in fileList:
        file_path = os.path.join(path, filename)
        if filename[-4:].upper() == '.TXT':
            txt_path.append(file_path)
    return txt_path


def isEnglishWords(word):
    english_dict = enchant.Dict("en_UK")
    return english_dict.check(word)

'''keyword == nouns,adjective,adverb'''
def findKeyword(file_path):
    keyword_list =[]
    with open(file_path, 'r', encoding="utf-8",errors="ignore") as f:
        
        word_list= nltk.word_tokenize(f.read().lower())
        pos_tag = nltk.pos_tag(word_list)
        for i in range(len(pos_tag)):
            if pos_tag[i][1] == 'JJ' or pos_tag[i][1] == 'JJR' or pos_tag[i][1] == 'JJR' or pos_tag[i][1] == 'JJS' or pos_tag[i][1] == 'NN' or pos_tag[i][1] == 'NNS' or pos_tag[i][1] == 'NNP' or pos_tag[i][1] == 'NNPS' or pos_tag[i][1] == 'RB' or pos_tag[i][1] == 'RBR' or pos_tag[i][1] == 'RBS':
                if isEnglishWords(pos_tag[i][0]):
                    print(pos_tag[i])
                    keyword_list.append(pos_tag[i][0])
        
    return keyword_list


if __name__=='__main__':
    pos_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/positive-depressed/txt")
    neg_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/negative-undepressed/txt")
    
    pos_words = []
    neg_words = []
    for i in pos_path:
        pos_words.append(findKeyword(i))
        print(i)
    print(pos_words)


