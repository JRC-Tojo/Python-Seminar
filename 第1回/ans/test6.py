# 
# Q1 numpyのサンプルコードを動かす
# 
# Q1'. 要素の平均を出力する
# Q2'. 要素の最大値・最小値を出力する
# Q3'. 要素の最大値・最小値のインデックスを出力する
# Q4'. ベクトル同士の四則演算を出力する
# 

import numpy as np

def Q1(nList:np.ndarray):
    print(nList.shape)
    print(nList.sum())
    print(np.sum(nList))

def Q1_list(sList:list):
    """
    与えられた配列の平均を出力する (list版)
    """
    return sum(sList) / len(sList)

def Q1_ndarray(nList:np.ndarray):
    """
    与えられた配列の平均を出力する (NDArray版)
    """
    return nList.mean()

def Q2_list(sList:list):
    """
    与えられた配列の最小, 最大値を出力する (list版)
    """
    return min(sList), max(sList)

def Q2_ndarray(nList:np.ndarray):
    """
    与えられた配列の最小, 最大値を出力する (NDArray版)
    """
    return nList.min(), nList.max()

def Q3_list(sList:list):
    """
    与えられた配列の最小, 最大値のインデックスを出力する (list版)
    """
    return sList.index(min(sList)), sList.index(max(sList))

def Q3_ndarray(nList:np.ndarray):
    """
    与えられた配列の最小, 最大値のインデックスを出力する (NDArray版)
    """
    return nList.argmin(), nList.argmax()

def Q4_list(sList1:list, sList2:list):
    """
    ベクトルの四則演算を行う (list版)
    """
    # このような[]の中にforを書いて配列を宣言する手法を「リスト内包」という
    # zipで指定した複数の配列はforで同時にループさせることができる
    sumLists = [s1 + s2 for s1, s2 in zip(sList1, sList2)]
    subLists = [s1 - s2 for s1, s2 in zip(sList1, sList2)]
    admLists = [s1 * s2 for s1, s2 in zip(sList1, sList2)]
    mulLists = sum(admLists)

    return sumLists, subLists, mulLists, admLists

def Q4_ndarray(nList1:np.ndarray, nList2:np.ndarray):
    """
    ベクトルの四則演算を行う (NDArray版)
    """
    sumLists = nList1 + nList2
    subLists = nList1 - nList2
    mulLists = nList1 @ nList2
    admLists = nList1 * nList2

    return sumLists, subLists, mulLists, admLists


if __name__ == "__main__":
    # 任意の配列を宣言する
    sampleList = [1, 2, 3]

    # 配列をNDArrayに変換する
    numpyList = np.array(sampleList)

    Q1(numpyList)

    print(Q1_list(sampleList))
    print(Q1_ndarray(numpyList))
    
    print(Q2_list(sampleList))
    print(Q2_ndarray(numpyList))

    print(Q3_list(sampleList))
    print(Q3_ndarray(numpyList))

    sampleList2 = [6, 4, 2]
    numpyList2  = np.array(sampleList2)
    print(Q4_list(sampleList, sampleList2))
    print(Q4_ndarray(numpyList, numpyList2))
    