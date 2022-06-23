#単回帰分析の練習
https://aiacademy.jp/texts/show/?id=33&context=subject-ml#:~:text=%E5%91%BC%E3%81%B3%E3%81%BE%E3%81%99%E3%80%82-,%E5%8D%98%E5%9B%9E%E5%B8%B0%E5%88%86%E6%9E%90%E3%81%AE%E5%AE%9F%E8%A3%85%E4%BE%8B,-%E7%B0%A1%E5%8D%98%E3%81%AA%E5%9B%9E%E5%B8%B0
#ピザのサイズを予想する

import matplotlib.pyplot as plt

x = [[12],[16],[20],[28],[36]]
y = [[700],[900],[1300],[1750],[1800]]

plt.figure()
plt.title('Relation between diameter and price')
plt.xlabel('diameter')
plt.ylabel('price')
plt.scatter(x,y)
plt.axis([0,50,0,2500])
plt.grid(True)
# plt.show()

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x,y)

import numpy as np

price = model.predict(np.array([25]).reshape(-1,1))
print('25 cm pizza should cost: $%s' %price[0][0])



