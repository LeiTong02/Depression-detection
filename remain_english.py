import nltk
import ast
import langid
import os
import csv
def judge_pure_english(tweet):
    language = langid.classify(tweet)
    return language[0]

def open_file(path):
    count = 0
    len=0
    path = "/Users/charles_tong/Desktop/tweet/positive/csv/rumpfcounselingcreated_at318594325.csv"
    with open(path,'r',encoding="utf-8",errors="ignore") as f:

        reader =csv.reader(f)
        txt_name = f.name

        name_string = txt_name.split('/')[-1]
        name_string = name_string[:-4] + '.json'
        print(name_string)
        json_name = os.path.join(os.path.dirname(os.path.dirname(path)), name_string)
        for tweet in reader:
            len=+1
            result =judge_pure_english(tweet[1])
            if result != 'en':
                with open(json_name,'r',encoding="utf-8",errors="ignore") as json_file:
                    filelines = json_file.readlines()
                filelines[int(tweet[0])]=""
                with open(json_name,'w',encoding="utf-8",errors="ignore") as json_write:
                    json_write.writelines(filelines)
                count+=1


    if count == len:
        ##os.remove(txt_name)
        ##os.remove(json_name)
        print("delete file: %s"%(json_name))




from extract_features import get_txt
if __name__ == '__main__':
    pos_path = "/Users/charles_tong/Desktop/tweet/positive/csv"
    neg_path = "/Users/charles_tong/Desktop/tweet/negative/csv"

    for pos_txt_path in get_txt(pos_path):
        open_file(pos_txt_path)
        break;
    print("positive finished")
    for neg_txt_path in get_txt(neg_path):
        open_file(neg_txt_path)
    print("negative finished")
