'''1. emoji processing'''
import emot
import re
from nltk.stem.snowball import SnowballStemmer
import nltk
class emojiClass:
    def __init__(self,newText,emoji_count,emoticon_count):
        self.newText = newText
        self.emoji_count = emoji_count
        self.emoticon_count = emoticon_count
def process_emoji(tweets):
    emoji_count = len(emot.emoji(tweets))
    emoticon_count = len(emot.emoticons(tweets))

    new_string = re.sub(r"[^\w']"," ",tweets)
    new_string = re.sub(r"[\s]+",' ',new_string)
    new_string = new_string.strip(" ")
    emoji_result= emojiClass(new_string,emoji_count,emoticon_count)

    return emoji_result

'''2. Steming'''
def Stemming(tweets):
    stemmer = SnowballStemmer("english")
    word_list  = nltk.word_tokenize(tweets)
    stem_result = [stemmer.stem(word) for word in word_list]
    new_string = " ".join(stem_result)
    return new_string



