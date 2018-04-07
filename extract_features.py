import nltk;
from nltk.corpus import sentiwordnet as swn
import pandas as pd
import time
import os;
from Model import Tweet


def get_csv(path):
    txt_path=[]

    fileList = os.listdir(path)
    for filename in fileList:
        file_path = os.path.join(path, filename)
        if filename[-4:].upper() == '.CSV':
            txt_path.append(file_path)
    return txt_path

def extract_csv(path):
    csv = pd.read_csv(path)
    if csv.shape[0] <= 5:
        pass
    else:
        rows = csv.shape[0]
        emojis = sum(csv.emoji_count) / rows
        emoticons = sum(csv.emoticon_count) / rows
        favorites = sum(csv.favorite_count) / rows
        followers = sum(csv.followers_count) / rows
        friends_count = sum(csv.friends_count) / rows
        listed_count = sum(csv.listed_count) / rows
        mention_count = sum(csv.mention_count) / rows
        retweet_count = sum(csv.retweet_count) / rows
        total_favourites_count = sum(csv.total_favourites_count) / rows

        '''Count the number of posting between 22:00 and 5:00'''
        time_Series = csv.created_at
        nightTime_count = 0
        for time_row in time_Series:
            time_struct = time.strptime(time_row, "%a %b %d %H:%M:%S +0000 %Y")
            HMS = int(time.strftime("%H%M%S", time_struct))
            if HMS <= 60000 or HMS >= 230000:
                nightTime_count += 1
        nightTime_count = nightTime_count / rows
        text_Series = csv.text
        pos_words = 0
        neg_words = 0
        '''Should modify here for specifying word class'''
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
        tweet_class = Tweet(nightTime_count, pos_words, neg_words, emojis, emoticons
                            , retweet_count, favorites, listed_count, mention_count, followers
                            , friends_count, total_favourites_count, rows)
        return tweet_class


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


if __name__=='__main__':
    ##Linux address /home/charles/tool/Depression_detection/tweet-ubuntu/negative-undepressed/txt
    pos_path = get_csv("/Users/charles_tong/Desktop/tweet/positive/csv")
    neg_path = get_csv("/Users/charles_tong/Desktop/tweet/negative/csv")

    pos_dict = {"nightTime_count": [], "pos_words": [], "neg_words": [], "emojis": [],
                "emoticons": [], "retweet_count": [], "favorites": [], "listed_count": [],
                "mention_count": [], "followers": [], "friends_count": [],
                "total_favourites_count": [], "total_post": []}
    neg_dict = {"nightTime_count": [], "pos_words": [], "neg_words": [], "emojis": [],
                "emoticons": [], "retweet_count": [], "favorites": [], "listed_count": [],
                "mention_count": [], "followers": [], "friends_count": [],
                "total_favourites_count": [], "total_post": []}

    for pos_csv in pos_path:
        tweet= extract_csv(pos_csv)
        if tweet:
            pos_dict["nightTime_count"].append(tweet.time)
            pos_dict["pos_words"].append(tweet.pos_words)
            pos_dict["neg_words"].append(tweet.neg_words)
            pos_dict["emojis"].append(tweet.emojis)
            pos_dict["emoticons"].append(tweet.emoticons)
            pos_dict["retweet_count"].append(tweet.retweet_count)
            pos_dict["favorites"].append(tweet.favorite_count)
            pos_dict["listed_count"].append(tweet.listed_count)
            pos_dict["mention_count"].append(tweet.mention_count)
            pos_dict["followers"].append(tweet.follower_count_user)
            pos_dict["friends_count"].append(tweet.friend_count_user)
            pos_dict["total_favourites_count"].append(tweet.total_favorite)
            pos_dict["total_post"].append(tweet.total_posts)

            print(pos_path.index(pos_csv))
    save_model("positive_model",pos_dict)
    print("Positive model generated")


    for neg_csv in neg_path:
        tweet = extract_csv(neg_csv)
        if tweet:
            neg_dict["nightTime_count"].append(tweet.time)
            neg_dict["pos_words"].append(tweet.pos_words)
            neg_dict["neg_words"].append(tweet.neg_words)
            neg_dict["emojis"].append(tweet.emojis)
            neg_dict["emoticons"].append(tweet.emoticons)
            neg_dict["retweet_count"].append(tweet.retweet_count)
            neg_dict["favorites"].append(tweet.favorite_count)
            neg_dict["listed_count"].append(tweet.listed_count)
            neg_dict["mention_count"].append(tweet.mention_count)
            neg_dict["followers"].append(tweet.follower_count_user)
            neg_dict["friends_count"].append(tweet.friend_count_user)
            neg_dict["total_favourites_count"].append(tweet.total_favorite)
            neg_dict["total_post"].append(tweet.total_posts)

            print(neg_path.index(neg_csv))

    save_model("negative_model", neg_dict)
    print("Negative model generated")



