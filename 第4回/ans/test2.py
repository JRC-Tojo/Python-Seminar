
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class Tankaiki:
    def __init__(self, sourceX:list[int], sourceY:list[float]) -> None:
        self.sourceX = np.array(sourceX)
        self.sourceY = np.array(sourceY)
        self.__predictLine()

    def __predictLine(self):
        """
        単回帰分析における係数a, bの導出
        """
        bar_x  = self.sourceX.mean()
        self.bar_y  = self.sourceY.mean()
        bar_xy = (self.sourceX * self.sourceY).mean()
        bar_x2 = (self.sourceX ** 2).mean()
        self.a = float((bar_xy - bar_x * self.bar_y) / (bar_x2 - bar_x**2))
        self.b = float(self.bar_y - self.a * bar_x)

    def predictLineFunc(self, x):
        """
        決定した関数の値を返す
        """
        return self.a * np.array(x) + self.b

    @property
    def R2f(self):
        """
        自由度調整済み決定係数
        説明変数は１つのみを想定しているため，常にk=1
        """
        n = len(self.sourceY)
        k = 1
        upper = sum((self.sourceY - self.predictLineFunc(self.sourceX)) ** 2) / (n-k-1)
        lower = sum((self.sourceY - self.bar_y) ** 2) / (n-1)
        return 1 - upper / lower

    def draw(self, savePath:str):
        """
        回帰直線を含んだ結果を描く
        今回の描画に特化した関数のため，タイトルなどの特有値をそのままハードコードしている
        """
        fig, ax = plt.subplots()
        ax.scatter(self.sourceX, self.sourceY, label='Source data')
        x = [-10, 100]
        ax.plot(x, self.predictLineFunc(x), 'r', label='Predict Line')

        contentX = 3.5
        contentY = 35
        formula = r'$y=' + f'{self.a:.1f}' + 'x' + f'{self.b:.1f}' + r'$'
        decided = r'$R^2_f=' + f'{self.R2f:.3f}' + r'$'
        ax.text(contentX, contentY, f'{formula}\n{decided}', fontsize=14)

        ax.set_xlabel('RM')
        ax.set_ylabel('Price')
        ax.set_xlim([3, 9.1])
        ax.set_ylim([3, 52])
        ax.grid()
        ax.legend()
        fig.savefig(savePath)
        print(f'Saved the graph at {savePath}')

class Jukaiki:
    def __init__(self, sourceX:list[int], sourceY:list[float], dim:int) -> None:
        self.sourceX = np.array(sourceX)
        self.sourceY = np.array(sourceY)
        self.dim = dim
        self.predictLine()

    def predictLine(self):
        """
        重回帰分析における係数a, bの導出
        """
        X = np.array([[ i**p for p in range(self.dim)] for i in self.sourceX ])
        self.w = np.linalg.inv(X.T @ X) @ X.T @ self.sourceY

    def predictLineFunc(self, x):
        """
        決定した関数の値を返す
        """
        return [np.array([ i**p for p in range(self.dim)]) @ self.w for i in np.array(x) ]

    @property
    def R2f(self):
        """
        自由度調整済み決定係数
        説明変数は１つのみを想定しているため，常にk=1
        """
        n = len(self.sourceY)
        k = 1
        bar_y = self.sourceY.mean()
        upper = sum((self.sourceY - self.predictLineFunc(self.sourceX)) ** 2) / (n-k-1)
        lower = sum((self.sourceY - bar_y) ** 2) / (n-1)
        return 1 - upper / lower

    def draw(self, savePath:str=None):
        """
        回帰直線を含んだ結果を描く
        今回の描画に特化した関数のため，タイトルなどの特有値をそのままハードコードしている
        """
        if savePath == None:
            savePath = str(Path(__file__).parent/'predictLine.png')

        fig, ax = plt.subplots()
        ax.scatter(self.sourceX, self.sourceY, label='Source data')
        x = np.linspace(0, 1, 100)
        ax.plot(x, self.predictLineFunc(x), 'r', label='Predict Line')

        ax.grid()
        ax.legend()
        fig.savefig(savePath)
        print(f'Saved the graph at {savePath}')
        plt.show()

class Ridge(Jukaiki):
    def __init__(self, sourceX: list[int], sourceY: list[float], dim: int, alpha:float) -> None:
        self.alpha = alpha
        super().__init__(sourceX, sourceY, dim)

    def predictLine(self):
        """
        重回帰分析における係数a, bの導出
        """
        X = np.array([[ i**p for p in range(self.dim)] for i in self.sourceX ])
        self.w = np.linalg.inv(X.T @ X + self.alpha * np.eye(self.dim)) @ X.T @ self.sourceY



if __name__ == "__main__":
    # 回帰のソース
    X = np.array([ 0.  ,  0.16,  0.22,  0.34,  0.44,  0.5 ,  0.67,  0.73,  0.9 ,  1.  ])
    Y = np.array([-0.06,  0.94,  0.97,  0.85,  0.25,  0.09, -0.9 , -0.93, -0.53,  0.08])
    
    # 重回帰
    jukaiki = Jukaiki(X, Y, 9)
    print(jukaiki.R2f)
    jukaiki.draw('')
    
    # リッジ回帰
    ridge = Ridge(X, Y, 9, 1)
    print(ridge.R2f)
    ridge.draw('')