# 
# 機会学習帳６章の解答
# 確率的勾配法による線形分類問題を解くクラスを作成
# fit()を呼ぶことで二値分類にも多クラス分類にも対応できるようにした
# 
# 変数名やメソッド名はsklearnに準拠しており，if文の冒頭にて from... でモジュールを呼び出せば精度の比較などがその他の呼び出し部分を変更することなく行える
# ※SGDClassifier()の引数のみsklearnと違うものになっている
# 


from pathlib import Path

import numpy as np
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
from tqdm import tqdm


class SGDClassifier:
    def __init__(self, step=1e-3, radius=1e-5, itrs=100, alpha=0.0001, n_jobs=-1) -> None:
        self.step = step
        self.radius = radius
        self.itrs = itrs
        self.alpha = alpha
        self.n_jobs = n_jobs

    def _fit_binary(self, x, y):
        """
        2値分類のパラメータを推定

        ※一般的に，'_'で始まるメソッドは外から呼び出さない
        """
        N = x.shape[0]
        w = np.zeros(x.shape[1])
        randomList = np.arange(N)

        for epoch in tqdm(range(int(self.itrs)+1)):
            # 学習事例をランダムな順番にしておく
            np.random.shuffle(randomList)

            for index in randomList:
                tmpX = x[index]
                tmpY = y[index]
                p = 1 / (1 + np.exp(0 - (tmpX.T @ w)))
                w = (1-2*self.alpha*self.step/N)*w + self.step*(tmpY - p)*tmpX
            
            # 勾配が十分に小さくなったと判断して打ち切る（これをコメントアウトすると，指定したEpochで繰り返し計算する）
            grad = 0 - (tmpY - p)*tmpX + (2*self.alpha/N)*w
            if max(abs(grad)) < self.radius:
                break

        self.finalEpoch = epoch * x.shape[0]
        return w

    def _fit_multiclass(self, x, y):
        """
        多クラス分類のパラメータを推定
        """
        oneHotY = np.eye(self.classes)[y]
        result = Parallel(self.n_jobs, verbose=1)(delayed(self._fit_binary)(x, oneHotY[:, i]) for i in range(self.classes))
        return np.array(result)

    def fit(self, x, y):
        """
        あらゆる分類問題に対してパラメータの推定を行う汎用メソッド
        """
        self.classes = np.unique(y).shape[0]
        # 定数項を含めた訓練データの宣言
        addX = np.insert(x, 0, 1, axis=1)
        
        if np.unique(y).shape[0] == 2:
            w = self._fit_binary(addX, y)
            w = w.reshape(1, -1)
            print(f'Loss function is minimized at {self.finalEpoch} Epoch')
        else:
            w = self._fit_multiclass(addX, y)
        
        self.coef_ = w[:, 1:]
        self.intercept_ = w[:, 0]


    def export(self, suffix:str):
        """
        モデルを外部ファイルへ出力
        """
        np.save(str(Path(__file__).parent/f'sgdResult{suffix}'), np.insert(self.coef_, 0, self.intercept_, axis=1))

    def load(self, suffix:str):
        """
        外部へ保存したモデルを読み込む
        """
        w = np.load(str(Path(__file__).parent/f'sgdResult{suffix}.npy'))
        self.coef_ = w[:, 1:]
        self.intercept_ = w[:, 0]
        self.classes = 2 if self.coef_.shape[0] == 1 else self.coef_.shape[0]

    def predict_proba(self, x):
        """
        それぞれの分類ごとの予測確率を算出する
        """
        pList = []
        for i in range(self.coef_.shape[0]):
            p = 1 / (1 + np.exp(0 - (x.T @ self.coef_[i] + self.intercept_[i])))
            pList.append(p)
        
        if self.classes == 2:
            return np.array([1-p, p])
        else:
            return np.array(pList)

    def predict(self, x):
        """
        分類問題の推論の結果（分類結果）を出力
        """
        predicts = []
        for tmpX in x:
            probs: np.ndarray = self.predict_proba(tmpX)
            predicts.append(probs.argmax())
        return np.array(predicts)

    def score(self, Xtest, Ytest):
        """
        正答率を算出
        """
        predict: np.ndarray = self.predict(Xtest)
        return np.count_nonzero(predict == Ytest) / Xtest.shape[0]


def image_to_vector(X):
    """
    画像データ（２次元）を一列に並べてベクトル化する
    """
    return np.reshape(X, (len(X), -1))  # Flatten: (N x 28 x 28) -> (N x 784)

def draw(i:int, coef:np.ndarray, save=False):
    """
    学習した重みを画像として描画
    """
    absMax = max(abs(coef))
    w = coef.reshape(28, 28)

    fig, ax = plt.subplots(dpi=100)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    im = ax.imshow(w, cmap='bwr', vmin=0-absMax, vmax = absMax)
    fig.colorbar(im, ax=ax)
    if save:
        plt.savefig(Path(__file__).parent/'images'/f'coef_{i}.png')
    else:
        plt.show()


if __name__ == '__main__':
    # ソースデータの読み込み
    data = np.load(Path(__file__).parent/'Sources'/'MNIST'/'mnist.npz')
    Xtrain = image_to_vector(data['train_x'])       # (60000 x 784) (no bias term)
    Ytrain = data['train_y']                        # (60000) (not one-hot encoding)
    Xtest = image_to_vector(data['test_x'])         # (10000 x 784) (no bias term)
    Ytest = data['test_y']                          # (10000) (not one-hot encoding)

    # 学習
    ##################################################
    # sklearnの実装を動かす場合
    # from sklearn.linear_model import SGDClassifier
    # model = SGDClassifier(loss='log')
    ##################################################
    # 自作メソッドを動かす場合
    model = SGDClassifier(radius=1e-6)
    ##################################################
    model.fit(Xtrain, Ytrain)

    # モデルの保存を行ったり，作成したモデルを読み込む場合は以下のコメントを利用
    # model.export('_multi')
    # model.load('_multi')
    
    # 重みやバイアスを表示
    print(model.coef_)
    print(model.intercept_)

    # それぞれの数字を出力する際にモデルがどこに重みを持って考えているか画像として出力する
    for i in range(10):
        draw(i, model.coef_[i], True)

    # 予測結果 & 精度評価
    print(model.predict(Xtest[0:1]))
    print(Ytest[0])
    print(model.score(Xtest, Ytest))
