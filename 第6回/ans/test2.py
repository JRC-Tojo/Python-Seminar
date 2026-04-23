# 
# 応用課題の解答
# 

from typing import ClassVar
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
from tqdm import tqdm

# pandasのWarningを黙らせる
warnings.simplefilter(action='ignore')

# 一般的に，グローバル変数は全ての文字を大文字で定義する
# 列名を一般化しておき，データが変わってもプログラムを動かせるようにしておく
COLUMNs = {
    'userID': 'ユーザーID',
    'tripID': 'トリップID',
    'createTime': '作成日時',
    'recordTime': '記録日時',
    'departureTime': '出発時刻',
    'arrivalTime': '到着時刻',
    'lat': '緯度',
    'lon': '経度',
    'height': '高度',
    'bearing': 'bearing',
    'speed': 'speed',
    'transportCode': '移動手段コード',
    'objectiveCode': '目的コード（active）'
}

class Trip:
    """
    １トリップにおけるデータを保管する
    １トリップ分のDataFrameを渡せば，勝手に必要な情報を抽出して格納する
    """
    def __init__(self, loc:pd.DataFrame, objective=0) -> None:
        self.objective = objective
        self.tripData = loc

    @property
    def startPos(self):
        """
        トリップのはじめの地点の座標を取得する
        """
        return self.tripData[[COLUMNs['lat'], COLUMNs['lon']]].values[-1]

    def plot(self):
        """
        移動経路を描画する
        """
        plt.scatter(self.tripData[COLUMNs['lon']].values, self.tripData[COLUMNs['lat']].values)
        plt.show()


@dataclass
class User:
    """
    ユーザーごとのデータをまとめる

    `loc`, `feeder`, `trip`は当該ユーザーのみのデータを渡す
    """
    userid: int
    loc: pd.Series
    feeder: pd.Series
    trip: pd.Series
    trips: list[Trip] = field(init=False)
    tripTargets:ClassVar[list[str]] = [
        COLUMNs['createTime'],
        COLUMNs['lat'],
        COLUMNs['lon'],
        COLUMNs['height'],
        COLUMNs['bearing'],
        COLUMNs['speed'],
        COLUMNs['transportCode']
    ]
    
    def __post_init__(self) -> None:
        self.trips = self.__setupTrips()

    def __setupTrips(self):
        """
        当該ユーザーの全トリップを抽出
        """
        # データが完全にそろっている場合のみ処理
        if not (len(self.trip.index) > 1 and len(self.feeder.index) > 1):
            return None

        # feederとtripを統合
        addedFeeder = pd.merge(self.feeder, self.trip, how='left', on=COLUMNs['tripID'])
        self.loc.drop(columns=[COLUMNs['userID']], inplace=True)

        # トリップごとに情報を集計
        trips = [
            self.__trip(addedFeeder[addedFeeder[COLUMNs['tripID']] == tripInfo[0]], *tripInfo[1:])
            for tripInfo in self.trip[[COLUMNs['tripID'], COLUMNs['arrivalTime'], COLUMNs['objectiveCode']]].values
        ]

        return trips

    def __trip(self, addedFeeder, arriveTime, objective):
        """
        指定された条件に合うTripオブジェクトを取得
        
        １トリップ内における乗換などをそれぞれ管理する

        `addedFeeder`は当該トリップのみのデータに整形したものを指定
        """
        def getSplitTimes():
            """
            乗換履歴データを作成する
            """
            _splitTimes:pd.Series = addedFeeder[COLUMNs['recordTime']]
            # 到着時間を追加
            _splitTimes.loc[-1] = arriveTime
            # データが到着順に並んでいるため，時系列通りに並び替え
            _splitTimes.sort_index(inplace=True, ascending=False)
            # NDArrayで出力
            return _splitTimes.values

        def getTransports():
            """
            移動手段の一覧を作成する
            """
            _transport:pd.Series = addedFeeder[COLUMNs['transportCode']]
            _transport.sort_index(inplace=True, ascending=False)
            return _transport.values
            
        # 出発・乗換の時間
        splitTimes = getSplitTimes()
        transports = getTransports()

        # 各交通手段におけるlocを集計
        # 各行手段で移動中のすべての移動履歴(loc)を収集していく
        locParts = pd.DataFrame(columns=self.tripTargets)
        for startTime, endTime, transport in zip(splitTimes[:-1], splitTimes[1:], transports):
            locPart = self.loc[(startTime<self.loc[COLUMNs['createTime']]) & (self.loc[COLUMNs['createTime']]<endTime)]
            locPart[COLUMNs['transportCode']] = transport
            locParts = pd.concat([locParts, locPart])

        return Trip(locParts, objective)


@dataclass
class SourceLoader:
    """
    CSVデータの読み込み＆UserやTripオブジェクトへ分解
    """
    encoding:str            = field(default='shift-jis')
    sourcePath:Path         = field(default=Path(__file__).parent/'Sources')
    locName:str             = field(default='t_loc_data.csv')
    feederName:str          = field(default='t_locfeeder.csv')
    tripName:str            = field(default='t_trip.csv')
    activeLegendName:str    = field(default='m_active.csv')
    transportLegendName:str = field(default='m_transportation.csv')
    locTargets:ClassVar[list[str]] = [
        COLUMNs['userID'],
        COLUMNs['createTime'],
        COLUMNs['lat'],
        COLUMNs['lon'],
        COLUMNs['height'],
        COLUMNs['bearing'],
        COLUMNs['speed']
    ]
    feederTargets:ClassVar[list[str]] = [
        COLUMNs['userID'],
        COLUMNs['recordTime'],
        COLUMNs['transportCode'],
        COLUMNs['tripID']
    ]
    tripTargets:ClassVar[list[str]] = [
        'ID',
        COLUMNs['userID'],
        COLUMNs['departureTime'],
        COLUMNs['arrivalTime'],
        COLUMNs['objectiveCode']
    ]

    def __post_init__(self):
        self.activeLegend, self.transportLegend = self.__loadLegend()
        loc = self.__loadLoc()
        feeder = self.__loadFeeder()
        trip = self.__loadTrip()
        self.users = self.__df2Users(loc, feeder, trip)

    def __loadLoc(self):
        """
        locationデータ（移動の詳細な軌跡）の読み込み
        """
        loc = pd.read_csv(self.sourcePath/self.locName, encoding=self.encoding)
        loc = loc[self.locTargets]
        loc[COLUMNs['createTime']] = pd.to_datetime(loc[COLUMNs['createTime']])
        return loc

    def __loadFeeder(self):
        """
        feederデータ（移動の目的など）の読み込み
        """
        feeder = pd.read_csv(self.sourcePath/self.feederName, encoding=self.encoding)
        feeder = feeder[self.feederTargets]
        feeder[COLUMNs['recordTime']] = pd.to_datetime(feeder[COLUMNs['recordTime']])
        return feeder

    def __loadTrip(self):
        """
        tripデータ（Trip単位の出発時刻や到着時刻など）の読み込み
        """
        trip = pd.read_csv(self.sourcePath/self.tripName, encoding=self.encoding)
        trip = trip[self.tripTargets]
        trip[COLUMNs['departureTime']] = pd.to_datetime(trip[COLUMNs['departureTime']])
        trip[COLUMNs['arrivalTime']] = pd.to_datetime(trip[COLUMNs['arrivalTime']])
        trip.rename(columns={'ID' : COLUMNs['tripID']}, inplace=True)
        return trip

    def __loadLegend(self):
        """
        凡例データ（移動手段や目的のコードとその意味の対応）の読み込み
        """
        active = pd.read_csv(self.sourcePath/self.activeLegendName  , index_col='コード', encoding=self.encoding)
        trans = pd.read_csv(self.sourcePath/self.transportLegendName, index_col='コード', encoding=self.encoding)
        return active.to_dict()['名称'], trans.to_dict()['名称']

    def __df2Users(self, loc:pd.DataFrame, feeder:pd.DataFrame, trip:pd.DataFrame):
        """
        Userオブジェクトの宣言
        """
        userids = np.unique(np.concatenate((loc[COLUMNs['userID']], feeder[COLUMNs['userID']], trip[COLUMNs['userID']]), axis=0))
        users = [
            User(
                userid,
                loc[loc[COLUMNs['userID']] == userid],
                feeder[feeder[COLUMNs['userID']] == userid],
                trip[trip[COLUMNs['userID']] == userid],
            )
            for userid in tqdm(userids)
        ]
        return users


if __name__ == "__main__":
    # データの読み込み
    loader = SourceLoader()
    
    # 試しに最初の人の最初のトリップ情報を取得してみる
    print(loader.users[0].trips[0].objective)
    print(loader.users[0].trips[0].tripData)
    print(loader.users[0].trips[0].startPos)

    # 移動履歴を描画
    loader.users[0].trips[0].plot()
