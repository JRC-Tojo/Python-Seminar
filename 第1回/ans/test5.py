# 
# Q1 今日の日付を表示
# Q2 書式を指定して今日の日付を表示
# 

from datetime import datetime
from typing import Literal

def Q1() -> datetime:
    """
    書式を指定せずに今日の日付を表示
    """
    return datetime.now()

def Q2(showType:Literal['japan', 'foreign']):
    """
    書式を指定して今日の日付を表示
    """
    nowDate = Q1()
    if showType == 'japan':
        dateStr = nowDate.strftime('%Y年%m月%d日')
    elif showType == 'foreign':
        dateStr = nowDate.strftime('%m/%d/%Y')
    else:
        # 引数に変なものが入ってきたときにはエラーを出してはじく（発展編）
        raise ValueError(
            f'Invalid argument ({showType}) is detected.'
        )
    
    return dateStr


if __name__ == "__main__":
    print(Q1())
    print(f"日本式 -> {Q2('japan')}")
    print(f"外国式 -> {Q2('foreign')}")