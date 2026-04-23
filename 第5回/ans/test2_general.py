# 
# test2.py（最尤推定）を一般化した実装
# 

from argparse import ArgumentTypeError
from pathlib import Path
from time import time

import japanize_matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import minimize


class Likelihood:
    def __init__(self) -> None:
        self._coef:np.ndarray
        self._intercept:np.ndarray

    def fit(self, choices:np.ndarray, explains:np.ndarray):
        """
        最尤推定のパラメータを計算する

        引数として与えるデータは以下の通り整形されたものとする

        Parameters
        ---
        choices : NDArray
            各状況における選択結果を示す

            OneHot表現になったもの or 各分類名を列挙した１次元ベクトルを入れる

        explains : NDArray
            各状況における説明変数を格納する

            説明変数は次のようなデータ構造となっている必要がある
            
            senario1 = [[choice1's explain1, choice1's explain2, ...], [choice2's explain1, choice2's explain2, ...], ...]

            explains = [senario1, senario2, ...]
        """
        # 引数の確認
        if len(choices.shape) == 1:
            unique = np.unique(choices)
            target_classes = np.frompyfunc(lambda className: np.where(unique==className)[0])(choices)
            self.one_hot_choices = np.eye(len(unique))[target_classes]
        elif np.all(np.unique(choices[0]) == np.array([0, 1])):
            self.one_hot_choices = choices
        else:
            raise ArgumentTypeError('You have to set one-hot vecs or class names in choices')
        if len(explains.shape) != 3:
            raise ArgumentTypeError(f'You have to set the explains size (data_count, class_count, variable_count), not {explains.shape}')

        # データ次元の決定
        self.class_count = explains.shape[1]
        self.valiable_count = explains.shape[2]

        # パラメータの次元決定
        self._coef = np.zeros(self.valiable_count)
        self._intercept = np.zeros(self.class_count - 1)

        # 学習用のデータを作成する
        self.calc_explains = self.__addIntercept(explains)

        # 目的関数最小化
        res = minimize(self.__sumLikelihood, self.w, method='Nelder-Mead')
        self._coef = res.x[:self.valiable_count]
        self._intercept = res.x[self.valiable_count:]

    def __sumLikelihood(self, w:np.ndarray):
        """
        対数尤度の合計（目的関数）
        """
        V = self.one_hot_choices * np.log(self.__logistic(w, self.calc_explains))
        return -V.sum()

    def __logistic(self, w, data:np.ndarray):
        """
        各選択肢に対する尤度
        """
        U = np.exp(data @ w)
        sum_U = np.repeat(U.sum(axis=1), self.class_count, axis=0).reshape(-1, self.class_count)
        return U/sum_U

    @property
    def w(self):
        """
        パラメータリストに定数項も併せて載せる
        """
        return np.append(self._coef, self._intercept)

    def __addIntercept(self, explain:np.ndarray):
        """
        元データに定数項の係数になる１，０データを付加する
        """
        selections = np.repeat(np.eye(self.class_count, dtype=int)[None, :, :self.class_count-1], explain.shape[0], axis=0)
        return np.append(explain, selections, axis=2)
    
    def predict(self, explains:np.ndarray) -> np.ndarray:
        """
        与えられた説明変数に対して選択確率を出力する

        explainsで与えるデータ構造はfit()と同じ形にする
        """
        return self.__logistic(self.w, self.__addIntercept(explains))


def draw(model:Likelihood):
    """
    パラメータ感度分析のグラフを描画

    テストケースの描画に特化した関数であり，任意のデータセットに対する描画関数ではない
    """
    # 各種説明変数の固定化
    dataset  = np.ones((22, 6))
    busTimes = np.array([350 + i*10 for i in range(22)])
    dataset[:, 0] *= 168
    dataset[:, 1] *= 19500 / 100
    dataset[:, 2] *= 279
    dataset[:, 3] *= 16320 / 100
    dataset[:, 4]  = busTimes
    dataset[:, 5] *= 9790 / 100

    # 要求された形に整形する
    dataset = dataset.reshape((-1, 3, 2))
    ratios = model.predict(dataset) * 100

    # グラフの定義
    plt.plot(busTimes, ratios[:, 0], lw=4, label='航空確率')
    plt.plot(busTimes, ratios[:, 1], lw=4, label='鉄道確率')
    plt.plot(busTimes, ratios[:, 2], lw=4, label='バス確率')

    plt.title('バス所要時間の変化が選択確率に与える影響', fontsize=16)
    plt.xlabel('バス所要時間（分）', fontsize=12)
    plt.ylabel('選択確率（％）', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # データの読み込み
    dataset = pd.read_csv(str(Path(__file__).parent/'Sources'/'Traffic selection probability'/'dataset.csv'), encoding='shift-jis')

    # 説明変数の抽出
    values = dataset[['航空時間', '航空費用', '鉄道時間', '鉄道費用', 'バス時間', 'バス費用']].values
    # fitが要求する形に整形
    values = values.reshape((-1, 3, 2))
    # 「費用」を1/100倍してスケールを調整
    values[:, :, -1] = values[:, :, -1]/100

    # パラメータ推定
    model = Likelihood()
    start = time()
    model.fit(dataset[['航空', '鉄道', 'バス']].values, values)
    print(f'{time() - start:.2f} s')

    # 描画
    draw(model)

