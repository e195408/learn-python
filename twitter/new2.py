# ★ツイートIDを指定
tweet_id = 'ツイートIDを入力'

# 関数
def GetTweet(tweet_id):
    # メソッド実行
    GetTwt = ClientInfo().get_tweet(id=int(tweet_id), expansions=["author_id"], user_fields=["username"])

    # 結果加工
    twt_result = {}
    twt_result["tweet_id"] = tweet_id
    twt_result["user_id"]  = GetTwt.includes["users"][0].id
    twt_result["username"] = GetTwt.includes["users"][0].username
    twt_result["text"]     = GetTwt.data
    twt_result["url"]      = "https://twitter.com/" + GetTwt.includes["users"][0].username + "/status/" + str(tweet_id)

    # 結果出力
    return twt_result

# 関数実行・出力
pprint(GetTweet(tweet_id))