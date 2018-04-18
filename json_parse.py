#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:11:38 2017

@author: charles
"""
import os
import os.path
import json

import pandas as pd

from text_preprocess import *
from textblob import TextBlob
import emot


class HandleClass:
    def __init__(self,path):
        self.__path = path

    def get_py(self,path,json_path):
        fileList = os.listdir(path)
        for filename in fileList:
            file_path = os.path.join(path,filename)
            if os.path.isdir(file_path):
                self.get_py(file_path,json_path)
            elif filename[-5:].upper()=='.JSON':
                json_path.append(file_path)
        return json_path


    def ParseJson(self):
        json_path=[]
        json_path = self.get_py(self.__path,json_path)
        print(len(json_path))
        count = 0

        for json_file in json_path:

            tweet_dict = {'created_at': [],'text':[], 'retweet_count': [], 'favorite_count': [],
                   'en':[],    'mention_count': [], 'followers_count': [], 'friends_count': []
                , 'total_favourites_count': [], 'listed_count': [],'emoji_count': [],'emoticon_count': [],
                'polarity':[],'subjectity':[],'statues_count':[],'background_color':[],'link_color':[],'sidebar_border_color':[],
                'sidebar_fill_color':[],'text_color':[],'truncated':[],'is_quote_status':[]}



            filename = json_file.split("/")[-1]
            filename = filename[:-5] + '.csv'
            csv_file = os.path.join(self.__path, "csv", filename)


            with open(json_file,'r',encoding="utf-8",errors="ignore") as f:
                print(json_file)
                for line in f:
                    '''Load data from Json'''
                    json_data = json.loads(line)

                    tweet_lang = json_data['lang']
                    if tweet_lang=="en":
                        self.Jsonloads(tweet_dict,json_data,'en','')
                    elif tweet_lang=='und':
                        continue
                    else:
                        # Translate noun english sentence
                        unEN_text = regular_express(json_data['text'])

                        if len(unEN_text)>=3:

                            try:
                                emoji_count = len(emot.emoji(unEN_text))
                                emoticon_count = len(emot.emoticons(unEN_text))

                                tb = TextBlob(unEN_text)
                                tb=tb.translate(to='en')
                            except BaseException:
                                continue
                            else:
                                if len(str(tb))>=3:
                                    if tb.detect_language() != 'en':
                                        pass
                                    else:
                                       sentence_polarity =  tb.polarity
                                       sentence_subjectivity  = tb.subjectivity
                                       en_string = re.sub(r"[^\w']", " ", str(tb))
                                       en_string = re.sub(r"[\s]+", ' ', en_string)
                                       en_string = en_string.strip()
                                       process_result = emojiClass(en_string,emoji_count,emoticon_count,sentence_polarity
                                                                   ,sentence_subjectivity)

                                       self.Jsonloads(tweet_dict,json_data,'diff_lang',process_result)
            count+=1
            print("Current: count=%d"%(count))
            pd.DataFrame(tweet_dict).to_csv(csv_file)

    def Jsonloads(self,tweet_dict,json_data,type,unEn_class):

        tweet_createAT = json_data['created_at']
        tweet_reweet = int(json_data['retweet_count'])
        tweet_favorite = int(json_data['favorite_count'])
        tweet_mention = len(json_data['entities']['user_mentions'])
        user_follower = int(json_data['user']['followers_count'])
        user_friend = int(json_data['user']['friends_count'])
        user_favourites = int(json_data['user']['favourites_count'])
        user_listed = int(json_data['user']['listed_count'])
        tweet_statues = int(json_data['user']['statuses_count'])
        tweet_bg_color = json_data['user']['profile_background_color']
        tweet_link_color = json_data['user']['profile_link_color']
        tweet_sb_border_color = json_data['user']['profile_sidebar_border_color']
        tweet_sb_fill_color = json_data['user']['profile_sidebar_fill_color']
        tweet_text_color = json_data['user']['profile_text_color']
        tweet_quote_status = json_data['is_quote_status']
        tweet_truncated = json_data['truncated']
        if type=='en':
            tweet_text = regular_express(json_data['text'])
            emoji_class = process_emoji(tweet_text)
            tweet_text = emoji_class.newText
            tweet_emoji = emoji_class.emoji_count
            tweet_emoticon = emoji_class.emoticon_count
            tweet_polarity = emoji_class.sen_polarity
            tweet_subjectivity = emoji_class.sen_subjectivity
        elif type=='diff_lang':
            tweet_text = unEn_class.newText
            tweet_emoji = unEn_class.emoji_count
            tweet_emoticon = unEn_class.emoticon_count
            tweet_polarity = unEn_class.sen_polarity
            tweet_subjectivity = unEn_class.sen_subjectivity

        '''Remove number and stop words

        
        tweet_text =re.sub(r'[\d]+',' number ',tweet_text)
        tweet_text =re.sub(r"[\s]+", ' ', tweet_text)
        tweet_text = tweet_text.strip()

        stem_text = Stemming(tweet_text)
        lemma_text = lemmatize_sentence(tweet_text)
        '''

        '''Store in dict'''
        tweet_dict['created_at'].append(tweet_createAT)
        tweet_dict['text'].append(tweet_text)
        tweet_dict['en'].append(json_data['lang'])
        tweet_dict['retweet_count'].append(tweet_reweet)
        tweet_dict['favorite_count'].append(tweet_favorite)
        tweet_dict['mention_count'].append(tweet_mention)
        tweet_dict['followers_count'].append(user_follower)
        tweet_dict['friends_count'].append(user_friend)
        tweet_dict['total_favourites_count'].append(user_favourites)
        tweet_dict['listed_count'].append(user_listed)
        tweet_dict['emoji_count'].append(tweet_emoji)
        tweet_dict['emoticon_count'].append(tweet_emoticon)
        tweet_dict['polarity'].append(tweet_polarity)
        tweet_dict['subjectity'].append(tweet_subjectivity)
        tweet_dict['statues_count'].append(tweet_statues)
        tweet_dict['background_color'].append(tweet_bg_color)
        tweet_dict['link_color'].append(tweet_link_color)
        tweet_dict['sidebar_border_color'].append(tweet_sb_border_color)
        tweet_dict['sidebar_fill_color'].append(tweet_sb_fill_color)
        tweet_dict['text_color'].append(tweet_text_color)

        tweet_dict['is_quote_status'].append(tweet_quote_status)
        tweet_dict['truncated'].append(tweet_truncated)







if __name__ == '__main__':
    pos_path = "/home/lt228/Desktop/tweet/positive"
    neg_path = "/home/lt228/Desktop/tweet/negative"
    positive = HandleClass(pos_path)
    json_path = []
    path = positive.get_py(pos_path,json_path)

    positive.ParseJson()
    print("Dealing with positive files successfully!")
    negtive = HandleClass(neg_path)
    negtive.ParseJson()
    print("Dealing with negative files successfully!")




