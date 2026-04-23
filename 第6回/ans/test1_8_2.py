# 
# 機械学習帳８章の解答
# このプログラムは「8.5. 確認問題: NNの学習」の解答を示す
# 

from copy import deepcopy
from pathlib import Path
import sys

import japanize_matplotlib
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from torch.nn import CrossEntropyLoss, Dropout, Linear, Module, ReLU
from torch.optim import Optimizer, SGD

# 上位階層を経由して別ディレクトリのプログラムを呼び出す場合，
# sys.pathによってカレントディレクトリを追加する必要あり
sys.path.append(str(Path(__file__).parents[2]))
from 第5回.ans.test1_6 import image_to_vector


class SingleLayer(Module):
    """
    単層NNモデルの定義
    """
    def __init__(self, features:int, outClasses:int=10) -> None:
        super().__init__()
        # レイヤの宣言
        self.linear = Linear(features, outClasses)

    def forward(self, x):
        """
        モデルの具体的な中身を定義
        """
        return self.linear(x)


class MultiLayer(Module):
    """
    多層NNモデルの定義
    """
    def __init__(self, features:int, channels=64, outClasses:int=10) -> None:
        super().__init__()
        self.linear1 = Linear(features, channels)
        self.linear2 = Linear(channels, channels)
        self.linear3 = Linear(channels, outClasses)
        self.relu = ReLU()
        self.dropout = Dropout(0.2)

    def forward(self, x):
        """
        モデルの中身
        """
        # 第１層
        x = self.linear1(x)
        x = self.dropout(x)
        x = self.relu(x)
        
        # 第２層
        x = self.linear2(x)
        x = self.dropout(x)
        x = self.relu(x)
        
        # 第３層
        x = self.linear3(x)

        return x


class Recorder:
    """
    Machine Learningの結果を整理する

    元プログラムはGitHub上の「ActScapeLab-2022/building-type-prediction-model/種別予測-改/utils/result.py」のnnResultsクラス
    """
    def __init__(self, train_y:torch.Tensor, val_y:torch.Tensor=None) -> None:
        # source
        self.train_y = train_y
        self.val_y   = val_y
        # learning history
        self.losses     = []
        self.accuracies = []
        self.valLosses     = []
        self.valAccuracies = []
        self.bestModel = None
        self.lastModel = None

    @property
    def hasValidation(self):
        return self.val_y is not None

    @property
    def epoch(self):
        return len(self.losses)

    def setResult(self, model:Module, train_out:torch.Tensor, loss:torch.Tensor, val_out:torch.Tensor=None, valLoss:torch.Tensor=None):
        """
        各学習段階で出力されるモデルやLossなどの情報をオブジェクトに登録しておく
        """
        # 最終モデルを記録
        self.lastModel = deepcopy(model)
        # 正答率の算出
        accuracy, valAccuracy = self.accuracy(train_out, val_out)
        # 最も良い検証精度を出力したモデルを記録
        if self.bestModel is None or max(self.valAccuracies) < valAccuracy:
            self.bestModel = deepcopy(model)
        # 損失と正答率の一覧を記録
        self.losses.append(loss.cpu().detach().numpy())
        self.accuracies.append(accuracy)
        if self.hasValidation:
            self.valLosses.append(valLoss.cpu().detach().numpy())
            self.valAccuracies.append(valAccuracy)

    def accuracy(self, train_out:torch.Tensor, val_out:torch.Tensor):
        """
        正答率を出力する
        """
        def _accuracy(y:torch.Tensor, out:torch.Tensor):
            if y is None or out is None: return None
            y    = y.cpu().detach().numpy()
            pred = out.argmax(dim=1).cpu().detach().numpy()
            return accuracy_score(y, pred)*100
        
        train_acc = _accuracy(self.train_y, train_out)
        val_acc   = _accuracy(self.val_y, val_out)
        return train_acc, val_acc

    def getHalfway(self, **contents):
        """
        途中経過をコンソールに出力するための文字列を返す

        Epoch数などは登録された情報をもとに計算する

        `contents`に指定すると，その内容も表示に含めることができる
        """
        strLine = []
        strLine.append(f'Epoch: {self.epoch}')
        strLine.append(f'Acc: {self.accuracies[-1]:.2f}%')
        strLine.append(f'Loss: {self.losses[-1]:.4f}')
        if self.hasValidation:
            strLine.append(f'valAcc: {self.valAccuracies[-1]:.2f}%')
            strLine.append(f'valLoss: {self.valLosses[-1]:.4f}')
        for k, v in contents.items():
            strLine.append(f'{k}: {v}')

        return ', '.join(strLine)

    def plot(self, title:str, savePath=None):
        """
        draw loss graph
        """
        # define objects
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        # plot data
        loss_indices = np.arange(1, self.epoch+1)
        ax1.plot(loss_indices, self.accuracies     , label='accuracy')
        ax2.plot(loss_indices, self.losses,    '--', label='loss')
        if self.hasValidation:
            ax1.plot(loss_indices, self.valAccuracies     , label='valAccuracy', color='orange')
            ax2.plot(loss_indices, self.valLosses,    '--', label='valLoss'    , color='orange')

        # set legend
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax2.legend(h1+h2, l1+l2)

        # set labels
        plt.title(title)
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax2.set_ylabel('Loss')
        plt.tight_layout()

        if savePath is None:
            plt.show()
        else:
            plt.savefig(savePath)

##############################################################################

def train(
    x_train:torch.Tensor,
    y_train:torch.Tensor,
    x_val:torch.Tensor,
    y_val:torch.Tensor,
    model:Module,
    optimizer:Optimizer,
    epoch=1000,
    freqInfo=100
):
    """
    モデルの学習を行う
    
    Loaderを使ってバッチ学習を行っても良いが，ここでは最も単純な実装を提示

    `freqInfo`で途中経過を表示する間隔（何Epochずつ表示するか）を調整
    """
    # 学習過程を記録しておくオブジェクトを宣言
    recorder = Recorder(y_train, y_val)
    
    # 損失関数にクロスエントロピーを指定
    criterion = CrossEntropyLoss()

    for e in range(epoch):
        # 学習データと検証データにおける結果を出力
        out_train = model(x_train)
        out_val   = model(x_val)
        
        # 損失の算出
        loss_train = criterion(out_train, y_train)
        loss_val   = criterion(out_val, y_val)

        # 自動微分＆パラメータ更新
        optimizer.zero_grad()
        loss_train.backward()
        optimizer.step()

        # 学習過程を記録
        recorder.setResult(model, out_train, loss_train, out_val, loss_val)
        
        # 途中経過を表示
        if e==0 or (e+1)%freqInfo==0:
            print(recorder.getHalfway())

    return recorder


def softmax(x:np.ndarray):
    """
    softmax関数を定義する
    """
    return np.exp(x) / np.exp(x).sum(axis=1).reshape(-1, 1)


def Q1(recorder:Recorder, title:str):
    """
    モデルの学習を行い，学習曲線を描画
    """
    recorder.plot(title)


def Q2(recorder:Recorder, y_pred:np.ndarray):
    """
    各種評価指標の出力
    """
    # Tensor -> NDArray
    val_y = recorder.val_y.cpu().detach().numpy()
    
    # 精度評価
    print('各クラスの適合率')
    print(precision_score(val_y, y_pred, average=None))
    print('各クラスの再現率')
    print(recall_score(val_y, y_pred, average=None))
    print('各クラスのF1スコア')
    print(f1_score(val_y, y_pred, average=None))
    print(f"マクロ平均の適合率   : {precision_score(val_y, y_pred, average='macro')}")
    print(f"マクロ平均の再現率   : {recall_score(val_y, y_pred, average='macro')}")
    print(f"マクロ平均のF1スコア : {f1_score(val_y, y_pred, average='macro')}")


def Q3(recorder:Recorder, y_pred:np.ndarray):
    """
    混同行列を出力
    """
    # 混同行列
    cm = confusion_matrix(recorder.val_y.cpu().detach().numpy(), y_pred, normalize='true')

    # グラフの描画
    sns.heatmap(cm, square=True, cbar=True, annot=True, cmap='Blues')
    
    plt.title('各クラスの正答率 (混同行列)')
    plt.xlabel("Predict", fontsize=13)
    plt.ylabel("Answer", fontsize=13)
    plt.tight_layout()

    plt.show()


def Q4(recorder:Recorder, val_x:np.ndarray, y_pred:np.ndarray):
    """
    モデルにとって簡単なデータと難しいデータ
    """
    def drawArgs(count:int, isDifficult:bool, axs, val_y, easyMask, easyIdx, difficultMask, difficultIdx):
        """
        draw()の引数を作成する
        """
        x = val_x[difficultMask][difficultIdx[count]] if isDifficult else val_x[easyMask][easyIdx[count]]
        vy = val_y[difficultMask][difficultIdx[count]] if isDifficult else val_y[easyMask][easyIdx[count]]
        yp = y_pred[difficultMask][difficultIdx[count]] if isDifficult else y_pred[easyMask][easyIdx[count]]

        if not isDifficult:
            return axs[isDifficult, count], x, vy, yp[vy]
        return axs[isDifficult, count], x, vy, yp[vy], yp.argmax(), yp[yp.argmax()]

    def draw(size, ax:Axes, x:np.ndarray, y_true, p_true, y_pred=None, p_pred=None):
        """
        一つ一つの数字を描画
        """
        ax.set_aspect('equal')
        ax.axis('off')
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        # １次元化しているため，reshape()で２次元に戻して描画
        ax.imshow(x.reshape(size, size))

        # タイトルを定義
        if y_pred is None:
            title = rf'$y=\hat!y|={int(y_true)}$' +'\n'+ \
                    rf'$p_{int(y_true)}=\hat!p|_{int(y_true)}={int(p_true*100)}$'
        else:
            title = rf'$y={int(y_true)}$, $\hat!y|={int(y_pred)}$' +'\n'+ \
                    rf'$p_{int(y_true)}={int(p_true*100)}$, $\hat!p|_{int(y_pred)}={int(p_pred*100)}$'
        ax.set_title(title.replace('!', '{').replace('|', '}'), y=1)
    

    # Tensor -> NDArray
    val_y = recorder.val_y.cpu().detach().numpy()
    # yの出力を確率に変換
    y_pred = softmax(y_pred)
    
    # それぞれの上位３件に当たるインデックスを取得
    counts = 3
    easyMask      = val_y == y_pred.argmax(axis=1)
    difficultMask = val_y != y_pred.argmax(axis=1)
    easyIdx      = np.argsort(y_pred[easyMask].max(axis=1))[-counts:]
    difficultIdx = np.argsort(y_pred[difficultMask].max(axis=1))[-counts:]

    # 描画
    fig = plt.figure(figsize=(5, 5.3))
    axs = fig.subplots(2, counts)
    size = int(np.sqrt(val_x.shape[1]))
    for isDifficult in [0, 1]:
        for i in range(counts):
            args = drawArgs(i, isDifficult, axs, val_y, easyMask, easyIdx, difficultMask, difficultIdx)
            draw(size, *args)
    
    plt.tight_layout()
    plt.show()


def single(x_train, y_train, x_val, y_val):
    """
    単層NNによる学習と各種検証
    """
    model = SingleLayer(x_train.shape[1]).to(device)
    optimizer = SGD(model.parameters(), lr=0.5)
    recorder = train(x_train, y_train, x_val, y_val, model, optimizer)
    # 学習曲線
    Q1(recorder, '単層NNによる学習曲線')
    # 検証データの予測結果
    y_pred:np.ndarray = recorder.lastModel(x_val).cpu().detach().numpy()
    # 精度評価
    Q2(recorder, y_pred.argmax(axis=1))
    # 混同行列
    Q3(recorder, y_pred.argmax(axis=1))
    # 紛らわしい事例
    Q4(recorder, x_val.cpu().detach().numpy(), y_pred)


def multi(x_train, y_train, x_val, y_val):
    """
    多層NNによる学習と各種検証
    """
    model = MultiLayer(x_train.shape[1]).to(device)
    optimizer = SGD(model.parameters(), lr=0.5)
    recorder = train(x_train, y_train, x_val, y_val, model, optimizer)
    # 学習曲線
    Q1(recorder, '多層NNによる学習曲線')
    # 検証データの予測結果
    y_pred:np.ndarray = recorder.lastModel(x_val).cpu().detach().numpy()
    # 精度評価
    Q2(recorder, y_pred.argmax(axis=1))
    # 混同行列
    Q3(recorder, y_pred.argmax(axis=1))
    # 紛らわしい事例
    Q4(recorder, x_val.cpu().detach().numpy(), y_pred)
    


if __name__ == "__main__":
    # GPUのあるPCで学習する場合は「cuda」そうでない場合は「cpu」
    device = 'cuda'

    # ソースデータの読み込み
    data = np.load(Path(__file__).parents[2]/'第5回'/'ans'/'Sources'/'MNIST'/'mnist.npz')
    x_train = torch.tensor(image_to_vector(data['train_x'])).type(torch.FloatTensor).to(device)
    y_train = torch.tensor(data['train_y']).type(torch.LongTensor).to(device)
    x_val   = torch.tensor(image_to_vector(data['test_x'])).type(torch.FloatTensor).to(device)
    y_val   = torch.tensor(data['test_y']).type(torch.LongTensor).to(device)


    # 単層NNによる学習
    single(x_train, y_train, x_val, y_val)

    # 多層NNによる学習
    multi(x_train, y_train, x_val, y_val)
