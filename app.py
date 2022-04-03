import tweepy
import random
import time
import os
import datetime
from spreadsheet import append_users, judge_user_existence
from dotenv import load_dotenv
load_dotenv()

influencer_id_list = ["@takapon_jp", "@hirox246", "@ochyai"]  # ホリエモン、ひろゆき、落合陽一
#ここのid変えるとフォローする対象を変更できる

NG_WORDS=['RT']
MY_SCREENNAME = 'st_st_blog'

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
    anhour_before = dt_now + datetime.timedelta(hours=-0.4)
    anhour_before_day = anhour_before.strftime('%Y-%m-%d')
    anhour_before = anhour_before.strftime('%H:%M:%S')
    return anhour_before_day, anhour_before

def select_blog_starter(api):
    day, anhour_before = get_anhour_before()
    query = f'#ブログ初心者 since:{day}_{anhour_before}_JST'
    print(f'検索ワード:{query}')
    tweets = api.search_tweets(q=query, lang='ja', count=20)
    selected_users = []
    selected_tweets = []
    for tweet in tweets:
        flag = True
        user_id = tweet.user.id
        user = api.get_user(user_id=user_id)
        followers = user.followers_count
        friends = user.friends_count
        ff_ratio = friends/followers
        #ツイートのいいねの数
        if tweet.favorite_count >= 10:
            print('-----------------')    
            print('ツイートについているいいねが多い')
            continue
        #ff比
        if ff_ratio <= 0.8 or ff_ratio >= 2:
            print('-----------------')
            print('フォローを返さない人')
            continue
        #フォロワー数
        if followers >= 400:
            print('-----------------')
            print('フォロワーが多すぎる')
            continue
        #NGWORD機能
        for ng_word in NG_WORDS:
            if ng_word in tweet.text:
                flag = False
                break
        if flag:
            print('-----------------')
            print(f'ユーザー名：{tweet.user.screen_name}')
            print(f'フォロワー数：{followers}')
            print(f'ff比：{ff_ratio}')
            print(f'ツイート：{tweet.text}')
            print('-----------------')
            selected_tweets.append(tweet)
            selected_users.append(user)
    return selected_tweets, selected_users

def favorite_tweet(tweet):
    try:
        api.create_favorite(id=tweet.id)
        print('ツイートをいいねしました')
    except:
        print('既にいいね済みです')

def follow_user(user):
    if judge_user_existence(user.screen_name):
        print(f'既に{user.screen_name}をフォロー済みです')
    else:
        api.create_friendship(user_id=user.id)
        print(f'{user.screen_name}をフォローしました')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        append_users([selected_user.screen_name, today])
    # try:   
    #     api.create_friendship(user_id=user.id)
    #     print(f'{user.screen_name}をフォローしました')
    #     already_follow = False
    #     return already_follow
    # except:
    #     print(f'既に{user.screen_name}をフォロー済みです')
    #     already_follow = True
    #     return already_follow

#API認証
api = create_api(os.getenv('API_KEY'), os.getenv(
    'API_SECRET'), os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))

if __name__ == '__main__':
    selected_tweets, selected_users = select_blog_starter(api)
    # for selected_tweet in selected_tweets:
    #     favorite_tweet(selected_tweet)
    for selected_user in selected_users:
        follow_user(selected_user)

#今後はスプシからフォローを返さない人をリムーブする