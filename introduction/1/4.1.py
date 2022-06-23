# 機械学習入門の本
# 第1部4章1
# たけのこ派ときのこ派に分類する

import pandas as pd
# ファイルを読み込んでデータフレームに変換
df = pd.read_csv('KvsT.csv')
# 特徴量の列を参照してｘに代入
xcol = ['身長','体重','年代']
x = [xcol]
# 正解データ（派閥）を参照してｔに代入
t = df['派閥']

# モデルの学習（未学習）
from sklearn from tree
model = tree.DecisionTreeClassifier(random_state = 0)
# 学習の実行（ｘ、ｔは上記で定義した特徴量と正解ラベル）
model.fit(x,t)

# 試したい太郎のデータを二次元リストで作成
taro = [[170,70,20]]
# 太郎がどちらになるか予測
model.predict(taro)

# 正解率の計算
model.score(x,t)

# モデルの保存
import pickle
with open('KinokoTakenoko.pkl','wb') as f:
