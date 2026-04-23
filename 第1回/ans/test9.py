# 
# シーザー暗号（カエサル暗号）の解読
# 

import re
import string
from pathlib import Path

from numpy import argmax


# 同系統の処理をまとめる意味でクラス化しているが、クラスを必ず使用する必要はない
class CaesarConverter:
    def encrypter(self, sentence:str, key:int) -> str:
        """
        受けた文字列を暗号化\n
        keyにはずらしたい分の数字を入力する
        """
        return self._shiftletters(sentence, key)

    def decrypter(self, sentence:str, key:int=None, keyLetter:str='e') -> str:
        """
        受けた文字列を復号化\n
        keyLetterには元の文で最も頻出のアルファベットを記入
        """
        if key == None:
            key = self._estimateKey(sentence, keyLetter)
        
        return self._shiftletters(sentence, -key)

    def _shiftletters(self, sentence:str, key:int) -> str:
        """
        指定された数字分、文字を後ろにずらす\n
        負の数がkeyに入った場合、文字を前にずらす
        """
        def shiftletter(letter:str):
            if re.match(r'[^a-z]', letter):
                return letter

            letterNum = ord(letter)
            if letterNum + key > ord('z'):
                return chr(ord('a') + (letterNum + key - ord('z')) - 1)
            elif letterNum + key < ord('a'):
                return chr(ord('z') + (letterNum + key - ord('a')) + 1)
            else:
                return chr(letterNum + key)

        return ''.join(map(shiftletter, sentence))

    def _estimateKey(self, sentence:str, keyLetter:str) -> int:
        """
        キーになる文字をもとに指定された文字列が平文からどの程度ずれているかを示す\n
        このメソッドでは英語の文章は原則として大文字よりも小文字で構成されることとしている\n
        全文大文字のパターンには対応していない
        """
        counter = []
        for letter in string.ascii_lowercase:
            counter.append(sentence.count(letter))

        # 最大値の要素のインデックスを取得
        maxIndex = argmax(counter)
        keyIndex = ord(keyLetter) - ord('a')

        return maxIndex - keyIndex


def readFile(path:str) -> str:
    with open(path, 'r') as f:
        sentence = ''.join(f.readlines())
    return sentence


def writeFile(path:str, lines:str) -> None:
    with open(path, 'w') as f:
        f.writelines(lines)


# ここまで使ってきたこのブロックについて，
# 本当は「このファイルをモジュールとして呼び出す場合に以下の実装は実行されない」という意味
if __name__ == '__main__':
    # 元の文章を記したファイルの読み込み
    sentencePath = str(Path(__file__).parent/'sentence_test9.txt')
    sentence = readFile(sentencePath)

    # カエサル暗号に関する処理を行うツールをクラス化
    converter = CaesarConverter()
    
    # 暗号化
    cryptography = converter.encrypter(sentence, 7)
    
    # 書き出し
    cryptographyPath = str(Path(__file__).parent/'cryptography_test9.txt')
    writeFile(cryptographyPath, cryptography)

    # 復号処理
    # print(converter.decrypter(cryptography))