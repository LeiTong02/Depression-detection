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
    text_blob = text_blob.correct()
    correct_string  = str(text_blob)
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
    tweet = re.sub(r'(rt @[^\s]+)', 'response', tweet)
    # Remove @username
    tweet = re.sub(r'(@[^\s]+)',' ',tweet)

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
# remove url response number and stop words

def remove_unlessword(tweet):
    tweet = re.sub(r'URL',' ',tweet)
    tweet = re.sub(r'^response',' ',tweet)
    tweet = re.sub(r'[\d]+', ' number ', tweet)
    tweet = re.sub(r"[\s]+", ' ', tweet)
    tweet = tweet.strip()
    ## stop words processing
    long_stop_list = ["a", "a's", "abaft", "able", "aboard", "about", "above", "abst", "accordance", "according",
                      "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects",
                      "afore", "aforesaid", "after", "afterwards", "again", "against", "agin", "ago", "ah", "ain't",
                      "aint", "albeit", "all", "allow", "allows", "almost", "alone", "along", "alongside", "already",
                      "also", "although", "always", "am", "american", "amid", "amidst", "among", "amongst", "an", "and",
                      "anent", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything",
                      "anyway", "anyways", "anywhere", "apart", "apparently", "appear", "appreciate", "appropriate",
                      "approximately", "are", "aren", "aren't", "arent", "arise", "around", "as", "aside", "ask",
                      "asking", "aslant", "associated", "astride", "at", "athwart", "auth", "available", "away",
                      "awfully", "b", "back", "bar", "barring", "be", "became", "because", "become", "becomes",
                      "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins",
                      "behind", "being", "believe", "below", "beneath", "beside", "besides", "best", "better",
                      "between", "betwixt", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "c'mon",
                      "c's", "ca", "came", "can", "can't", "cannot", "cant", "cause", "causes", "certain", "certainly",
                      "changes", "circa", "clearly", "close", "co", "com", "come", "comes", "concerning",
                      "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding",
                      "cos", "could", "couldn", "couldn't", "couldnt", "couldst", "course", "currently", "d", "dare",
                      "dared", "daren", "dares", "daring", "date", "definitely", "described", "despite", "did", "didn",
                      "didn't", "different", "directly", "do", "does", "doesn", "doesn't", "doing", "don", "don't",
                      "done", "dost", "doth", "down", "downwards", "due", "during", "durst", "e", "each", "early", "ed",
                      "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "em", "end", "ending",
                      "english", "enough", "entirely", "er", "ere", "especially", "et", "et-al", "etc", "even", "ever",
                      "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example",
                      "except", "excepting", "f", "failing", "far", "few", "ff", "fifth", "first", "five", "fix",
                      "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from",
                      "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives",
                      "giving", "go", "goes", "going", "gone", "gonna", "got", "gotta", "gotten", "greetings", "h",
                      "had", "hadn", "hadn't", "happens", "hard", "hardly", "has", "hasn", "hasn't", "hast", "hath",
                      "have", "haven", "haven't", "having", "he", "he'd", "he'll", "he's", "hed", "hello", "help",
                      "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "heres", "hereupon", "hers",
                      "herself", "hes", "hi", "hid", "high", "him", "himself", "his", "hither", "home", "hopefully",
                      "how", "how's", "howbeit", "however", "hundred", "i", "i'd", "i'll", "i'm", "i've", "id", "ie",
                      "if", "ignored", "ill", "im", "immediate", "immediately", "importance", "important", "in",
                      "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information",
                      "inner", "inside", "insofar", "instantly", "instead", "into", "invention", "inward", "is", "isn",
                      "isn't", "it", "it'd", "it'll", "it's", "itd", "its", "itself", "j", "just", "k", "keep", "keeps",
                      "kept", "kg", "km", "know", "known", "knows", "l", "large", "largely", "last", "lately", "later",
                      "latter", "latterly", "least", "left", "less", "lest", "let", "let's", "lets", "like", "liked",
                      "likely", "likewise", "line", "little", "living", "ll", "long", "look", "looking", "looks", "ltd",
                      "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn", "me", "mean", "means",
                      "meantime", "meanwhile", "merely", "mg", "mid", "midst", "might", "mightn", "million", "mine",
                      "minus", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must",
                      "mustn", "mustn't", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly",
                      "neath", "necessarily", "necessary", "need", "needed", "needing", "needn", "needs", "neither",
                      "never", "nevertheless", "new", "next", "nigh", "nigher", "nighest", "nine", "ninety", "nisi",
                      "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted",
                      "nothing", "notwithstanding", "novel", "now", "nowhere", "o", "obtain", "obtained", "obviously",
                      "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones",
                      "oneself", "only", "onto", "open", "or", "ord", "other", "others", "otherwise", "ought", "oughtn",
                      "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page",
                      "pages", "part", "particular", "particularly", "past", "pending", "per", "perhaps", "placed",
                      "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly",
                      "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provided",
                      "provides", "providing", "public", "put", "q", "qua", "que", "quickly", "quite", "qv", "r", "ran",
                      "rather", "rd", "re", "readily", "real", "really", "reasonably", "recent", "recently", "ref",
                      "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respecting",
                      "respectively", "resulted", "resulting", "results", "right", "round", "run", "s", "said", "same",
                      "sans", "save", "saving", "saw", "say", "saying", "says", "sec", "second", "secondly", "section",
                      "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible",
                      "sent", "serious", "seriously", "seven", "several", "shall", "shalt", "shan", "shan't", "she",
                      "she'd", "she'll", "she's", "shed", "shell", "shes", "short", "should", "shouldn", "shouldn't",
                      "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar",
                      "similarly", "since", "six", "slightly", "small", "so", "some", "somebody", "somehow", "someone",
                      "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
                      "special", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly",
                      "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "summat", "sup",
                      "supposing", "sure", "t", "t's", "take", "taken", "taking", "tell", "tends", "th", "than",
                      "thank", "thanks", "thanx", "that", "that'll", "that's", "that've", "thats", "the", "thee",
                      "their", "theirs", "them", "themselves", "then", "thence", "there", "there'll", "there's",
                      "there've", "thereafter", "thereby", "thered", "therefore", "therein", "thereof", "therere",
                      "theres", "thereto", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've",
                      "theyd", "theyre", "thine", "think", "third", "this", "tho", "thorough", "thoroughly", "those",
                      "thou", "though", "thoughh", "thousand", "three", "thro", "throug", "through", "throughout",
                      "thru", "thus", "thyself", "til", "till", "tip", "to", "today", "together", "too", "took",
                      "touching", "toward", "towards", "tried", "tries", "true", "truly", "try", "trying", "ts", "twas",
                      "tween", "twere", "twice", "twill", "twixt", "two", "twould", "u", "un", "under", "underneath",
                      "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us",
                      "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value",
                      "various", "ve", "versus", "very", "via", "vice", "vis-a-vis", "viz", "vol", "vols", "vs", "w",
                      "wanna", "want", "wanting", "wants", "was", "wasn", "wasn't", "wasnt", "way", "we", "we'd",
                      "we'll", "we're", "we've", "wed", "welcome", "well", "went", "were", "weren", "weren't", "werent",
                      "wert", "what", "what'll", "what's", "whatever", "whats", "when", "when's", "whence",
                      "whencesoever", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein",
                      "wheres", "whereupon", "wherever", "whether", "which", "whichever", "whichsoever", "while",
                      "whilst", "whim", "whither", "who", "who'll", "who's", "whod", "whoever", "whole", "whom",
                      "whomever", "whore", "whos", "whose", "whoso", "whosoever", "why", "why's", "widely", "will",
                      "willing", "wish", "with", "within", "without", "won't", "wonder", "wont", "words", "world",
                      "would", "wouldn", "wouldn't", "wouldnt", "wouldst", "www", "x", "y", "ye", "yes", "yet", "you",
                      "you'd", "you'll", "you're", "you've", "youd", "your", "youre", "yours", "yourself", "yourselves",
                      "z", "zero"]
    text_token = tokenizer.tokenize(tweet)
    non_stop_token = [word for word in text_token if word not in long_stop_list]

    return non_stop_token








