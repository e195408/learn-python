#重回帰分析の練習
https://aiacademy.jp/texts/show/?id=33&context=subject-ml#:~:text=%E5%9B%9E%E5%B8%B0%E4%BF%82%E6%95%B0%E3%81%A8%E3%81%84%E3%81%84%E3%81%BE%E3%81%99%E3%80%82-,%E9%87%8D%E5%9B%9E%E5%B8%B0%E5%88%86%E6%9E%90%E3%81%AE%E5%AE%9F%E8%A3%85%E4%BE%8B,-%E3%81%A7%E3%81%AF%E3%80%81%E9%87%8D%E5%9B%9E%E5%B8%B0
#ピザの値段を予想する（トッピングなどの情報を追加した）

from sklearn.linear_model import LinearRegression
x = [[12,2],[16,1],[20,0],[28,2],[36,0]]
y = [[700],[900],[1300],[1750],[1800]]

model = LinearRegression()
model.fit(x,y)

x_test = [[16,2],[18,0],[22,2],[32,2],[24,0]]
y_test = [[1100],[850],[1500],[1800],[1100]]

prices = model.predict(x_test)

for i,price in enumerate(prices):
    print('Predicted:%s, Taget:%s'%(price,y_test[i]))

score = model.score(x_test,y_test)
print("r-squared:",score)
