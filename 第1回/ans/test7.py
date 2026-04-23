import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib


def plot(x, y, title:str, xlabel:str, ylabel:str, dataLabel:str=None):
    """
    任意のx, yに対して折れ線グラフを描画する

    - 引数に「=None」としている部分はオプション引数と呼ばれ，
    当該引数について指定がなかった場合は＝で指定された値を関数内の処理で用いる
    """
    plt.plot(x, y, '--or', label=dataLabel)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title)
    plt.legend()
    plt.show()


def Q1(x, y, title:str, xlabel:str, ylabel:str, dataLabel:str=None):
    """
    任意のx, yに対して棒グラフを描画する
    """
    plt.bar(x, y, label=dataLabel)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title)
    plt.legend()
    plt.show()


def Q2_1(x, names, title:str):
    """
    任意の個数データ`x`に対して円グラフを描画する

    それぞれの個数に対応する名称を`names`で指定する
    """
    plt.pie(x=x, labels=names, autopct='%1.1f%%')

    plt.title(title)
    plt.show()


def Q2_2(x1, names1, x2, names2, title:str):
    """
    任意の２つの個数データ`x1`, `x2`に対して円グラフを２つ並べて描画する
    """
    # 正式な作成方法はこのようにplt.figure()を宣言する方法
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2 , 1)
    ax1.pie(x=x1, labels=names1, autopct='%1.1f%%')
    
    ax2 = fig.add_subplot(1, 2 , 2)
    ax2.pie(x=x2, labels=names2, autopct='%1.1f%%')

    # ２つのグラフを使うときはこのようにタイトルを設定する
    fig.suptitle(title)

    # plt.tight_layout() は無駄な余白を削って画面サイズに図をフィットさせる
    plt.tight_layout()

    plt.show()


def Q2_3(x, names, innerX:dict, innerNames:dict, title:str):
    """
    任意の個数データ`x`について，それらの内訳`innerX`を同時に描画する

    `innerX`は辞書で指定し，その使い方は答えとして記載の通り
    """
    x2 = [innerX[name] for name in names]
    names2 = [innerNames[name] for name in names]

    # x2が現状では2次元になってしまっているため，これを1次元に直す
    # 今回は最も記述量の少ないやり方にしているが，素直に別の配列を作成して，forで回しながらそこに追加しても良い
    x2 = sum(x2, [])
    names2 = sum(names2, [])

    # 円グラフの色を決定する
    # 実際には自分で指定しても良いが，本メソッドでは自動で指定する
    colorSteps = np.linspace(0, 1, len(x))
    outerColors = mpl.colormaps['tab10'](colorSteps)[:, :3]
    innerColors = [np.insert(oColor, 3, 1/(len(_x)+2)*(i+1)).tolist() for oColor, _x in zip(outerColors, innerX.values()) for i in range(len(_x))]

    wedgeprops = {'width': 0.3, 'edgecolor':'white'}
    plt.pie(x=x,  labels=names,  autopct='%1.1f%%', colors=outerColors, wedgeprops=wedgeprops, radius=1.3, pctdistance=0.9)
    plt.pie(x=x2, labels=names2, autopct='%1.1f%%', colors=innerColors, wedgeprops=wedgeprops, labeldistance=0.75)

    plt.title(title)
    plt.show()


def Q3(x, cumulative=False):
    """
    任意のデータに対してヒストグラムを描画する

    - `cumulative`: 各階級のデータを累積したヒストグラムを描画する
    """
    plt.hist(x, cumulative=cumulative, density=cumulative)
    plt.show()


if __name__ == "__main__":
    # 設問１
    sampleData = np.random.randint(0, 100, 10)
    samplePos = np.linspace(0, sampleData.shape[0], sampleData.shape[0])
    plot(samplePos, sampleData, '適当な遷移データの折れ線グラフ', '時間 [$s$]', '面積 [$m^2$]', '適当なサンプルデータ')
    Q1(samplePos, sampleData, '適当な遷移データの折れ線グラフ', '時間 [$s$]', '面積 [$m^2$]', '適当なサンプルデータ')

    #########################################################################################################################
    # 設問２
    # 小問１：基本的な円グラフ
    peopleCounts = [65, 48, 10]
    subjectNames = ['音楽', '美術', '書道']
    Q2_1(peopleCounts, subjectNames, '各教科の受講者人数')

    # 小問２：2つ横並びの円グラフ
    experiencedPeoples = 37
    x2 = [experiencedPeoples, sum(peopleCounts)-experiencedPeoples]
    names2 = ['経験者', '未経験者']
    Q2_2(peopleCounts, subjectNames, x2, names2, '各教科の受講者人数')

    # 小問３：内包型の円グラフ
    innerPeopleCounts = {
        '音楽': [13, 37, 15],
        '美術': [5, 8, 35],
        '書道': [1, 5, 4],
    }
    innerName = ['経験者', '興味あり', 'なんとなく']
    innerNames = {'音楽': innerName, '美術': innerName, '書道': innerName}
    Q2_3(peopleCounts, subjectNames, innerPeopleCounts, innerNames, None)

    #########################################################################################################################
    # 設問３，４
    sampleX = np.random.normal(50, 10, 30000)
    # 設問４は第2引数をTrueにしたパターン
    Q3(sampleX, False)

