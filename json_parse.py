#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:11:38 2017

@author: charles
"""
import os
import os.path
import json
import ast
import re
import csv
import pandas as pd
from Model import Tweet
from text_preprocess import *


def regular_express(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet



class HandleClass:
    def __init__(self,path):
        self.__path = path
        
    def __get_py(self,path,json_path):
        fileList = os.listdir(path)
        for filename in fileList:
            file_path = os.path.join(path,filename)
            if os.path.isdir(file_path):
                self.__get_py(file_path,json_path)
            elif filename[-5:].upper()=='.JSON':
                json_path.append(file_path)              
        return json_path


    def ParseJson(self):
        json_path=[]
        json_path = self.__get_py(self.__path,json_path)
        print(len(json_path))
        count = 0
        for json_file in json_path:

            tweet_dict = {'created_at': [], 'text': [], 'retweet_count': [], 'favorite_count': [],
                          'lang': [], 'mention_count': [], 'followers_count': [], 'friends_count': []
                , 'total_favourites_count': [], 'listed_count': [],'emoji_count': [],'emoticon_count': []}

            filename = json_file.split("/")[-1]
            filename = filename[:-5] + '.csv'
            csv_file = os.path.join(self.__path, "csv", filename)
            with open(json_file,'r',encoding="utf-8",errors="ignore") as f:

                for line in f:
                    json_data = json.loads(line)
                    tweet_createAT  = json_data['created_at']
                    tweet_text = regular_express(json_data['text'])
                    tweet_reweet  = int(json_data['retweet_count'])
                    tweet_favorite = int(json_data['favorite_count'])
                    tweet_lang = json_data['lang']
                    tweet_mention = len(json_data['entities']['user_mentions'])

                    user_follower = int(json_data['user']['followers_count'])
                    user_friend = int(json_data['user']['friends_count'])
                    user_favourites = int(json_data['user']['favourites_count'])
                    user_listed = int(json_data['user']['listed_count'])

                    if tweet_lang =='en':

                        tweet_dict['created_at'].append(tweet_createAT)

                        emoji_class = process_emoji(tweet_text)
                        tweet_text = emoji_class.newText
                        tweet_text = Stemming(tweet_text)
                        tweet_dict['text'].append(tweet_text)


                        tweet_dict['retweet_count'].append(tweet_reweet)
                        tweet_dict['favorite_count'].append(tweet_favorite)
                        tweet_dict['lang'].append(tweet_lang)
                        tweet_dict['mention_count'].append(tweet_mention)
                        tweet_dict['followers_count'].append(user_follower)
                        tweet_dict['friends_count'].append(user_friend)
                        tweet_dict['total_favourites_count'].append(user_favourites)
                        tweet_dict['listed_count'].append(user_listed)
                        tweet_dict['emoji_count'].append(emoji_class.emoji_count)
                        tweet_dict['emoticon_count'].append(emoji_class.emoticon_count)


                    else:
                        pass
                        continue

            count+=1
            print("Current: count=%d"%(count))

            pd.DataFrame(tweet_dict).to_csv(csv_file)


        


if __name__ == '__main__':
    pos_path = "/Users/charles_tong/Desktop/tweet/positive"
    neg_path = "/Users/charles_tong/Desktop/tweet/negative"
    positive = HandleClass(pos_path)
    positive.ParseJson()
    print("Dealing with positive files successfully!")
    negtive = HandleClass(neg_path)
    negtive.ParseJson()
    print("Dealing with negative files successfully!")

    ''' 
    path = "/home/charles/tool/tweet-ubuntu/positive-depressed/txt/_JasmineRakhracreated_at-907409179.txt"
    with open(path,'r',encoding="utf-8",errors="ignore") as f:
        data = ast.literal_eval(f.read())
        print(len(data))
    '''
        
    
    