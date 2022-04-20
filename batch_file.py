#code written by teammate
import snscrape.modules.twitter as sntwitter
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vanderSentimentAnalyzer = SentimentIntensityAnalyzer()
from datetime import date,timedelta                        
import random  
import re                     
import string

all_dates = []
start = date.today()-timedelta(days = 7)
for i in range(0,8):
    all_dates.append((start+timedelta(days = i)).strftime("%Y-%m-%d"))

def remove_special_character(tweet):
#     print(tweet)
    # remove the old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

    # remove hashtags. only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)

    # remove single numeric terms in the tweet. 
    tweet = re.sub(r'[0-9]', '', tweet)
    
    return tweet

def getVanderScore(tweet):    
    vs = vanderSentimentAnalyzer.polarity_scores(tweet)
    score = vs['compound']
    return score




engagement_threshold = 40

#apple
apple_tweet_list = []

for m in range(0,7):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('AAPL since:{start_date} until:{end} lang:"en"'.format(start_date = all_dates[m],end=all_dates[m+1])).get_items()):
        if i>500:
            break
        apple_tweet_list.append([tweet.date, tweet.content,tweet.retweetCount,tweet.likeCount,tweet.replyCount])


apple_df = pd.DataFrame(apple_tweet_list, columns=['Datetime', 'Text','retweet','like','comment'])    
        

apple_df["total_engangement"] = apple_df["comment"] + apple_df["retweet"] + apple_df["like"]
apple_df = apple_df[apple_df["total_engangement"] > engagement_threshold]
apple_df['Datetime'] = pd.to_datetime(apple_df['Datetime'].apply(lambda date: date.date()))
apple_df["Text"] = apple_df["Text"].apply(lambda tweet: remove_special_character(tweet))
apple_df["Text"] = apple_df["Text"].str.lower()
apple_df['vander_score'] = apple_df['Text'].apply(lambda tweet: getVanderScore(tweet))


average_vander_score = []
for i in all_dates[:-1]:
    sum_engagement = 0
    temp_vander_sum = 0
    options = apple_df[apple_df.Datetime==i]
    if len(options)==0:
        average_vander_score.append(0)
    else:
        for index, row in options.iterrows():
            sum_engagement = sum_engagement+row.total_engangement
        for index, row in options.iterrows():
            temp_vander_sum = temp_vander_sum+ (row.vander_score*(row.total_engangement/sum_engagement))
        average_vander_score.append(temp_vander_sum/len(options))

apple_final_df = pd.DataFrame(average_vander_score,columns=['Score'])
apple_final_df.to_csv("./data/sentiment data/"+all_dates[-1] + "_AAPL.csv")
print('apple done')


#tesla
tesla_tweet_list = []

for m in range(0,7):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('TSLA since:{start_date} until:{end} lang:"en"'.format(start_date = all_dates[m],end=all_dates[m+1])).get_items()):
        if i>500:
            break
        tesla_tweet_list.append([tweet.date, tweet.content,tweet.retweetCount,tweet.likeCount,tweet.replyCount])


tesla_df = pd.DataFrame(tesla_tweet_list, columns=['Datetime', 'Text','retweet','like','comment'])    
        

tesla_df["total_engangement"] = tesla_df["comment"] + tesla_df["retweet"] + tesla_df["like"]
tesla_df = tesla_df[tesla_df["total_engangement"] > engagement_threshold]
tesla_df['Datetime'] = pd.to_datetime(tesla_df['Datetime'].apply(lambda date: date.date()))
tesla_df["Text"] = tesla_df["Text"].apply(lambda tweet: remove_special_character(tweet))
tesla_df["Text"] = tesla_df["Text"].str.lower()
tesla_df['vander_score'] = tesla_df['Text'].apply(lambda tweet: getVanderScore(tweet))


average_vander_score = []
for i in all_dates[:-1]:
    sum_engagement = 0
    temp_vander_sum = 0
    options = tesla_df[tesla_df.Datetime==i]
    if len(options)==0:
        average_vander_score.append(0)
    else:
        for index, row in options.iterrows():
            sum_engagement = sum_engagement+row.total_engangement
        for index, row in options.iterrows():
            temp_vander_sum = temp_vander_sum+ (row.vander_score*(row.total_engangement/sum_engagement))
        average_vander_score.append(temp_vander_sum/len(options))

tesla_final_df = pd.DataFrame(average_vander_score,columns=['Score'])
tesla_final_df.to_csv("./data/sentiment data/"+all_dates[-1] + "_TSLA.csv")
print('tesla done')

#google
google_tweet_list = []

for m in range(0,7):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('GOOG since:{start_date} until:{end} lang:"en"'.format(start_date = all_dates[m],end=all_dates[m+1])).get_items()):
        if i>500:
            break
        google_tweet_list.append([tweet.date, tweet.content,tweet.retweetCount,tweet.likeCount,tweet.replyCount])


google_df = pd.DataFrame(google_tweet_list, columns=['Datetime', 'Text','retweet','like','comment'])    
        

google_df["total_engangement"] = google_df["comment"] + google_df["retweet"] + google_df["like"]
google_df = google_df[google_df["total_engangement"] > engagement_threshold]
google_df['Datetime'] = pd.to_datetime(google_df['Datetime'].apply(lambda date: date.date()))
google_df["Text"] = google_df["Text"].apply(lambda tweet: remove_special_character(tweet))
google_df["Text"] = google_df["Text"].str.lower()
google_df['vander_score'] = google_df['Text'].apply(lambda tweet: getVanderScore(tweet))


average_vander_score = []
for i in all_dates[:-1]:
    sum_engagement = 0
    temp_vander_sum = 0
    options = google_df[google_df.Datetime==i]
    if len(options)==0:
        average_vander_score.append(0)
    else:
        for index, row in options.iterrows():
            sum_engagement = sum_engagement+row.total_engangement
        for index, row in options.iterrows():
            temp_vander_sum = temp_vander_sum+ (row.vander_score*(row.total_engangement/sum_engagement))
        average_vander_score.append(temp_vander_sum/len(options))

google_final_df = pd.DataFrame(average_vander_score,columns=['Score'])
google_final_df.to_csv("./data/sentiment data/"+all_dates[-1] + "_GOOG.csv")
print('google done')


#alphabet
alphabet_tweet_list = []

for m in range(0,7):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('GOOGL since:{start_date} until:{end} lang:"en"'.format(start_date = all_dates[m],end=all_dates[m+1])).get_items()):
        if i>500:
            break
        alphabet_tweet_list.append([tweet.date, tweet.content,tweet.retweetCount,tweet.likeCount,tweet.replyCount])


alphabet_df = pd.DataFrame(alphabet_tweet_list, columns=['Datetime', 'Text','retweet','like','comment'])    
        

alphabet_df["total_engangement"] = alphabet_df["comment"] + alphabet_df["retweet"] + alphabet_df["like"]
alphabet_df = alphabet_df[alphabet_df["total_engangement"] > engagement_threshold]
alphabet_df['Datetime'] = pd.to_datetime(alphabet_df['Datetime'].apply(lambda date: date.date()))
alphabet_df["Text"] = alphabet_df["Text"].apply(lambda tweet: remove_special_character(tweet))
alphabet_df["Text"] = alphabet_df["Text"].str.lower()
alphabet_df['vander_score'] = alphabet_df['Text'].apply(lambda tweet: getVanderScore(tweet))


average_vander_score = []
for i in all_dates[:-1]:
    sum_engagement = 0
    temp_vander_sum = 0
    options = alphabet_df[alphabet_df.Datetime==i]
    if len(options)==0:
        average_vander_score.append(0)
    else:
        for index, row in options.iterrows():
            sum_engagement = sum_engagement+row.total_engangement
        for index, row in options.iterrows():
            temp_vander_sum = temp_vander_sum+ (row.vander_score*(row.total_engangement/sum_engagement))
        average_vander_score.append(temp_vander_sum/len(options))

alphabet_final_df = pd.DataFrame(average_vander_score,columns=['Score'])
alphabet_final_df.to_csv("./data/sentiment data/"+all_dates[-1] + "_GOOGL.csv")
print('alphabet done')

#amazon
amazon_tweet_list = []

for m in range(0,7):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('AMZN since:{start_date} until:{end} lang:"en"'.format(start_date = all_dates[m],end=all_dates[m+1])).get_items()):
        if i>500:
            break
        amazon_tweet_list.append([tweet.date, tweet.content,tweet.retweetCount,tweet.likeCount,tweet.replyCount])


amazon_df = pd.DataFrame(amazon_tweet_list, columns=['Datetime', 'Text','retweet','like','comment'])    
        

amazon_df["total_engangement"] = amazon_df["comment"] + amazon_df["retweet"] + amazon_df["like"]
amazon_df = amazon_df[amazon_df["total_engangement"] > engagement_threshold]
amazon_df['Datetime'] = pd.to_datetime(amazon_df['Datetime'].apply(lambda date: date.date()))
amazon_df["Text"] = amazon_df["Text"].apply(lambda tweet: remove_special_character(tweet))
amazon_df["Text"] = amazon_df["Text"].str.lower()
amazon_df['vander_score'] = amazon_df['Text'].apply(lambda tweet: getVanderScore(tweet))


average_vander_score = []
for i in all_dates[:-1]:
    sum_engagement = 0
    temp_vander_sum = 0
    options = amazon_df[amazon_df.Datetime==i]
    if len(options)==0:
        average_vander_score.append(0)
    else:
        for index, row in options.iterrows():
            sum_engagement = sum_engagement+row.total_engangement
        for index, row in options.iterrows():
            temp_vander_sum = temp_vander_sum+ (row.vander_score*(row.total_engangement/sum_engagement))
        average_vander_score.append(temp_vander_sum/len(options))

amazon_final_df = pd.DataFrame(average_vander_score,columns=['Score'])
amazon_final_df.to_csv("./data/sentiment data/"+all_dates[-1] + "_AMZN.csv")
print('amazon done')