# 
# Q1 配列を宣言し，それを表示する
# Q2 作った配列を一つ一つ表示する
# Q3 作った配列に要素を追加する
# Q4 range(n)を利用して九九の表を「きれいに」作成する
# 


firstList = [1, 2, 3, 4]

def Q1():
    print(firstList)

def Q2():
    for item in firstList:
        print(item)

def Q3():
    firstList.append(5)
    print(firstList)

def Q4():
    for i in range(1, 10):
        for j in range(1, 10):
            print(i*j, end='\t')
        print()
        print()

if __name__ == "__main__":
    Q1()
    Q2()
    Q3()
    Q4()