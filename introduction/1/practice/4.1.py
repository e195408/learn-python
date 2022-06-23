import pandas as pd

data = {
    'データベースの試験得点':[70,72,75,80],
    'ネットワークの試験得点':[80,85,79,92]
}
df = pd.DataFrame(data)

df.index = ['一郎','次郎','三郎','太郎']
df

df2 = pd.read_csv('ex1.csv')

df2.index

df2.columns
