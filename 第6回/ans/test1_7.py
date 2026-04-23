# 
# 機械学習帳７章の解答
# 出力されるグラフはHP上の表示と同じになるようにした
# 

from matplotlib import pyplot as plt
import numpy as np

def f(x, v, w, b):
    def sigmoid(x):  
        return np.exp(-np.logaddexp(0, -x))
    return np.dot(sigmoid(np.outer(x, w) + b), v)

def init_graph():
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_aspect('equal')
    return fig, ax

if __name__ == "__main__":
    # 元データ
    X = np.linspace(-4.5, 3.5, 1000)

    # パラメータ計算
    v = np.array([-1, 1, 1, -1, -1, 2, -1, 1, -2])
    stepX = np.array([-6, -4, -3, -2, -1, 0, 1, 2, 3])
    w = np.array([1000] * v.shape[0])
    b = -stepX * w

    # グラフの描画
    fig, ax = init_graph()
    ax.plot(X, f(X, v, w, b))
    plt.show()