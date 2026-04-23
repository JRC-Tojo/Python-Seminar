# 
# Vector2Dクラスを作成する
# 

class Vector2D:
    def setVec(self, x:float, y:float):
        self.x = x
        self.y = y

    def getAbs(self):
        return (self.x**2 + self.y**2)**(1/2)

    def getNormVec(self):
        size = self.getAbs()
        return self.x/size, self.y/size

    def addVec(self, otherVec:list[float, float]):
        return self.x+otherVec[0], self.y+otherVec[1]

    def subVec(self, otherVec:list[float, float]):
        return self.x-otherVec[0], self.y-otherVec[1]
    
    def innerProd(self, otherVec:list[float, float]):
        return self.x*otherVec[0] + self.y*otherVec[1]


if __name__ == "__main__":
    # Vector2Dオブジェクトの宣言
    vecCalc = Vector2D()

    # 初期ベクトルを定義
    vecCalc.setVec(3, 5)

    # メソッドを使ってみる
    print(vecCalc.getAbs())

    # 計算してみる
    print(vecCalc.addVec([-4, 10]))