import json
import tweepy
from pprint import pprint

# API情報を記入
from pandas.io.json import json_normalize

BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAANjxegEAAAAA6QThvSP3PAjoEQNzdOP8Hj4asFg%3D4OYU76W0CTzWNj8OSMl3sOebdAW88WsnbJ26hx09DO2aIAqBEN"
API_KEY             = "CyDAKDFXFXA3Xo7kW1AT4s5Ax"
API_SECRET          =  "L1AC89dCbvud3OIQQ119pxsAdcVB2QGcGGYGywg71IEAq36hqs"
ACCESS_TOKEN        = "3247854692-LkKtNIGlA7huMQHzFUFf5rNfK2RZjVPmSAmSfJk"
ACCESS_TOKEN_SECRET = "CsAWbp0NZ5Uit4ih9NVdNGLhEyaq81qpi5K2uiNUN9xxV"


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                           )

    return client

#tweet取得コード#
# ★必要情報入力
search    =   '勅使河原'
tweet_max = 100          # 取得したいツイート数(10〜100で設定可能)

# 関数
def SearchTweets(search,tweet_max):
    # 直近のツイート取得
    tweets = ClientInfo().search_recent_tweets(query = search, max_results = tweet_max)

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

    with open("twitter/tweet_data/top.csv",mode="w", encoding="shift-jis",errors="ignore")as f:
        df.to_csv(f)
    # df.to_csv("twitter/tweet_data/01.csv", encoding="")

    # 結果出力
    return results


if __name__ == "__main__":
    SearchTweets(search, tweet_max)
