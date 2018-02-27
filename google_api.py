from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import extract_features
import os
import ast
import csv
def GOOGLE_API(file,polarity,number):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    pos_count =0
    neg_count =0
    with open(file,'r',encoding='utf-8',errors='ignore') as f:
        txt=ast.literal_eval(f.read())
        for tweet in txt:
            try:
                document = types.Document(
                    content=tweet,
                    type=enums.Document.Type.PLAIN_TEXT)

                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                if sentiment.score>=0:
                    pos_count+=1
                elif sentiment.score<0:
                    neg_count+=1
            except BaseException:
                pass
            continue
    result='No'
    if pos_count<neg_count and polarity=='depressed':
        result="YES"
    elif neg_count<=pos_count and polarity=='common':
        result="YES"
    output ="%d %s: pos_count=%d   neg_count=%d   result=%s"%(number,polarity,pos_count,neg_count,result)
    print(output)
    return output

        ##print('Text: {}'.format(text))
        ##print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


if __name__ == '__main__':

    pos_path = extract_features.get_txt("/home/charles/tool/Depression_detection/tweet-ubuntu/positive-depressed/txt")
    neg_path = extract_features.get_txt("/home/charles/tool/Depression_detection/tweet-ubuntu/negative-undepressed/txt")
    ##Mac address
    ''' 
    pos_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/positive-depressed/txt")
    neg_path = get_txt("/Users/charles_tong/Desktop/Depression-detection/tweet-ubuntu/negative-undepressed/txt")
    '''

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/charles/tool/google-key.json"
    save_path ="/home/charles/tool/Depression_detection/API_result.csv"
    for pos_txt in pos_path:

        pos_result=GOOGLE_API(pos_txt,'depressed',(pos_path.index(pos_txt)+1))
        combinWithpath=pos_result+"\n"
        print(pos_txt)
        with open(save_path,"a") as f:
            f.write(combinWithpath)
    for neg_txt in neg_path:

        neg_result=GOOGLE_API(neg_txt,'common',(neg_path.index(neg_txt)+1))
        combinWithpath = neg_result + "\n"
        print(neg_txt)
        with open(save_path,"a",encoding="utf-8",errors="ignore") as f:
            f.write(combinWithpath)


