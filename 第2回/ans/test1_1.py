# 
# １．単回帰の確認問題
# 

from matplotlib import pyplot as plt
import numpy as np
import japanize_matplotlib


def Q1_1(d:np.ndarray):
    """
    引数として受けたDについて単回帰分析で出力される傾きaと切片bを出力する
    """
    x = d[:, 0]
    y = d[:, 1]

    # パラメータの算出に必要な値を定義
    x_mean = x.mean()
    y_mean = y.mean()
    xy_mean = (x*y).mean()
    x2_mean = (x**2).mean()

    # 単回帰分析におけるパラメータの定義式に基づいて算出
    a = (xy_mean - x_mean * y_mean) / (x2_mean - x_mean**2)
    b = y_mean - a*x_mean

    return a, b

def Q1_2(d:np.ndarray, a:float, b:float):
    """
    パラメータa, bとデータDのグラフを描画
    """
    x = d[:, 0]
    y = d[:, 1]

    # 回帰直線のデータを作成
    line_x = np.linspace(x.min()-5, x.max()+5)
    line_y = a*line_x + b

    # プロットする点や直線の定義
    plt.scatter(x, y, label='実データ')
    plt.plot(line_x, line_y, '--r', label='回帰直線')

    # 描画範囲を指定することで，直線の左右が途切れないように描画する
    plt.xlim(x.min()-2, x.max()+2)

    plt.title('回帰直線の描画')
    plt.legend()
    plt.show()

def Q1_3(d:np.ndarray, a:float, b:float):
    """
    回帰直線と実データの残差を算出
    """
    x = d[:, 0]
    y = d[:, 1]
    return y - (a*x + b)

def Q1_4(d:np.ndarray, e:np.ndarray):
    """
    説明変数と残差`e`の共分散を算出

    機械学習帳，式1.34を参照
    """
    x = d[:, 0]
    return (x*e).sum() / d.shape[0]

def Q1_5(d:np.ndarray, a:float, b:float, e:np.ndarray):
    """
    目的変数の推定値と残差`e`の共分散を算出

    機械学習帳，式1.36を参照
    """
    x = d[:, 0]
    predY = a*x + b
    return (predY*e).sum() / d.shape[0]

def Q1_6(d:np.ndarray, e:np.ndarray):
    """
    決定係数を算出
    """
    y = d[:, 1]
    return 1 - e.var() / y.var()



if __name__ == "__main__":
    # データの宣言
    d = np.array([[1, 3], [3, 6], [6, 5], [8, 7]])
    
    a, b = Q1_1(d)
    
    Q1_2(d, a, b)
    
    e = Q1_3(d, a, b)

    print(f'説明変数と残差の共分散: {Q1_4(d, e)}')
    print(f'目的変数の推定値と残差の共分散: {Q1_5(d, a, b, e)}')
    print(f'決定係数: {Q1_6(d, e)}')
