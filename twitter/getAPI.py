#JSONとOAuth認証用のライブラリを使用
import json
from requests_oauthlib import OAuth1Session

#取得した認証キーを設定
CONSUMER_KEY = "CyDAKDFXFXA3Xo7kW1AT4s5Ax"
CONSUMER_SECRET = "L1AC89dCbvud3OIQQ119pxsAdcVB2QGcGGYGywg71IEAq36hqs"
ACCESS_TOKEN = "3247854692-LkKtNIGlA7huMQHzFUFf5rNfK2RZjVPmSAmSfJk"
ACCESS_SECRET = "CsAWbp0NZ5Uit4ih9NVdNGLhEyaq81qpi5K2uiNUN9xxV"
Bearer_Token = "AAAAAAAAAAAAAAAAAAAAANjxegEAAAAA6QThvSP3PAjoEQNzdOP8Hj4asFg%3D4OYU76W0CTzWNj8OSMl3sOebdAW88WsnbJ26hx09DO2aIAqBEN"

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

#API用のURLを設定（●にはデベロッパー管理画面のDev environment labelを入力）
url = "https://api.twitter.com/1.1/tweets/search/30day/testproductions.json"

#paramsに検索ワードや件数、日付などを入力
params = {'query' : '台風', #検索したいワード
           "maxResults" : "100"} #取得件数

#上記で設定したパラメーターをget関数を使い指定URLから取得
res = twitter.get(url, params = params)

#ステータスコードが正常値（200）だった場合の処理
if res.status_code == 200:

    #後でpandasで処理するためリスト化
    created_at = []
    text = []
    retweet_count = []
    favorite_count = []

    name = []
    followers_count = []
    friends_count = []
    statuses_count = []

    #100件を超えるデータ用に繰り返し処理で対応
    while True:
        tweets = json.loads(res.text)
        tweet_list = tweets["results"]

        for tweet in tweet_list:
            created_at.append(tweet["created_at"]) #投稿日時
            text.append(tweet["text"]) #投稿本文
            retweet_count.append(tweet["retweet_count"]) #リツイート数
            favorite_count.append(tweet["favorite_count"]) #いいね数
            user = tweet["user"]
            name.append(user["name"]) #名前
            followers_count.append(user["followers_count"]) #フォロワー数
            friends_count.append(user["friends_count"]) #フォロー数
            statuses_count.append(user["statuses_count"]) #投稿数

        #対象Tweetが101件以上となりnextページがある場合
        if "next"  in tweets.keys():
            #nextの値をパラメータに追加する
            params['next'] =  tweets["next"]
            print(params)
            tweet_list = tweets["results"]

        #nextページがない場合（100件以内の場合と最終ページ用）
        else:
            print("最終ページなので取得終了")
            break

else:
    print("ERROR: %d" % res.status_code)

