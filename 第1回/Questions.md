> [出題時のScrapbox](https://scrapbox.io/actscape-seminar/%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%82%BC%E3%83%9F%E2%88%92%EF%BC%91)

# 1. VSCode, Pythonの導入

本年から主に[Visual Studio Code (VSCode)](https://azure.microsoft.com/ja-jp/products/visual-studio-code/?cdn=disable)を用いる．

これはプログラムを作成するために使用するツールであることから，必ずアプリをインストール，セットアップすること．

> 参考サイト：[Python 環境へのパッケージのインストール](https://docs.microsoft.com/ja-jp/visualstudio/python/tutorial-working-with-python-in-visual-studio-step-05-installing-packages?view=vs-2022)

各設問にて必要なライブラリが明記されている場合はその指示に沿ってライブラリを導入

> 参考サイト：[Python ライブラリのインストール](https://docs.python.org/ja/3/installing/index.html)



# 2. 標準入力、標準出力

1. HelloWorldと出力する

1. キーボードから入力（＝標準入力）した数字を使い、「あなたは〇月生まれです」と出力する

1. 2つの数字を標準入力し、その数字同士の加減乗除の結果を得る

    ```
    (コンソール表示の例)

    1つめの数字を入力してください >>> 3
    2つめの数字を入力してください >>> 7
    四則演算の結果は以下の通りです
    3 + 7 = 10
    3 - 7 = -4
    3 * 7 = 21
    3 / 7 = 0.43  (<- 割り算は最初の2ケタのみを表示するようにする)
    ```



# 3. メソッドの宣言と利用

1. 引数のあるメソッドを作成する

    - 引数は数字（整数）１つ

    - メソッド内で標準入力をとり、その入力された数字と引数の和を計算する

    - 計算した和を戻り値とする

1. 作成したメソッドを使い，結果を表示する（実行する）



# 4. 配列の活用、for文の活用

1. 配列を宣言し，それを表示する

1. 作った配列を一つ一つ表示する

1. 作った配列に要素を追加する

1. range(n)を利用して九九の表を「きれいに」作成する

    ```
    (九九の表の例)

    1       2       3       4       5       6       7       8       9

    2       4       6       8       10      12      14      16      18

    3       6       9       12      15      18      21      24      27

    4       8       12      16      20      24      28      32      36

    5       10      15      20      25      30      35      40      45

    6       12      18      24      30      36      42      48      54

    7       14      21      28      35      42      49      56      63

    8       16      24      32      40      48      56      64      72

    9       18      27      36      45      54      63      72      81
    ```



# 5. import（組み込み）の活用（datetime）

1. 今日の日付を表示してみる

    - 日付に関連する処理は「datetime」というライブラリを用いる

    - プログラムではライブラリを使用するとき，プログラムの最初に「このライブラリを使います」と宣言する必要がある

    - Pythonではライブラリを宣言するときには「import」を使い，今回の場合はプログラムの冒頭に`from datetime import datetime`と記入する

2. 書式を指定して今日の日付を表示してみる

    ```
    (日付表示の例)

    日本式 -> 0000年00月00日
    外国式 -> 00/00/0000
    ```



# 6. import（外付け）の活用（numpy）
## Basic Guide

- numpyとは，Pythonにおいて行列やリストにおける数値計算を簡単に行うための計算ライブラリである．

- numpyでは通常の配列とは異なり，NDArrayと呼ばれる特殊な配列を利用する．

- NDArrayについての基本的な利用方法は下記の通り．

    ```python
    # pip install numpy によってNumpyをPCにインストールしておく必要がある
    import numpy as np

    # 任意の配列を宣言する
    sampleList = [1, 2, 3]

    # 配列をNDArrayに変換する
    numpyList = np.array(sampleList)
    # 順番に並ぶ連番をNDArrayで宣言したいときには以下の方が良い
    # numpyList = np.arange(1, 4)

    # NDArrayのサイズを確認したいとき
    print(numpyList.shape)

    # NDArrayを使うと，宣言した変数の後ろに「.」をつけて便利なツール(=メソッド)を呼び出せる
    # 例えば，合計を算出したいとき
    print(numpyList.sum())

    # 一部のツール(=メソッド)は以下のように呼び出すことも可能
    # ツールによってどちらも対応していたり，下記のパターンしか対応していなかったりする
    print(np.sum(numpyList))
    ```


1. numpyにおける配列である「NDArray」を宣言し，上記のサンプルコードを動かしてみる

    - `sampleList`と`numpyList`の両方を作成しておき，これらを以下の設問で使う配列とする

以下，Numpyを使った実装と，使わなかった実装の両方を作成すること
<hr/>

1. 要素の平均を出力する

1. 要素の最大値・最小値を出力する

1. 要素の最大・最小値のあるインデックスを出力する

1. `sampleList`や`numpyList`のほかにもう１つ配列を作成し，それらを行列(ベクトル)と見たときの四則演算（足し算、引き算、行列積、アダマール積）を算出する



# 7. import（外付け）の活用（matplotlib）
## Basic Guide

- MatplotLibはPythonにおいて図を描画する際の標準的なライブラリである

- 棒グラフや折れ線グラフといった様々なグラフを簡単に描画することができる

- 多くのプログラム作成者において，極めて基本的なライブラリであることから，Pandasをはじめとした様々な別のライブラリとの互換性が高いため，まずはこのライブラリを勉強するべき

- 図の描画ではこのほかに，オシャレで綺麗な図を描画することのできる[Plotly](https://plotly.com/)なども有名

- 一般的な折れ線グラフのテンプレートは以下のようなプログラムで出力可能

    ```python
    # pip install matplotlib によってmatplotlibをPCにインストールしておく必要がある
    import matplotlib.pyplot as plt
    import numpy as np
    # グラフに日本語を入れる場合は以下も宣言
    # pip install japanize-matplotlibとしてPCにインストールしておく
    import japanize_matplotlib


    # 適当な10件の推移データを乱数により作成
    # この値が折れ線グラフのy座標になる
    sampleData = np.random.randint(0, 100, 10)

    # 上で生成したy座標に対応するx座標を生成する
    # 単純な0, 1, 2, ...として生成
    samplePos = np.linspace(0, sampleData.shape[0], sampleData.shape[0])

    # 折れ線グラフを定義
    # Matplotlibでは第3引数はFormat Stringsと呼ばれ，グラフの恰好を定義できる
    # （詳細は https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html の後半を参照）
    plt.plot(samplePos, sampleData, '--or', label='適当なサンプルデータ')

    # タイトルを定義
    plt.title('適当な遷移データの折れ線グラフ')

    # それぞれの軸に名前をつける
    # $で囲むことで，その中身をLateX形式で記述できる
    plt.xlabel('時間 [$s$]')
    plt.ylabel('面積 [$m^2$]')

    # 凡例を表示
    plt.legend()

    # 図を描画
    plt.show()
    ```

1. 上記のサンプルを棒グラフに変更した図を作成する

1. 以下に示す各教科の受講者人数についてのデータセットについて各設問を実装せよ

    |subject|counts (人)|
    |:---:|:---:|
    |音楽|65|
    |美術|48|
    |書道|10|

    1. データセットに基づいた円グラフを作成せよ

    1. 全実技科目受講者のうち経験者は37人であるという．<br/>このことが分かる円グラフを1.の円グラフの右横に描画せよ

    1. 各教科の受講者に追加のアンケートを行った結果，それぞれの教科における経験者，未経験だが興味がある，なんとなく参加，の人数が以下の通り明らかになった．<br/>「それぞれの教科受講者のうち」ということが分かりやすいように円グラフを描画せよ

        |subject|Type|counts (人)|
        |:---:|:---:|:---:|
        ||経験者|13|
        |音楽|興味あり|37|
        ||なんとなく|15|
        ||||
        ||経験者|5|
        |美術|興味あり|8|
        ||なんとなく|35|
        ||||
        ||経験者|1|
        |書道|興味あり|5|
        ||なんとなく|4|

1. 平均が50で標準偏差が10の正規分布に従う値を30000個生成し，ヒストグラムを描画．

    - 正規分布に従う乱数の生成には`np.random.normal(loc, scale, size)`が便利

    - ヒストグラムは`plt.hist(x)`で宣言できる

1. 上記のヒストグラムを各階級の値で累積していったヒストグラムを描画

    - 単純に累積すると，y軸の値が非常に大きくなるため，`density=True`を`hist(x)`の引数に入れることで値を正規化しておくと見やすい



# 8. if文・条件文の活用

1. 引数に数字を渡し，その数字が偶数か否かを判別する関数を作成する

1. 任意の配列に格納されたそれぞれの値について，3で割って整数になるもののみを抽出した配列を返す関数を作成する

1. 10^6までの素数を出力するプログラムを作成する（推奨実行時間0.5秒以内）

    - 実行時間（表示にかかる時間を除く）の求め方は以下の通り

    - primes(endNum)で計算を行い、その結果をresultが受けるものとする

    ```python
    import time

    def primes(endNum:int):
        """
        endNumで指定した値までに含まれる素数の配列を返す
        """
        pass
    

    if __name__ == '__main__':
        endNum = 10**6

        startTime = time.time()
        result = primes(endNum)
        endTime = time.time()
        
        print(result)
        print(f'計算時間：{endTime - startTime:.3f}s')
    ```



# 9. 暗号解読

以下の暗号文を復号（もとの読める文章に直すこと）しなさい

```
Tv jvuzpkly aol klclsvwtlua vm byihu hylhz huk mbabyl wshuupun, pa pz ptwvyahua av huhsfgl aol tpjyv shuk bzl ayhuzpapvu vm hyjopaljabyhs bupaz. Tol wbywvzl vm aopz zabkf pz av klclsvw h thjopul slhyupun tvkls av lzapthal ibpskpun afwl myvt ibpskpun uhtl huk viahpu tpjyv shuk bzl ayhuzpapvu khah.
Hvbzpun thwz ohcl h opno wvaluaphs mvy aol huhsfzpz vm ayhuzpapvu, iba zbjo khah kvlz uva pujsbkl h ibpskpun afwl. Wl bzl nlv-jvvykpuhalk wovul ivvr huk Gvvnsl Pshjl API, dopjo pujsbkl ivao ibpskpun uhtlz huk aolpy afwlz, hz ayhpupun khah.
Iu khah wylwyvjlzzpun, aol ibpskpun uhtlz hyl kpcpklk puav dvykz if MlChi, huk lhjo dvyk pz jvuclyalk puav h cljavy if Wvyk2Vlj. Uzpun TF-IDF, lhjo dvyk dhz tlynlk puav h bupmplk cljavy, dlpnoalk hjjvykpun av aol mylxblujf vm pa. Tolu, dl bzlk Rhukvt Fvylza, dopjo pz hisl av nla hjjbyhjf huk aol ylzbsaz jhu il cpldlk hz h kljpzpvu ayll.
Tol ahynla hylh pz aol jpaf jlualy, dolyl tpelk ibpskpun afwlz hyl vizlyclk, huk aol afwlz dlyl jshzzpmplk puav zpe afwlz. Iujylhzpun aol ubtily vm byihu hylhz pu aol ayhpupun khah ptwyvclz aol hjjbyhjf, iba aol yhal vm ptwyvcltlua kljylhzlk hmaly hivba 10 byihu hylhz. Tol mpuhs hjjbyhjf vm tvyl aohu 80% dhz hjoplclk zahisf.
```


## HINT

- (これを見ずに出来たらすごいけど、これを見て完璧にもとに戻せれば十分)

- 暗号の種別はシーザー暗号（カエサル暗号）

- シーザー暗号とは文字を数字で表した際に、適当な数だけずらした文字に置き換える暗号化手法である
    - ａ＝１に対して、４つずらすとｅ＝５になる

    - ｆ＝６に対して、ー３つずらすとｃ＝３になる

    - ｚ＝２６に対して、２つずらすとｂ＝２になる（はみ出した分はループする）

    - 今回は小文字に対してのみこのルールを適用して暗号化しており、大文字や数字などの他の文字はそのまま
- **実は、英語の文章では一般的に「ｅ」が最も多く出てくるアルファベット（今回の文章もｅが最も多く登場する）**

- 文字を数字に直すときは`ord('A')`のようにすることで数字（この場合は65）が得られる

- 数字を文字に直すときは`chr(65)`のようにすることで文字（この場合はＡ）が得られる

- 適当な文字列がtestStrという変数に入っているとき、testStr.count('a')とすることで文章中の小文字のaの個数を得ることができる

- 適当な一文字（`letter`）が小文字のアルファベットか否かを調べるプログラムは以下の通り

```python
import re

if re.match(r'[^a-z]', letter):
    # letterが小文字ではない時に実行
else:
    # letterが小文字の時に実行
```