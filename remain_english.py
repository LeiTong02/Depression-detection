import nltk
import  ast
def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)
def open_file(path):
    count = 0
    with open(path,'r',encoding="utf-8",errors="ignore") as f:
        txt = ast.literal_eval(f.read().lower())
        for tweet in txt[(len(txt)-3):len(txt)]:
            tweet = nltk.word_tokenize(tweet)
            english = 0
            nand_english = 0
            for word in tweet:
                if judge_pure_english(word):
                    english+=1
                else:
                    nand_english += 1
            if nand_english>=english:
                count+=1
    filename = path.split("/")[-1]
    if count>=2:
        print("Wrong language: %s"%(filename))



from extract_keywords import get_txt
if __name__ == '__main__':
    pos_path = "/Users/charles_tong/Desktop/tweet/positive/txt"
    neg_path = "/Users/charles_tong/Desktop/tweet/negative/txt"

    for pos_txt_path in get_txt(pos_path):
        open_file(pos_txt_path)
    print("positive finished")
    for neg_txt_path in get_txt(neg_path):
        open_file(neg_txt_path)
    print("negative finished")
