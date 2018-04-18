class Social_network_feature:
    '''day_time_ratio": [],'night_time_ratio':[],'time_distribution':[],  "emojis": [],
                "emoticons": [], "retweet_count": [], "favorite": [], "listed_count": [],
                "mention_count": [], "followers": [], "friends_count": [],
                "favourites_count": [], "posts": [],'quote_count':[],'statues_count':[],'text_length':[],'RT_ratio':[],
                'links':[],'polarity':[],'subjectivity':[],'truncated':[]'''
    def __init__(self,day_time_ratio,night_time_ratio,time_distribution,emojis,emoticons,retweet_count,
                 favorite,listed_count,mention_count,followers,
                 friends,favorites,posts,quote_count,statues_count,text_length,RT_ratio,links,polarity
                 ,subjectivity,truncated_count):
        self.day_time_ratio = day_time_ratio
        self.night_time_ratio = night_time_ratio
        self.time_distribution  = time_distribution

        self.emojis = emojis
        self.emoticons = emoticons
        self.retweet_count = retweet_count
        self.favorite = favorite
        self.favorites = favorites
        self.listed_count = listed_count
        self.mention_count = mention_count
        self.followers = followers
        self.friends = friends
        self.posts = posts
        self.quote_count = quote_count
        self.statues_count  = statues_count
        self.text_length = text_length
        self.RT_ratio = RT_ratio
        self.links = links
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.truncated_count = truncated_count








