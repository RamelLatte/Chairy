
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .chairyData.MediaInfo import MediaInfo
from .chairyData.NeisData import NeisData
from .interface import Interface
from datetime import datetime



class UpdateExecutor:
    """ ### 백그라운드 업데이트 실행기 """

    Media_Info: MediaInfo
    Neis_Data : NeisData

    Executor: ThreadPoolExecutor
    Loop: asyncio.AbstractEventLoop

    Running : bool
    Tick    : int

    Day: int
    Hou: int
    Min: int

    Media: bool



    def __init__(self, media_info: MediaInfo, neis_data: NeisData):
        """
        #### 매개변수:
        - **media_info:** MediaInfo
        - **neis_data:** NeisData

        * **근데 절대로 인스턴스 새로 만들면 안되고 ChairyData에 있는거 그대로 투입해야함!**
        """
        self.Media_Info = media_info
        self.Neis_Data  = neis_data

        self.Executor = ThreadPoolExecutor(max_workers=1)
        self.Loop     = asyncio.new_event_loop()
        asyncio.set_event_loop(self.Loop)

        self.Running  = True

        dt = datetime.now()
        self.Day = dt.day
        self.Hou = dt.hour
        self.Min = dt.minute

        self.Tick = 0
        self.Media = False



    def stop(self):
        """ UpdateExecuter 종료 """
        if self.Running:
            self.Running = False
            self.Loop.call_soon_threadsafe(self.Loop.stop)
            self.Executor.shutdown(wait=True)


    def tick(self, tick: int):
        """ 타이밍 계산 """
        self.Tick += tick

        if self.Tick > 1000:
            self.Tick = 0
            self.Media = not self.Media
            self._second()


    def _updateMedia(self):
        """ MediaInfo 갱신 """
        self.Loop.run_until_complete(self.Media_Info.update())


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
                self.Executor.submit(self.Neis_Data.update)
            self.Hou = dt.hour

        # 분
        if self.Min != dt.minute:
            self.Executor.submit(Interface.SD_DateTime.minuteChanged)
            self.Min = dt.minute

        # 미디어 갱신
        if self.Media:
            self.Executor.submit(self._updateMedia)