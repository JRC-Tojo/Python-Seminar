# 
# 3個目の課題の解答
# 分かりやすさ重視版
# 関数が大量に生成され，どこがどのような処理を担当しているのかが見通しにくくなってきていますね
# また，関数が多くなってくると色々なデータを引数ですべて渡していく必要があり，めんどくさい
# 実装の綺麗さ重視版の test3_1.py も合わせてご参照ください
# 

import re
from pathlib import Path
from statistics import mean

import numpy as np
from matplotlib import pyplot as plt


class Person:
    firstName = ''
    lastName  = ''
    age = 0
    sex = None 
    results = []

    def __init__(self, fname, lname, ageNum, sexStr, resultList) -> None:
        self.firstName = fname
        self.lastName = lname
        self.age = ageNum
        self.sex = sexStr
        self.results = resultList

    def show(self):
        """
        フィールドのデータをすべて表示する
        """
        # 野暮ったく (or python3.6未満を使って) 書くのであれば以下の通り
        # print('Fitst Name : ' + self.firstName)
        print(f'First Name : {self.firstName}')
        print(f'Last Name  : {self.lastName}')
        print(f'Age        : {self.age}')
        print(f'Results    : {self.results}')

    def __str__(self) -> str:
        """
        オブジェクトを直接printしたときにこの文字列が表示される
        実装でこれを活用する一例は test3_1.py の PersonCollection.compAge() を参照
        """
        return f'{self.firstName}, {self.lastName}, {self.age}, {self.results}'

    def fullName(self):
        """
        フルネームを表示する
        """
        print(f'{self.firstName} {self.lastName}')

    def checkSex(self):
        """
        性別についての情報を表示する
        """
        if (self.sex == 'male'):
            print(f'{self.lastName} は男です')
        else:
            print(f'{self.lastName} は女です')

    def getAve(self):
        """
        平均点を取得する
        """
        print(f'{self.lastName} が取得した点数の平均点は {mean(self.results):.1f}点 です')

    def compAge(self, person:object):
        """
        Personオブジェクトを引数にとり、そのPersonとの年齢を比較する
        person引数にPersonオブジェクト以外が渡ってくると、エラーで処理が落ちてしまう
        """
        if person.age > self.age:
            print(f'{person.lastName} のほうが {self.lastName} よりも年上です')
        elif person.age == self.age:
            print(f'{person.lastName} と {self.lastName} は同い年です')
        else:
            print(f'{person.lastName} のほうが {self.lastName} よりも年下です')

    def addResult(self):
        """
        テスト結果を追加する
        
        せっかくフルネームを計算しているのに，
        現状のfullName()の実装では計算結果を利用することができない
        """
        while True:
            newTestResult = input(f'{self.firstName} {self.lastName} に追加するテストの結果を入力してください\n')
            
            if re.match(r'[^0-9]+', newTestResult) or newTestResult == '':
                print('入力された値が数字（または整数）ではありません\n点数となる整数を入力してください')
                continue

            resultNum = int(newTestResult)
            
            if 0 > resultNum or resultNum > 100:
                print('点数は 0 ~ 100 のいずれかになります')
                continue

            break

        self.results.append(int(newTestResult))
        print(f'新しい点数 {resultNum} を結果に追加しました')

    def exportCsvLine(self) -> str:
        """
        csvファイルに結果を出力するためのデータ列を返す
        """
        resultContents = [
            self.firstName,
            self.lastName,
            self.age,
            self.sex
        ]
        resultContents.extend(self.results)

        result = ''
        for content in resultContents:
            result = result + f'{content},'

        return f'{result}\n'




def readFile(readPath):
    """
    datasetファイルを読み込み、Personオブジェクトのリストを生成する
    """
    persons = []
    with open(readPath, 'r') as f:
        lines = f.readlines()
        header = lines[0]
        # ヘッダーをスキップする
        for line in lines[1:]:
            lineContents = line.split(',')
            fname = lineContents[0]
            lname = lineContents[1]
            age = int(lineContents[2])
            sex = lineContents[3]
            results = []
            for content in lineContents[4:]:
                results.append(int(content))

            persons.append(Person(fname, lname, age, sex, results))
    
    return header, persons

def getNames(persons:list[Person]):
    """
    全員の名前を表示する
    """
    print('【All Persons】')
    for person in persons:
        person.fullName()

def addResults(persons:list[Person]):
    """
    全員のテスト結果を追加する
    """
    for person in persons:
        person.addResult()

def getHeader(header:str, persons:list[Person]):
    """
    ファイルを書き込む際のヘッダーデータを作成する
    """
    _header = header.split(',')[:4]
    _header.extend([f'Result {i+1}' for i in range(len(persons[0].results))])
    return f'{",".join(_header)}\n'

def export(savePath:str, header:str, persons:list[Person]):
    """
    csvファイルに結果を出力する
    """
    with open(savePath, 'w') as f:
        f.write(getHeader(header, persons))
        for person in persons:
            f.write(person.exportCsvLine())

    print(f'Saved person data at {savePath}')

def draw(savePath:str, persons:list[Person]):
    """
    回帰直線を含んだ結果を描く
    drawで使うデータの計算をここでやると非常に可読性が下がる（可読性＝見やすさ）
    """
    # 全員の年齢・平均点を導出する
    ages = []
    means = []
    for person in persons:
        ages.append(person.age)
        # getAve()メソッドがあるにも関わらず，それを使うことができないところが，メソッド内でprintする良くないところ
        # printしても良いが，基本的に計算した値は戻り値に入れておくことでその計算をメソッド内に隠蔽（カプセル化）することを意識する
        means.append(mean(person.results))

    # 回帰分析を行う
    sourceX = np.array(ages)
    sourceY = np.array(means)
    bar_x  = sourceX.mean()
    bar_y  = sourceY.mean()
    bar_xy = (sourceX * sourceY).mean()
    bar_x2 = (sourceX ** 2).mean()
    a = float((bar_xy - bar_x * bar_y) / (bar_x2 - bar_x**2))
    b = float(bar_y - a * bar_x)

    # 決定係数の導出
    predictY = a * sourceX + b
    upper = sum((sourceY - predictY) ** 2)
    lower = sum((sourceY - bar_y) ** 2)
    R2 = 1 - upper / lower

    # 描画処理
    # 本来であればここから下が描画処理でありメソッドがもっとも行うべきこと
    # オブジェクト指向的にはこれより上の処理は別のオブジェクトで計算されるべき
    # この辺の書き方の例はtest3_1.pyを参照のこと
    fig, ax = plt.subplots()
    ax.scatter(sourceX, sourceY, label='Source data')
    x = np.array([-10, 100])
    predictY2 = a * x + b
    ax.plot(x, predictY2, 'r', label='Predict Line')

    # テキスト表示位置の決定
    contentX = 40
    # 「予測した係数に値を適用する」という処理を何度も書いているのは良くない実装
    contentY = a * contentX + b + 15
    formula = r'$y=' + f'{a:.1f}' + 'x+' + f'{b:.1f}' + r'$'
    decided = r'$R^2=' + f'{R2:.3f}' + r'$'
    ax.text(contentX, contentY, f'{formula}\n{decided}', fontsize=14)

    ax.set_title('研究室メンバーの年齢と平均持ち点の関係', fontname="MS Gothic")
    ax.set_xlabel('年齢（歳）', fontname="MS Gothic")
    ax.set_ylabel('平均点', fontname="MS Gothic")
    ax.set_xlim([0, 70])
    ax.set_ylim(0)
    ax.grid()
    ax.legend()
    fig.savefig(savePath)
    print(f'Saved the graph at {savePath}')
    # plt.show()

if __name__ == '__main__':
    # csvファイルの読み込み
    dataPath = str(Path(__file__).parents[1]/'dataset.csv')
    header, persons = readFile(dataPath)

    # Personオブジェクトのリストに対する操作
    getNames(persons)
    # addResults(persons)

    # ファイルの書き込み
    savePath = str(Path(__file__).parent/'new_dataset.csv')
    export(savePath, header, persons)

    # グラフの描画
    savePath = str(Path(__file__).parent/'age-ave.png')
    draw(savePath, persons)

