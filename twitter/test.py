import json
import tweepy
from pprint import pprint


BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAANjxegEAAAAA6QThvSP3PAjoEQNzdOP8Hj4asFg%3D4OYU76W0CTzWNj8OSMl3sOebdAW88WsnbJ26hx09DO2aIAqBEN"
API_KEY             = "CyDAKDFXFXA3Xo7kW1AT4s5Ax"
API_SECRET          =  "L1AC89dCbvud3OIQQ119pxsAdcVB2QGcGGYGywg71IEAq36hqs"
ACCESS_TOKEN        = "3247854692-LkKtNIGlA7huMQHzFUFf5rNfK2RZjVPmSAmSfJk"
ACCESS_TOKEN_SECRET = "CsAWbp0NZ5Uit4ih9NVdNGLhEyaq81qpi5K2uiNUN9xxV"

from requests_oauthlib import OAuth1Session

class Agent:

    ...

    def connect_api(self):
        api = OAuth1Session(config.CONSUMER_KEY,
                            config.CONSUMER_SECRET,
                            config.ACCESS_TOKEN,
                            config.ACCESS_TOKEN_SECRET)

        return api

    def make_params(self):
        query = '猫 filter:images min_replies:10 min_retweets:500 min_faves:500 exclude:retweets'
        params = {
            'q': query,
            'count': 20
        }

        return params

    def search_tweet(self, api, params):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        req = api.get(url, params=params)

        result = []
        if req.status_code == 200:
            tweets = json.loads(req.text)
            result = tweets['statuses']
        else:
            print("ERROR!: %d" % req.status_code)
            result = None

      # 取得したデータ加工
        results     = []
        tweets_data = tweets.data

      # tweet検索結果取得
        if tweets_data != None:
            for tweet in tweets_data:
                obj = {}
                obj["tweet_id"] = tweet.id      # Tweet_ID
                obj["text"] = tweet.text  # Tweet Content
                results.append(obj)
        else:
            results.append('')

        # info = json.loads(results)
        df = json_normalize(results)
        print(df)

        with open("twitter/tweet_data/5.csv",mode="w", encoding="shift-jis",errors="ignore")as f:
            df.to_csv(f)
        # df.to_csv("twitter/tweet_data/01.csv", encoding="")

        # 結果出力
        return results