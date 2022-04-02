import tweepy
import random
import time
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

influencer_id_list = ["@takapon_jp", "@hirox246", "@ochyai"]  # ホリエモン、ひろゆき、落合陽一
#ここのid変えるとフォローする対象を変更できる

def create_api(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def favorite_other_account(api, user_id_list):
    influencer_id = random.choice(influencer_id_list)
    followers_id_list = api.followers_ids(influencer_id)
    random.shuffle(followers_id_list)
    for follower_id in followers_id_list[:5]:
        if api.get_user(follower_id).protected == False:
            print(f"TwitterIdが{follower_id}のツイートをいいねします")
            tweets = api.user_timeline(follower_id, count=3)
            for tweet in tweets:
              if (not tweet.retweeted) and (not tweet.favorited) and ('RT @' not in tweet.text):
                  api.create_favorite(tweet.id)
                  time.sleep(random.randint(0, 5))

def get_anhour_before():
    dt_now = datetime.datetime.now()
    anhour_before = dt_now + datetime.timedelta(hours=-0.1)
    anhour_before_day = anhour_before.strftime('%Y-%m-%d')
    anhour_before = anhour_before.strftime('%H:%M:%S')
    return anhour_before_day, anhour_before

def like_blog_starter(api):
    day, anhour_before = get_anhour_before()
    tweets = api.search_tweets(
        q=f'#ブログ初心者 since:{day}_{anhour_before}_JST', lang='ja', count=50)
    print(f'#ブログ初心者 since:{day}_{anhour_before}_JST')
    users = []
    for tweet in tweets:
        user_id = tweet.user.id
        user = api.get_user(user_id=user_id)
        #ツイートのいいねの数
        if tweet.favorite_count >= 10:
            print('-----------------')    
            print('いいね過多')
            continue
        #フォロワー数
        if user.followers_count >= 200:
            print('-----------------')
            print('フォロワー過多')
            continue
        print('-----------------')
        print(f'ユーザー名：{tweet.user.screen_name}')
        print(f'フォロワー数：{user.followers_count}')
        print(f'内容：{tweet.text}')
        
        try:
            api.create_favorite(id=tweet.id)
            print('ツイートをいいねしました')
        except:
            print('既にいいね済みです')
            
        try:
            api.create_friendship(user_id=user_id)
            print(f'{user.screen_name}をフォローしました')
        except:
            print(f'既に{user.screen_name}をフォロー済みです')


if __name__ == '__main__':
    #API認証
    api = create_api(os.getenv('API_KEY'), os.getenv('API_SECRET'), os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    like_blog_starter(api)