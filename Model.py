class Tweet:

    def __init__(self,time,pos_words,neg_words,emojis,emoticons,retweet_count,
                 favorite_count,listed_count,metion_count,follower_count_user,
                 friend_count_user,total_favorite,total_posts):
        ##Each tweet
        self.time = time
        self.pos_words = pos_words
        self.neg_words = neg_words
        self.emojis = emojis
        self.emoticons = emoticons
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.listed_count = listed_count
        self.mention_count = metion_count
        ##User
        self.follower_count_user = follower_count_user
        self.friend_count_user = friend_count_user
        self.total_favorite = total_favorite
        self.total_posts = total_posts






