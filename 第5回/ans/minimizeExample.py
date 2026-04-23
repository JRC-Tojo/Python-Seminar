from scipy.optimize import minimize
import numpy as np

def objective_func(x, a, b, c):
	# 目的関数（この例では２次関数）
	return a * x**2 + b * x + c
	

# abcAnsは求めたいパラメータの答え
abcAns = [2, -4, 5]
sourceX = np.linspace(-5, 5, 50)
# sourceY は本来の２次関数に乱数を載せたものとした
sourceY = objective_func(sourceX, *abcAns) + np.random.normal(0, 3, len(sourceX))

def zansa(param):
	# sourceX, sourceYと予測した２次関数の残差２乗和を返す
    return ((sourceY - objective_func(sourceX, *param))**2).sum()

# 第一引数に最小化したい関数
# 第二引数に最適化するパラメータの初期値（今回は[0, 0, 0]とした）
# 第三引数は例のように記載する．Nelder-Meadが何かは次回説明
res = minimize(zansa, np.zeros(3), method='Nelder-Mead')
print(res.x)  # []という結果を得ることができ，求めたいパラメータであるabcAnsとほぼ同じ値となっている


import matplotlib.pyplot as plt
plt.scatter(sourceX, sourceY)
plt.plot(sourceX, objective_func(sourceX, *res.x))
plt.show()