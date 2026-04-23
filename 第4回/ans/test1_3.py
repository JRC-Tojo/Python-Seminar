# 
# 3. モデル選択と正則化
# 

import japanize_matplotlib
import numpy as np
from matplotlib import pyplot as plt


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

def Q3_1(x:np.ndarray, y:np.ndarray, alphas:list[float], dim=9, sideMargin=0.2):
    """
    リッジ回帰によって実データ`D`の近似曲線を作成する
    
    `alphas`は正則化のパラメータリスト

    作成した近似曲線についてグラフの作成も行う

    Parameters
    ---
    - `dim`: 重回帰分析における次数（xの何乗まで含む多項式にするか）を決定する
    - `sideMargin`: 描画時に与えた点の両サイドにもつ余白の大きさ
    """
    ws = []
    x_line = np.linspace(x.min()-sideMargin, x.max()+sideMargin)
    for alpha in alphas:
        # パラメータを算出（機械学習帳，式3.5を参照）
        X = __makeX(x, dim)
        w = np.linalg.inv(X.T@X + alpha*np.eye(X.shape[1]))@X.T@y
        ws.append(w)

        # 図の定義
        plotX = __makeX(x_line, dim)
        plt.plot(x_line, plotX @ w, '--', label=fr'回帰曲線 $\alpha = {alpha}$')

    # 実データの散布図
    plt.scatter(x, y, label='実データ')

    # 描画範囲を指定することで，直線の左右が途切れないように描画する
    plt.xlim(x.min()-sideMargin, x.max()+sideMargin)

    plt.title('様々なリッジ回帰曲線の描画')
    plt.legend()
    plt.show()

    return ws


def Q3_2(ws:list[np.ndarray], alphas:list[float]):
    """
    L2ノルムを算出
    """
    for w, alpha in zip(ws, alphas):
        print(f'α = {alpha} : ||w||^2 = {w@w.T}')


def Q3_3(x:np.ndarray, y:np.ndarray, ws:list[np.ndarray], alphas:list[float], dim=9):
    """
    汎化性能が最も高いパラメータを見つける
    """
    def mse(y_true:np.ndarray, y_pred:np.ndarray):
        """
        平均２乗残差（MSE）を算出する
        """
        return ((y_true - y_pred)**2).mean()
    
    # 各パラメータに対応するwを用いて，パラメータごとに残差が算出されたリストを作成
    X = __makeX(x, dim)
    mses = [mse(y, X @ w) for w in ws]

    print(f'最も汎化性能の高いパラメータは，MSEが最小となった「α = {alphas[np.argmin(mses)]}」である．')



if __name__ == "__main__":
    alphas = [1e-9, 1e-6, 1e-3, 1]
    x = np.array([ 0.  ,  0.16,  0.22,  0.34,  0.44,  0.5 ,  0.67,  0.73,  0.9 ,  1.  ])
    y = np.array([-0.06,  0.94,  0.97,  0.85,  0.25,  0.09, -0.9 , -0.93, -0.53,  0.08])

    # ハイパーパラメータと回帰曲線の関係を描画
    ws = Q3_1(x, y, alphas)

    # L2ノルム
    Q3_2(ws, alphas)

    # 検証
    # (Pythonの変数名は原則小文字で始める)
    xValid = np.array([ 0.05,  0.08,  0.12,  0.16,  0.28,  0.44,  0.47,  0.55,  0.63,  0.99])
    yValid = np.array([ 0.35,  0.58,  0.68,  0.87,  0.83,  0.45,  0.01, -0.36, -0.83, -0.06])
    Q3_3(xValid, yValid, ws, alphas)
