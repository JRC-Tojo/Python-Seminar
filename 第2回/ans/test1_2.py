# 
# ２．重回帰の確認問題
# 

from matplotlib import pyplot as plt
import numpy as np
import japanize_matplotlib

# test1_1.pyより関数を引用する
from test1_1 import Q1_1, Q1_3, Q1_6


def __makeX(x:np.ndarray, dim=1):
    """
    もともとのx座標に定数項部分と累乗部分を付け足して回帰計算ができる行列形式に整形したXを出力
    """
    # 定数項を定義
    X = np.insert(x.reshape((-1, 1)), 0, 1, axis=1)
    # 累乗部分を付け足していく
    for i in range(dim-1):
        X = np.insert(X, i+2, x**(i+2), axis=1)

    return X

def getW(d:np.ndarray, dim=1):
    """
    与えられた次数における重回帰分析を行った際のパラメータwを算出する
    """
    x = d[:, 0]
    y = d[:, 1]

    # 回帰計算で用いる行列Xを作成
    X = __makeX(x, dim)

    # パラメータを算出（機械学習帳，式2.25を参照）
    w = np.linalg.inv(X.T@X)@X.T@y

    return w

def plot(d:np.ndarray, w:np.ndarray):
    """
    任意の次元による関数で近似したパラメータ`w`について，回帰分析の結果を描画する
    """
    x = d[:, 0]
    y = d[:, 1]

    # 実データの定義
    plt.scatter(x, y, label='実データ')
    
    # 回帰の定義
    x_line = np.linspace(x.min()-5, x.max()+5)
    X = __makeX(x_line, w.shape[0]-1)
    plt.plot(x_line, X @ w, '--r', label='回帰曲線')

    # 描画範囲を指定することで，直線の左右が途切れないように描画する
    plt.xlim(x.min()-2, x.max()+2)

    plt.title('回帰曲線の描画')
    plt.legend()
    plt.show()

def R2(d:np.ndarray, w:np.ndarray):
    """
    任意の次元による関数で近似した際の決定係数を算出する
    """
    x = d[:, 0]
    y = d[:, 1]
    X = __makeX(x, w.shape[0]-1)
    
    # 残差の導出
    e = y - X@w

    # 決定係数
    r2 = 1 - e.var() / y.var()

    return r2



if __name__ == "__main__":
    # 必要なデータの宣言＆計算
    d = np.array([[1, 3], [3, 6], [6, 5], [8, 7]])
    a, b = Q1_1(d)
    e = Q1_3(d, a, b)

    # 重回帰分析
    print(f'単回帰分析におけるパラメータ: {(b, a)}')
    print(f'単回帰分析における決定係数: {Q1_6(d, e)}')
    w1 = getW(d, 1)
    w2 = getW(d, 2)
    w3 = getW(d, 3)
    print(f'１次関数によるパラメータ: {w1}')
    print(f'１次関数による決定係数: {R2(d, w1)}')
    print(f'２次関数によるパラメータ: {w2}')
    print(f'２次関数による決定係数: {R2(d, w2)}')
    print(f'３次関数によるパラメータ: {w3}')
    print(f'３次関数による決定係数: {R2(d, w3)}')
    plot(d, w1)
    plot(d, w2)
    plot(d, w3)