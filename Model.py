class Tweet:

    def __init__(self,time,pos_words,neg_words,emojis,emoticons,retweet_count,favorite_count,metion_count,follower_count_user,friend_count_user,favorite_count_user,listed_count_user):
        ##Each tweet
        self.time = time
        self.pos_words = pos_words
        self.neg_words = neg_words
        self.emojis = emojis
        self.emoticons = emoticons
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count

        self.mention_count = metion_count
        ##User
        self.follower_count_user = follower_count_user
        self.friend_count_user = friend_count_user
        self.favorite_count_user = favorite_count_user
        self.listed_count_user = listed_count_user





