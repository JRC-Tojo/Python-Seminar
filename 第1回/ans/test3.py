# 
# Q1 引数（数字）を一つ取り，その引数を標準入力の数自分足した値を返すメソッドを作成する
# Q2 作成したメソッドを使い，結果を表示する
# 

def Q1(arg1:int) -> int:
    addNum = int(input('数字を入力して下さい\n'))
    return arg1 + addNum


if __name__ == "__main__":
    print(Q1(10))
    