# https://aiacademy.jp/texts/show/?id=215&context=subject-ml
# ↑ラッソ回帰とリッジ回帰をしたかったがボストンデータのため断念

# ↓カリフォルニアデータを使用してやりたかったが挫折中
# https://zerofromlight.com/blogs/detail/65/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

from sklearn.linear_model import Lasso
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

housing = fetch_california_housing()

df_housing = pd.DataFrame(housing.data, columns=housing.feature_names)
df_housing.head()

df_housing['price'] = housing.target
df_housing.head()

# df_housing.info()




