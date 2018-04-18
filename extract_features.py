import nltk;
from nltk.corpus import sentiwordnet as swn
from nltk import pos_tag
import pandas as pd
import time
import os;
from Model import Social_network_feature
from collections import Counter
import numpy as np
from text_preprocess import *
import re
from wordsegment import load,segment
from nltk.corpus import wordnet as wn
def get_csv(path):
    txt_path=[]

    fileList = os.listdir(path)
    for filename in fileList:
        file_path = os.path.join(path, filename)
        if filename[-4:].upper() == '.CSV':
            txt_path.append(file_path)
    return txt_path

def social_network_feature(path):
    csv = pd.read_csv(path)

    if csv.shape[0] <= 10:
        return False
    else:

        rows = csv.shape[0]
        emojis_ave = sum(csv.emoji_count) / rows
        emoticons_ave = sum(csv.emoticon_count) / rows
        favorite_ave = sum(csv.favorite_count) / rows
        followers = csv.followers_count[0]
        friends = csv.friends_count[0]
        listed_count = csv.listed_count[0]
        mention_ave = sum(csv.mention_count) / rows
        retweet_ave = sum(csv.retweet_count) / rows
        total_favourites_count = csv.total_favourites_count[0]
        # row number - False number = True number
        quote_ratio = rows-Counter(csv.is_quote_status)[False]/rows
        statues_count = csv.statues_count[0]
        text_length_ave = sum(len(sentence.split()) for sentence in csv.text)/rows
        polarity_ave = sum(csv.polarity)/rows
        subjectivity_ave = sum(csv.subjectity)/rows
        truncated_ratio = rows-Counter(csv.truncated)[False]/rows


        '''Count the number of posting between 9:00pm and 6:00am'''
        time_Series = csv.created_at
        nightTime_count = 0
        # Record 24h time distribution
        time_distribution = list(np.zeros(24))
        for time_row in time_Series:
            time_struct = time.strptime(time_row, "%a %b %d %H:%M:%S +0000 %Y")
            HMS = int(time.strftime("%H%M%S", time_struct))
            time_distribution[int(HMS/10000)]+=1
            if HMS < 60000 or HMS >= 210000:
                nightTime_count += 1
        # Normalize time feature
        time_distribution = [(hour/rows) for hour in time_distribution]
        night_time_ratio = nightTime_count / rows
        day_time_ratio = 1 - night_time_ratio

        text_Series = csv.text
        RT_ratio = 0
        links_ratio=0
        for text in text_Series:
            RT_ratio = len(re.findall(r'^response',text))
            links_ratio = len(re.findall(r'URL',text))
        # pos_word and neg_word should be calculated after removing stop words
        ''' 
        pos_words = 0
        neg_words = 0
        Should modify here for specifying word class   
        for text in text_Series:

            for word in text:
                if len(list(swn.senti_synsets(word)))>0:
                    for synset in swn.senti_synsets(word):
                        score = synset
                        break
                    if score.pos_score() > score.neg_score():
                        pos_words += 1
                    elif score.pos_score() < score.neg_score():
                        neg_words += 1
        pos_words= pos_words/rows
        neg_words= neg_words/rows
        '''

        sn_class = Social_network_feature(day_time_ratio,night_time_ratio,time_distribution,emojis_ave,emoticons_ave,retweet_ave,favorite_ave,
                                             listed_count,mention_ave,followers,friends,total_favourites_count,
                                             rows,quote_ratio,statues_count,text_length_ave,RT_ratio,
                                             links_ratio,polarity_ave,subjectivity_ave,truncated_ratio)
        return sn_class
#Count pos words and neg words
def pos_neg_wordsCount(tweet):
    ## remove URL,reponse,number and stop words
    tweet_token = remove_unlessword(tweet)

    pos_words = 0
    neg_words = 0


    for word,pos in pos_tag(tweet_token):
        wordnet_pos = get_wordnet_pos(pos) or wn.NOUN
        if list(swn.senti_synsets(word,wordnet_pos)):
            for synset in swn.senti_synsets(word):
                score = synset
                break
            if score.pos_score() > score.neg_score():
                pos_words += 1
            elif score.pos_score() < score.neg_score():
                neg_words += 1
    return pos_words,neg_words



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
    filename = name +'.csv'
    path = os.path.join("/Users/charles_tong/Desktop/Depression-detection",filename)
    pd.DataFrame(data).to_csv(path)

def storeinDict(dict,SN_feature):
    dict['day_time_ratio'].append(SN_feature.day_time_ratio)
    dict['night_time_ratio'].append(SN_feature.night_time_ratio)
    dict['time_distribution'].append(SN_feature.time_distribution)
    dict['emojis_ave'].append(SN_feature.emojis)
    dict['emoticons_ave'].append(SN_feature.emoticons)
    dict['retweet_ave'].append(SN_feature.retweet_count)
    dict['favorite_ave'].append(SN_feature.favorite)
    dict['listed_count'].append(SN_feature.listed_count)
    dict['mention_ave'].append(SN_feature.mention_count)
    dict['followers'].append(SN_feature.followers)
    dict['friends_count'].append(SN_feature.friends)
    dict['favourites'].append(SN_feature.favorites)
    dict['posts'].append(SN_feature.posts)
    dict['quote_ratio'].append(SN_feature.quote_count)
    dict['statues_count'].append(SN_feature.statues_count)
    dict['text_length_ave'].append(SN_feature.text_length)
    dict['RT_ratio'].append(SN_feature.RT_ratio)
    dict['links_ratio'].append(SN_feature.links)
    dict['polarity_ave'].append(SN_feature.polarity)
    dict['subjectivity_ave'].append(SN_feature.subjectivity)
    dict['truncated_ratio'].append(SN_feature.subjectivity)



if __name__=='__main__':
    # Linux address /home/charles/tool/Depression_detection/tweet-ubuntu/negative-undepressed/txt
    pos_path = get_csv("/home/lt228/Desktop/tweet/positive/csv")
    neg_path = get_csv("/home/lt228/Desktop/tweet/negative/csv")
    # Social network features
    pos_dict = {"day_time_ratio": [],'night_time_ratio':[],'time_distribution':[], "emojis_ave": [],
                "emoticons_ave": [], "retweet_ave": [], "favorite_ave": [], "listed_count": [],
                "mention_ave": [], "followers": [], "friends_count": [],
                "favourites": [], "posts": [],'quote_ratio':[],'statues_count':[],'text_length_ave':[],'RT_ratio':[],
                'links_ratio':[],'polarity_ave':[],'subjectivity_ave':[],'truncated_ratio':[]}
    neg_dict = pos_dict.copy()

    # word segment e.g whatisyou -> what is you
    load()
    for csv_path in pos_path+neg_path:
        csv = pd.read_csv(csv_path)
        loop_text = csv.text.copy()
        for text_index,text in enumerate(loop_text):
            word_list = text.split()
            new_text=text.copy()
            modify_label = False
            for word_index,word in enumerate(word_list):
                if len(wn.synsets(word))==0:
                    new_text=new_text.replace(word,' '.join(segment(word)),1)
                    modify_label=True
            if modify_label == True:
                csv.text[text_index] =new_text
        csv.to_csv(csv_path)



    # Social network feature extract
    for pos_csv in pos_path:
        SN_feature= social_network_feature(pos_csv)
        if SN_feature:
            storeinDict(pos_dict,SN_feature)

            print(pos_path.index(pos_csv))
    save_model("positive_model",pos_dict)
    print("Positive model generated")


    for neg_csv in neg_path:
        SN_feature = social_network_feature(neg_csv)
        if SN_feature:
            storeinDict(neg_dict,SN_feature)

            print(neg_path.index(neg_csv))

    save_model("negative_model", neg_dict)
    print("Negative model generated")








