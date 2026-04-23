# 
# 機械学習帳８章の解答
# このプログラムは「8.4. 確認問題: 自動微分」の解答を示す
# 

import warnings
import torch

# torchのWarningを黙らせる
warnings.simplefilter(action='ignore')


def relu(x:torch.Tensor):
    """
    ReLU(x)の実装
    """
    x[x < 0] = 0
    return x

def sigmoid(x:torch.Tensor):
    """
    シグモイド関数の実装
    """
    return 1 / (1 + torch.exp(-x))

def crossEntropyLoss(y_true:torch.Tensor, y_pred:torch.Tensor):
    """
    クロスエントロピー損失関数の値を算出

    Parameters
    ---
    - `y_true`: 答えの値
    - `y_pred`: 予測結果の値
    """
    l = y_true * y_pred + (1 - y_true) * (1 - y_pred)
    return -torch.log(l).sum()

def Q1(x:torch.Tensor, W:torch.Tensor, q:torch.Tensor, b:torch.Tensor, c:float):
    """
    与えられた式の出力を計算する
    """
    h = relu(W@x + b)
    y = sigmoid(h.T@q + c)

    return h, y

def Q2(x:torch.Tensor, y:torch.Tensor, W:torch.Tensor, q:torch.Tensor, b:torch.Tensor, c:float):
    """
    勾配計算
    """
    h, y_pred = Q1(x, W, q, b, c)
    loss = crossEntropyLoss(y, y_pred)
    loss.backward()

    print(loss.item())
    print(f'Wの勾配 : {W.grad}')
    print(f'qの勾配 : {q.grad}')
    print(f'bの勾配 : {b.grad}')
    print(f'cの勾配 : {c.grad}')


if __name__ == "__main__":
    x = torch.tensor([0, 0], dtype=torch.float)
    W = torch.tensor([[1, 1], [-1, -1]], dtype=torch.float, requires_grad=True)
    q = torch.tensor([1, 1], dtype=torch.float, requires_grad=True)
    b = torch.tensor([-0.5, 1.5], dtype=torch.float, requires_grad=True)
    c = torch.tensor(-1.5, requires_grad=True)
    
    print(Q1(x, W, q, b, c))

    x = torch.tensor([1, 1], dtype=torch.float)
    y = torch.tensor(0)
    Q2(x, y, W, q, b, c)