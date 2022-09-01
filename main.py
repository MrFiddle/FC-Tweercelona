# Juan Pablo | Mr Fiddle -w-

import time
from datetime import datetime
import os
from dotenv import load_dotenv
import re
import tweepy
import urllib.request
from random import randrange
import logging

load_dotenv()

api_key=os.getenv('api_key')
api_secret_key=os.getenv('api_secret_key')
access_token=os.getenv('access_token')
access_token_secret=os.getenv('access_token_secret')
telegram_token=os.getenv('telegram_token')
chat_id=os.getenv('chat_id')
personal_chat_id=os.getenv('personal_chat_id')

def main(api_key, api_secret_key, access_token, access_token_secret, telegram_token, chat_id, personal_chat_id):

    RT = 25
    logging.addLevelName(RT, "RT")

    logging.basicConfig(filename = 'logs.log', encoding = 'utf-8', level=logging.INFO)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    tweet_number = 0
    lastTweetBuffer = ""

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    friendlyReminders = (

        "De Jong won't downgrade to United", # 0
        "Barcelona will no longer exist in two years", # 1
        "La gente guapa esta arriba de la Xavineta", # 2
        "La gente inteligente confia en Ten Hag" # 3

    )

    barcelona_keywords = (
        
        "barcelona",
        "barça",
        "fc barcelona",
        "laporta",
        "joan laporta",
        "xavi",
        "mateu alemany",
        "alemany",

        "lewandowski",
        "frenkie de jong",
        "frenkie",
        "de jong",

        "kounde",
        "#fcb",
        "fcb"

    )

    api = tweepy.API(auth)

    while True:

        try:

            odds = randrange(500)

            print("tweet n: " + str(tweet_number))
            statuses = api.user_timeline(screen_name="FabrizioRomano", tweet_mode = "extended")

            if len(statuses) < 19:

                continue

            print("array length tweets: " + str(len(statuses)))
            latestFabrizioTweet = (statuses[tweet_number].full_text, "https://twitter.com/FabrizioRomano/status/" + str(statuses[tweet_number].id))

            if odds == 7:

                friendlyMessage = "Friendly reminder! : " + friendlyReminders[randrange(4)]
                print(friendlyMessage)
                urlRequest = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={friendlyMessage}'
                urlRequest = urlRequest.replace(" ", "%20")
                urllib.request.urlopen(urlRequest)

            if latestFabrizioTweet[0][0:2] == "RT":

                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logging.log(RT, f' {now} | rt junk | {latestFabrizioTweet[1]}')
                tweet_number = tweet_number + 1
                time.sleep(2)
                continue
            
            elif latestFabrizioTweet[0] == lastTweetBuffer:

                print("no news yet")
                tweet_number = 0

            else:

                for i in barcelona_keywords:

                    if re.search(r'\b' + i + r'\b', latestFabrizioTweet[0].lower()):

                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        lastTweetBuffer = latestFabrizioTweet[0]
                        print("🚨🚨 FC BARCELONA NEWS! 🚨🚨 : " + latestFabrizioTweet[0])
                        print("LINK OF THE TWEET: " + latestFabrizioTweet[1])

                        botMessage = f'FC BARCELONA NEWS! | TWEET URL: {latestFabrizioTweet[1]}'

                        urlRequest = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={botMessage}'
                        urlRequest = urlRequest.replace(" ", "%20")
                        urllib.request.urlopen(urlRequest)

                        tweet_number = 0
                        logging.info(f' {now} | fcb pass | {latestFabrizioTweet[1]}')

                        break

                    else:

                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        logging.warning(f' {now} | junk | {latestFabrizioTweet[1]}')
                        tweet_number = 0
                        print("no barca tweet")
                        break

            time.sleep(30)
        
        except KeyboardInterrupt:

            print("nothing")
            break

        except:

            bot_text = 'Bot stopped working'

            print(bot_text)

            urlRequestError = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={personal_chat_id}&text={bot_text.replace(" ", "%20")}'
            urllib.request.urlopen(urlRequestError)
            break
 

if __name__ == "__main__":

    try:

        main(api_key, api_secret_key, access_token, access_token_secret, telegram_token, chat_id, personal_chat_id)

    except:

        bot_text = "Bot couldn't start"

        print(bot_text)

        urlRequestError = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={bot_text.replace(" ", "%20")}'
        urllib.request.urlopen(urlRequestError)


        