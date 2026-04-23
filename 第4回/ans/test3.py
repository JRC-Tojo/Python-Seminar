# 
# 課題３・４の解答
# 各学習方法についてクラス単位で実装を行うことで，必要なモデルを呼び出しやすくした
# 

from copy import deepcopy
import numpy as np


class GradientMethod:
    def __init__(self, lossFunc, step=10**(-4)) -> None:
        self.step = step
        self.lossFunc = lossFunc

    def loss(self, x, w):
        return self.lossFunc(x, w)

    def grad(self, x, w:list, h=10**(-5)):
        """
        微分計算を極限の形の定義式より，数値計算することで導出する
        """
        results = []
        for i in range(len(w)):
            tmpw = deepcopy(w)
            tmpw[i] = w[i] + h
            _grad = (self.loss(x, tmpw) - self.loss(x, w)) / h
            results.append(_grad)
        return results

    def minimization(self, x:np.ndarray, w:list, radius=1e-5, epochs=10**5):
        """
        勾配法によって目的関数を最小化する

        Parameters
        ---
        x: 予測対象のxデータ，最小化問題では予測対象がないためNoneでもよい
        w: 最小化する目的パラメーター群（関数最小化問題ではxと同じ配列を指定）
        radius: 収束半径
        epochs: 最大反復回数
        """
        for epoch in range(epochs+1):
            grads = self.grad(x, w)

            # パラメーターごとにどの程度進むかを決める
            for i in range(len(w)):
                tmpW = w[i] - self.step * grads[i]
                w[i] = tmpW
            
            if abs(max(grads)) < radius:
                print(f'Loss function is minimized at {epoch} Epoch')
                return w

        print('Loss function is not enough minimized')
        return w

class sgdMethod(GradientMethod):
    """
    確率的勾配法の実装\n
    最小化問題において確率的勾配法は利用できない
    """
    def __init__(self, lossFunc, step=10**-4) -> None:
        super().__init__(lossFunc, step)

    def minimization(self, x:np.ndarray, w:list, radius=1e-5, epochs=10**5):
        """
        勾配法によって目的関数を最小化する

        Parameters
        ---
        w: パラメーター群
        radius: 収束半径
        epochs: 最大反復回数
        """
        for epoch in range(epochs+1):
            index = np.random.randint(0, x.shape[0])
            tmpX = x[index]
            grads = self.grad(tmpX, w)

            # パラメーターごとにどの程度進むかを決める
            for i in range(len(w)):
                tmpW = w[i] - self.step * grads[i]
                w[i] = tmpW
            
            if abs(max(grads)) < radius:
                print(f'Loss function is minimized at {epoch} Epoch')
                return w

        print('Loss function is not enough minimized')
        return w


if __name__ == '__main__':
    def f(x, w):
        """
        最小値を導出する関数を定義する
        """
        return w[0]**6 - w[0]**4 + w[0]**3 - w[0]**2
    
    # 初期値
    x = [-2]
    
    # 最小化ツールの宣言と処理の実行
    gradMethod = GradientMethod(f)
    print(gradMethod.minimization(x, x))
