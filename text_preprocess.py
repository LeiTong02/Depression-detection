'''1. emoji processing'''
import emot
import re
from nltk.stem.snowball import SnowballStemmer
import nltk
from nltk import TweetTokenizer

from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

tokenizer = TweetTokenizer()
class emojiClass:

    def __init__(self,newText,emoji_count,emoticon_count,sen_polarity,sen_subjectivity):
        self.newText = newText
        self.emoji_count = emoji_count
        self.emoticon_count = emoticon_count
        self.sen_polarity  = sen_polarity
        self.sen_subjectivity = sen_subjectivity
def process_emoji(tweets):
    ##stop_words = get_stop_words("en")

    emoji_count = len(emot.emoji(tweets))
    emoticon_count = len(emot.emoticons(tweets))

    '''remove stop-words
    text_token = tokenizer.tokenize(tweets)
    non_stop_token = [word for word in text_token if word not in stop_words]
    non_stop_text = " ".join(non_stop_token)
    '''

    '''remove non-ascii letters'''

    new_string = re.sub(r"[^\w']", " ", tweets)
    new_string = re.sub(r"[\s]+", ' ', new_string)
    new_string = new_string.strip()

    '''Textblob: Spell correction and analysis polarity'''
    text_blob = TextBlob(new_string)
    correct_string = str(text_blob.correct())

    polarity = text_blob.sentiment.polarity
    subjectity = text_blob.sentiment.subjectivity
    emoji_result= emojiClass(correct_string,emoji_count,emoticon_count,polarity,subjectity)

    return emoji_result

'''2. Steming'''
def Stemming(tweets):
    stemmer = SnowballStemmer("english")
    word_list  = nltk.word_tokenize(tweets)
    stem_result = [stemmer.stem(word) for word in word_list]
    new_string = " ".join(stem_result)
    return new_string


'''Regular express for specifying word polarity'''
def regular_express(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub(r'(rt @[^\s]+)|(^rt [^\s]+)|(@[^\s]+)', ' ', tweet)

    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip()
    return tweet

'''Lemmatize sentence'''
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    res = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    res = " ".join(res)
    return res



