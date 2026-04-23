> [出題時のScrapbox](https://scrapbox.io/actscape-seminar/%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%82%BC%E3%83%9F_-_5)

# 1. 機械学習帳の復習

- 5.線形二値分類，6.線形多クラス分類の確認問題を解く

- 6章のMNISTについては`createMNIST.py`を実行して`mnist.npz`というデータセットを生成すること



# 2. 交通手段選択のパラメータ推定

[交通選択データテーブル](ans/Sources/Traffic%20selection%20probability/dataset.csv)に対して最尤推定を`Scipy.optimize.minimize()`によって行うプログラムを実装し，所要時間（or 費用）の変化が各交通経路選択確率に及ぼす影響を考察せよ

- [交通手段選択の分析を行ったエクセルシート](ans/Sources/Traffic%20selection%20probability/%E8%80%83%E5%AF%9F%E4%BE%8B.xlsx)を作成したため，参考にしてください

    - パラメータ推定にはソルバーを使用しています
    
    - ２つ目のタブには考察の一例を示しています

- Scipyは組み込みライブラリではないため，`pip install scipy`でインストールを行ってください

- `minimize()`は引数として与えた関数について，パラメーターをうまく調整して最小化した結果を返すメソッドです．２次関数に乱数を加えたデータセットに対して，残差２乗和を最小化することでパラメータを推定するプログラムを以下に示します．

    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.optimize import minimize
    

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
    print(res.x)
    # [2.00517805 -3.83845419  4.80906073]という結果を得る
    # 求めたいパラメータであるabcAnsとほぼ同じ値となっている

    # 様子を見たい
    plt.scatter(sourceX, sourceY)
    plt.plot(sourceX, objective_func(sourceX, *res.x))
    plt.show()
    ```


## 最尤推定の概要

とある人がとある交通手段$ i(=1,2,...,n)$を選択した際の対数尤度は次の通り

$$ L=\sum^n_i{\delta_i}\ln{P_i} \tag{1} $$

ここで，$\delta_i$は選択した交通手段において1をとり，その他の交通で0を取る数値

全ての人（N人とする）に対してこの対数尤度を導出することから，最尤推定における目的関数は次の通り

$$ L^*=\sum^N_p{\sum^n_i{\delta_{pi}\ln{P_{pi}}}} \tag{2} $$

とある交通手段$i$において選択確率$P_i$は次の通り

$$
\begin{equation}
    \begin{split}
        V_i &= \beta_i+\theta_{time}T_i+\theta_{cost}C_i \\
        P_i &= \frac{e^{V_i}}{\displaystyle\sum^n_{j=1}{e^{V_j}}} \\
    \end{split}
    \tag{3}
\end{equation}
$$

$\beta_i$は交通手段$i$における定数項であり，それぞれの交通手段で異なる値を持つ

すなわち，推定するパラメーターは$\beta_1,...,\beta_{n-1},\theta_{time},\theta_{cost}$である

最尤推定における目的関数は上に凸な関数ですが，minimize()は目的関数を最小化するメソッドであることに注意されたい