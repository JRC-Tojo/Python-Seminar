# 
# 3個目の課題の解答（別解）
# 実装の綺麗さ重視版
# test3.pyの実装とこちらの実装を比較して，どんなところに気を付けて実装しているか考えてみてください
# 使えそうな技術や書き方は積極的に盗んでいくことが上達の近道です
# 

import re
from pathlib import Path
from statistics import mean

import numpy as np
from matplotlib import pyplot as plt


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
    def R2(self):
        """
        決定係数
        """
        upper = sum((self.sourceY - self.predictLineFunc(self.sourceX)) ** 2)
        lower = sum((self.sourceY - self.bar_y) ** 2)
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

        contentX = 40
        contentY = self.predictLineFunc(contentX) + 15
        formula = r'$y=' + f'{self.a:.1f}' + 'x+' + f'{self.b:.1f}' + r'$'
        decided = r'$R^2=' + f'{self.R2:.3f}' + r'$'
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

class Person:
    def __init__(self, fname:str, lname:str, ageNum:int, sexStr:str, resultList:list[int]) -> None:
        """
        初期値の設定は原則、コンストラクタ内で行うため、この外で変数を宣言する必要はない
        """
        self.firstName = fname
        self.lastName = lname
        self.age = ageNum
        self.sex = sexStr
        self.results = resultList

    def __str__(self) -> str:
        return self.lastName

    def __lt__(self, __o: object) -> bool:
        """
        演算子のオーバーロード

        オブジェクト同士の大小関係を直接比較できるようにする
        
        今回は年齢でしか比較を行わないため，比較に使う値をageに設定している
        
        __eq__(), __gt__() も同様の特殊メソッド
        """
        if not isinstance(__o, Person):
            raise TypeError

        return self.age < __o.age

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Person):
            raise TypeError

        return self.age == __o.age

    def __gt__(self, __o: object) -> bool:
        if not isinstance(__o, Person):
            raise TypeError

        return self.age > __o.age

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

    def fullName(self):
        """
        フルネームを表示する

        基本的にprintするだけのメソッドは作成せず、その情報を外部に受け渡し、
        そこでprintなどの情報操作を行うべき
        """
        return f'{self.firstName} {self.lastName}'

    def checkSex(self):
        """
        性別についての情報を表示する

        これは本来フィールドに直接アクセスすれば良いものを，
        わざわざprintで体裁を整えて出力しているため，そのまま残す
        """
        if (self.sex == 'male'):
            print(f'{self.lastName} は男です')
        else:
            print(f'{self.lastName} は女です')

    def getAve(self):
        """
        平均点を取得する
        """
        return mean(self.results)

    def addResult(self):
        """
        テスト結果を追加する
        """
        while True:
            newTestResult = input(f'{self.fullName()} に追加するテストの結果を入力してください\n')
            
            if re.match(r'[^0-9]+', newTestResult) or newTestResult == '':
                print('入力された値が数字（または整数）ではありません\n点数となる整数を入力してください\n')
                continue

            resultNum = int(newTestResult)            
            if 0 > resultNum or resultNum > 100:
                print('点数は 0 ~ 100 のいずれかになります\n')
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
            self.sex,
            *self.results
        ]
        return f'{",".join(iter(map(str, resultContents)))}\n'

class PersonCollection:
    """
    Personオブジェクトをまとめたクラスを作ることで，オブジェクトのリスト全体に対する処理を一元化する
    """
    def __init__(self, readPath:str) -> None:
        self.__readFile(readPath)

    def __readFile(self, readPath):
        """
        datasetファイルを読み込み、Personオブジェクトのリストを生成する
        
        Personオブジェクトのリストをクラス内で管理することで，想定外の操作が行われることを防止する
        
        __で外からアクセスできないメソッドになる
        """
        self.persons:list[Person] = []
        with open(readPath, 'r') as f:
            lines = f.readlines()
            self.header = lines[0]
            # ヘッダーをスキップする
            for line in lines[1:]:
                lineContents = line.split(',')
                fname = lineContents[0]
                lname = lineContents[1]
                age = int(lineContents[2])
                sex = lineContents[3]
                results = list(map(int, lineContents[4:]))

                self.persons.append(Person(fname, lname, age, sex, results))

    def compAge(self, index1, index2):
        """
        指定したインデックスのPersonを比較する
        
        以前はageフィールドにアクセスして比較していたが，オブジェクトを直接比較している
        
        オブジェクトが直接参照されたときにlastNameを返すように__repr__を実装している
        """
        person1 = self.persons[index1]
        person2 = self.persons[index2]
        if person1 > person2:
            print(f'{person1} のほうが {person2} よりも年上です')
        elif person1 == person2:
            print(f'{person1} と {person2} は同い年です')
        else:
            print(f'{person1} のほうが {person2} よりも年下です')


    def getNames(self):
        """
        全員の名前を取得する
        """
        return list(map(lambda x: x.fullName(), self.persons))

    def getAges(self):
        """
        全員の年齢を取得する
        """
        return list(map(lambda x: x.age, self.persons))

    def getMeans(self):
        """
        全員の平均点を取得する
        """
        return list(map(lambda x: x.getAve() , self.persons))

    def addResults(self):
        """
        全員のテスト結果を追加する
        """
        for person in self.persons:
            person.addResult()

    def __getHeader(self):
        """
        Headerの項目を調整する
        今回は増やすメソッドしか実装しておらず，Collectionを通してpersonsを操作しているため，どれか一つだけResultsのデータが増えることはない
        よって，代表Person１つのResultsの長さを基準にHeaderを決定する
        """
        header = self.header.split(',')[:3]
        header.extend([f'Result {i+1}' for i in range(len(self.persons[0].results))])
        return f'{",".join(header)}\n'

    def export_csv(self, savePath):
        """
        csv出力する
        """
        with open(savePath, 'w') as f:
            f.write(self.__getHeader())
            for person in self.persons:
                f.write(person.exportCsvLine())

        print(f'Saved person data at {savePath}')


        
if __name__ == '__main__':
    # CSVファイルの読み込み
    dataPath = str(Path(__file__).parents[1]/'dataset.csv')
    collection = PersonCollection(dataPath)

    # ３番目と４番目に格納されたPersonの年齢を比較
    collection.compAge(3, 4)

    # Personオブジェクトのリストに関する操作
    print('【All Persons】')
    print(*collection.getNames(), sep='\n')
    # collection.addResults()

    # CSVに書き出し
    savePath = str(Path(__file__).parent/'new_dataset.csv')
    collection.export_csv(savePath)

    # 単回帰分析に基づく描画
    tankaiki = Tankaiki(collection.getAges(), collection.getMeans())
    savePath = str(Path(__file__).parent/'age-ave.png')
    tankaiki.draw(savePath)
