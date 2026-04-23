from pathlib import Path
from time import time
from matplotlib import pyplot as plt
import japanize_matplotlib

import numpy as np
import pandas as pd
from scipy.optimize import minimize

source = pd.read_csv(
    str(Path(__file__).parent/'Sources'/'Traffic selection probability'/'dataset.csv'), encoding='shift-jis')
choices = source[['航空', '鉄道', 'バス']].values
traficTimes = source[['航空時間', '鉄道時間', 'バス時間']].values
traficCosts = source[['航空費用', '鉄道費用', 'バス費用']].values/100


def logistic(w, _times, _costs):
    """
    ロジットモデルにおける選択確率を導出する

    Parameters
    ---
    x: 入力データ
    w: パラメーター群
    """
    utilities = np.zeros(3)
    for i in range(len(_times)):
        x = np.array([i == 0, i == 1, _times[i], _costs[i]])
        utilities[i] = np.exp(x @ w)

    return utilities/sum(utilities)

def getSumLikelihoods(w):
    """
    目的関数である対数尤度の合計を算出する
    """
    likes = []
    for _choice, _times, _costs in zip(choices, traficTimes, traficCosts):
        sumV = logistic(w, _times, _costs)
        likes.append(np.log(sumV) @ _choice.T)

    return -sum(likes)

def draw(params):
    """
    パラメータ感度分析のグラフを描画
    """
    # 各種説明変数の固定化
    busTime = [350 + i*10 for i in range(22)]
    airTime = 168
    airCost = 19500 / 100
    trainTime = 279
    trainCost = 16320 / 100
    busCost = 9790 / 100
    costs = [airCost, trainCost, busCost]
    ratios = []
    for btime in busTime:
        ratios.append(logistic(params, [airTime, trainTime, btime], costs))
    ratios = np.array(ratios) * 100

    # 描画の定義
    plt.plot(busTime, ratios[:, 0], lw=4, label='航空確率')
    plt.plot(busTime, ratios[:, 1], lw=4, label='鉄道確率')
    plt.plot(busTime, ratios[:, 2], lw=4, label='バス確率')

    plt.title('バス所要時間の変化が選択確率に与える影響', fontsize=16)
    plt.xlabel('バス所要時間（分）', fontsize=12)
    plt.ylabel('選択確率（％）', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # パラメータ導出
    start = time()
    res = minimize(getSumLikelihoods, np.zeros(4), method='Nelder-Mead')
    print(f'{time() - start:.2f} s')

    # 描画
    draw(res.x)