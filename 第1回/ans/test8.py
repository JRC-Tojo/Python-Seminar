# 
# Q1 引数に数字を渡し，その数字が偶数か否かを判別するメソッドを作成する
# Q2 0 ~ 99の整数を持つ配列を3で割って整数になるもののみを抽出した配列を返すメソッドを作成する
# Q3 10^6までの素数を出力するプログラムを作成する（推奨実行時間0.5秒以内）
# 

import time
import numpy as np


def Q1(arg1:int) -> str:
    if arg1 % 2 == 0:
        return 'これは偶数です'
    else:
        return 'これは奇数です'

def Q2(checkList:list) -> list[int]:
    resultList = []
    for item in checkList:
        if item % 3 == 0:
            resultList.append(item)

    return resultList

def Q2_1(checkList:np.ndarray) -> list[int]:
    """
    Q2()の別解 (checkListをNDArrayで宣言する必要あり)
    """
    return checkList[checkList % 3 == 0]

def Q3(endNum:int) -> list[int]:
    """
    エラトステネスの篩によって素数を算出する
    >>> endNum = i * iであった場合、iまでの数について篩にかければそこから先については素数のみが残っているはず
    
    これにより、小さい数から順にループを回していき、出てきた数の倍数を削除しつつ、出てきた数についてはresultNumsに保管\n
    i (= sqrtEndNum) までこの操作を繰り返したら、numbersに残っている数はすべて素数\n
    resultNumsとnumbersの残りを合体させたものが求める素数のリストになる
    """
    sqrtEndNum = np.sqrt(endNum)
    numbers = np.arange(2, endNum + 1)
    resultNums = []

    while numbers[0] <= sqrtEndNum:
        firstNum = numbers[0]
        resultNums.append(firstNum)
        numbers = numbers[numbers % firstNum != 0]
    resultNums.extend(numbers)
    
    return resultNums

def Q3_1(endNum:int):
    """
    Q3の別解
    
    (Q3と同様にエラトステネスの篩を使っているが，連番数字を格納した配列を直接操作することで実行速度を向上した)
    """
    from math import ceil

    nums = np.arange(2, endNum)

    for i in nums[0:ceil(endNum**0.5)]:
        if i:
            nums[2*i-2:endNum:i] = 0

    result = nums[nums != 0]

    return result



if __name__ == "__main__":
    # 設問１，２
    Q1(5)
    Q2([i for i in range(100)])
    Q2_1(np.arange(100))

    #############################################################################
    # 設問３：素数の列挙
    startTime = time.time()
    result = Q3(10**6)
    # result = Q3_1(10**7)
    endTime = time.time()

    # 表示項目を抑えるためにnumpyでラップ（単純な実装という意味ではラップの必要なし）
    print(np.array(result))
    print(f'計算時間：{endTime - startTime:.3f}s')