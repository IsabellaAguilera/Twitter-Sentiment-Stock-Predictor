import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import datetime
import pandas as pd
import stock_data

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'N0EyJWCQ9AAAEBO0FfumQnfe6'
        consumer_secret = '78ehOmcz9sQMCADWDKO5Hm48pksuE4EujHu6zOFFNl0hHKHyI3'
        access_token = '106210504-hthpR2CQ8yWInGhtdYH8KCGGNEyniHg4zxSJJxfg'
        access_token_secret = 'MrN1vw0c6Nylh90TwtmD8OXnsgk1z7l5HUYdCkSTVd8GB'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 100, max_id = None): #"1217210436359376890"
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count, max_id = max_id) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                if not tweet.retweeted:
                    parsed_tweet = {} 

                    # saving text of tweet 
                    parsed_tweet['text'] = tweet.text 
                    parsed_tweet['date'] = tweet.created_at
                    parsed_tweet['id'] = tweet.id
                    # saving sentiment of tweet 
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                    # appending parsed tweet to tweets list 
                    if tweet.retweet_count > 0: 
                        # if tweet has retweets, ensure that it is appended only once 
                        if parsed_tweet not in tweets: 
                            tweets.append(parsed_tweet) 
                    else: 
                        tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

def scores_dict():
    today = datetime.date.today()

    scores = {}

    day = {'positive':0, 'negative':0, 'neutral':0}
    scores[str(today)] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 1))] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 2))] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 3))] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 4))] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 5))] = [0,0,0]
    scores[str(today - datetime.timedelta(days = 6))] = [0,0,0]
    
    return scores

def search_scores(query):
    api = TwitterClient()
    loop = 0
    max_id = None
    
    # approximate 1 hour ID 
    #partition = 17750122401798
    # approximate 8 hour ID increment
    
    partition = 142000979214384
    scores = scores_dict()
    today = datetime.date.today()
    last_day = str(today - datetime.timedelta(days = 6))
    while loop < 2:
        tweets = api.get_tweets(query = query, count = 100, max_id = max_id)
#         print(tweets)
#         print("/n/n/n/n")
        if (len(tweets) == 0):
            break
        last_tweet = tweets[len(tweets) - 1]
        max_id = str(last_tweet['id'] - partition)
        count = 0
        for tweet in tweets:
            try:
                sentiment = tweet['sentiment']
#                 print(sentiment)
                day_key = str(tweet['date'].date())
                if day_key == last_day:
                    if count == 0:
                        count = 1
                        loop += 1
                elif day_key < last_day:
                    loop = 2
                    break
                if sentiment == 'positive':
                    scores[day_key][0] += 1
                elif sentiment == 'negative':
                    scores[day_key][1] += 1
                elif sentiment == 'neutral':
                    scores[day_key][2] += 1
            except:
                continue
                #print(tweet)
        #print(scores)
    return scores

def score_stats(scores):
    stats = {}
    for key in scores:
        stats[key] = {}
        total = scores[key][0] + scores[key][1] + scores[key][2]
        if total == 0:
            stats[key]['positive'] = 0
            stats[key]['negative'] = 0
            stats[key]['total'] = 0
            continue
        stats[key]['positive'] = scores[key][0]/total
        stats[key]['negative'] = scores[key][1]/total
        stats[key]['total'] = total
    stat_df = pd.DataFrame.from_dict(stats).T
    stat_df.reset_index(inplace = True)
    stat_df.sort_values(by = 'index', inplace = True)
    stat_df.rename(columns = {'index':'Date'}, inplace = True)
    return stat_df

def search_predict(query):
    api = TwitterClient()
    max_id = None
    partition = 142000979214384
    today = str(datetime.date.today())
    scores = {today:[0,0,0]}
    
    for i in range(3):
        tweets = api.get_tweets(query = query, count = 100, max_id = max_id)
        if (len(tweets) == 0):
            break

        last_tweet = tweets[len(tweets) - 1]

        max_id = str(last_tweet['id'] - partition)
        
        for tweet in tweets:
            try:
                sentiment = tweet['sentiment']
                if sentiment == 'positive':
                    scores[today][0] += 1
                elif sentiment == 'negative':
                    scores[today][1] += 1
                elif sentiment == 'neutral':
                    scores[today][2] += 1
            except:
                continue
    return scores
    
    
def data_creator_predict(company):
    if not stock_data.is_valid_company(company):
        print("Not a valid company")
        return None
    search_results = search_predict(company)
    scores = score_stats(search_results)
    stock_prices = stock_data.find_ticker_data(company)
    stock = stock_data.up_down(stock_prices)
    stock['Date'] = stock['Date'].astype('str')
    total_df = scores.merge(stock, how = 'inner', on = 'Date')
    total_df = total_df[['negative', 'positive', 'total','Price Change']]
    final = pd.get_dummies(total_df)
    return final

def data_creator_binary(list_of_companies):
    final_data = pd.DataFrame()
    count = 0
    for company in list_of_companies:
        if not stock_data.is_valid_company(company):
            continue
        search_results = search_scores(company)
        scores = score_stats(search_results)
        stock_prices = stock_data.find_ticker_data(company)
        stock = stock_data.up_down(stock_prices)
        stock['Date'] = stock['Date'].astype('str')
        total_df = scores.merge(stock, how = 'inner', on = 'Date')
        if count == 0:
            final_data = total_df
            count = 1
        else:
            #print(total_df)
            final_data = pd.concat([final_data,total_df])
    final_df = final_data[['negative', 'positive', 'total','Price Change']]
    final = pd.get_dummies(final_df)
    return final

if __name__ == '__main__':
    pass