
import asyncio
from threading import Thread
from .interface import Interface, SceneManager
from datetime import datetime
from time import sleep
from .chairyData import ChairyData


class UpdateExecutor(Thread):
    """ ### 백그라운드 업데이트 실행기 """

    Running : bool

    FREEZE  : bool = False

    Tick    : int

    Day: int
    Hou: int
    Min: int

    Media: bool



    def __init__(self):
        """
        #### 매개변수:
        - **media_info:** MediaInfo
        - **neis_data:** NeisData

        * **근데 절대로 인스턴스 새로 만들면 안되고 ChairyData에 있는거 그대로 투입해야함!**
        """

        self.Running  = True

        dt = datetime.now()
        self.Day = dt.day
        self.Hou = dt.hour
        self.Min = dt.minute

        self.Tick = 0
        self.Media = False

        super().__init__()
        self.start()



    def stop(self):
        """ UpdateExecuter 종료 """
        if self.Running:
            self.Running = False
            self.join()


    @staticmethod
    def Freeze():
        UpdateExecutor.FREEZE = True


    @staticmethod
    def Unfreeze():
        UpdateExecutor.FREEZE = False


    def run(self):
        while 1:
            sleep(1)
            if not self.Running:
                return
            if not UpdateExecutor.FREEZE:
                self._second()


    def _second(self):
        """ 매초마다 호출되는 함수 """

        dt = datetime.now()

        # 일
        if self.Day != dt.day:
            
            self.Day = dt.day

        # 시
        if self.Hou != dt.hour:
            # Neis 갱신
            if dt.hour == 0 or dt.hour == 18:
                ChairyData.NEISDATA.update()
            self.Hou = dt.hour

        # 분
        if self.Min != dt.minute:
            Interface.SD_DateTime.minuteChanged()
            ChairyData.ROOMDATA.Save()
            self.Min = dt.minute

        # 미디어 갱신
        self.Media = not self.Media

        if self.Media:
            asyncio.run(ChairyData.CURRENT_MEDIA.update())

        # 재시작 검사
        if ChairyData.Ready and ChairyData.RESTART_AT < dt:
            SceneManager.Restart()