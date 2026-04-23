# 
# Q1 HelloWorldと出力する
# Q2 キーボードから入力した数字を使い、「あなたは〇月生まれです」という出力を得るプログラムの作成
# Q3 ２つの数字を入力し、その数字同士の加減乗除、の結果を得る
# 

def Q1():
    print('Hello World')

def Q2():
    month = input('あなたの誕生月を入力してください\n')
    print(f'あなたは{month}月生まれです')

def Q3():
    firstNum = int(input('１つ目の数字を入力してください\n'))
    secondNum = int(input('２つ目の数字を入力してください\n'))
    print(f'和：{firstNum + secondNum}')
    print(f'差：{firstNum - secondNum}')
    print(f'積：{firstNum * secondNum}')
    print(f'商：{firstNum / secondNum :.2f}')

if __name__ == "__main__":
    Q1()
    Q2()
    Q3()