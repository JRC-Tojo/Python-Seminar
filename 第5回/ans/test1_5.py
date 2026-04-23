# 
# 機会学習帳５章の解答
# 確率的勾配法の実装についてはtest1_6.pyから呼び出しているため，そちらを参照
# 

import collections
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer

from test1_6 import SGDClassifier


################################## データ読み込み～ベクトル化は機械学習帳と同じ ##################################

def tokenize(s):
    return [t.rstrip('.') for t in s.split(' ')]

def vectorize(tokens):
    return collections.Counter(tokens)

def readiter(fi):
    for line in fi:
        fields = line.strip('\n').split('\t')
        x = vectorize(tokenize(fields[1]))
        y = fields[0]
        yield x, y


with open(str(Path(__file__).parent/'Sources'/'Spam'/'SMSSpamCollection'), encoding='utf-8') as fi:
    D = [d for d in readiter(fi)]

Dtrain, Dtest = train_test_split(D, test_size=0.1, random_state=0)

VX = DictVectorizer(sparse=False)
VY = LabelEncoder()

Xtrain = VX.fit_transform([d[0] for d in Dtrain])
Ytrain = VY.fit_transform([d[1] for d in Dtrain])
Xtest = VX.transform([d[0] for d in Dtest])
Ytest = VY.transform([d[1] for d in Dtest])

################################## ここまでは同じ ##################################

# 学習
sgd = SGDClassifier()
sgd.fit(Xtrain, Ytrain)

# モデルの保存を行ったり，作成したモデルを読み込む場合は以下のコメントを利用
# sgd.export(f'_{sgd.finalEpoch}')
# sgd.load('_501600')

# 予測結果 & 精度評価
print(sgd.predict_proba(Xtest[0]))
print(sgd.predict(Xtest))
print(sgd.score(Xtest, Ytest))

# Spamか否かを判別する際に特に重視している単語を一覧表示する
F = sorted(zip(VX.feature_names_, sgd.coef_[0]), key=lambda x: x[1])
print('Top 20 (ham)')
print(*F[:20], sep='\n')
print()
print('Top 20 (spam)')
print(*F[-20:], sep='\n')