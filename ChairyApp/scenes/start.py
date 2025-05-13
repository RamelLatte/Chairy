
from ..interface    import Scene, Styles, SceneManager, Interface
from ..chairyData   import ChairyData
from ChairyApp.ChairyApp import ChairyApp
from .exportDaily   import ExportDaily
from .exportMonthly import ExportMonthly
from .exportPeriod  import ExportPeriod
from .exportSeats   import ExportSeats
from .mainScene     import MainScene
from .transition    import Transition
from pygame         import Surface, draw

from ..optimization.animation import Animate

from concurrent.futures import ThreadPoolExecutor


class StartScene(Scene):
    """
    ### 시작 장면

    이 장면에서 Chairy 구동을 위한 다양한 요소를 준비함.
    """

    Asset_MasanHighSchool: Surface
    Asset_HR: Surface

    Queued_Interface: bool

    CurrentProcess_Surface  : Surface
    CurrentProcess_String   : str

    Bar_Length: int
    Bar_Length_: int

    Executor: ThreadPoolExecutor

    Complete: bool
    Timer: int


    def __init__(self):
        super().__init__()
        self.Identifier = 'start'
        self.Queued_Interface = False


    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        self.Asset_MasanHighSchool = SceneManager.loadAsset("/ChairyApp/assets/MasanHighSchool.png").convert(DISPLAY)
        self.Asset_HR = SceneManager.loadAsset("/ChairyApp/assets/startSceneLogo.png").convert(DISPLAY)

        self.Executor = ThreadPoolExecutor(max_workers=1)

        self.CurrentProcess_Surface = Surface((800, 20))
        self.CurrentProcess_Surface.fill(Styles.SPRLIGHTGRAY)

        self.CurrentProcess_String = ''

        self.Bar_Length = 0
        self.Bar_Length_ = 0

        self.Complete = False
        self.Timer = 0

        # 로고 렌더링
        DISPLAY.fill(Styles.SPRLIGHTGRAY, [0, 480, 1920, 120])
        DISPLAY.blit(self.Asset_MasanHighSchool, (812, 509))
        DISPLAY.blit(self.Asset_HR, (1028, 509))
        draw.rect(DISPLAY, Styles.BLACK, [960, 480, 1, 120])

        # 데이터 불러오기
        self.Executor.submit(ChairyData.Init)


    def On_Update(self, ANIMATION_OFFSET, TICK):

        if self.CurrentProcess_String != ChairyData.CURRENT_PROGRESS:
            self.CurrentProcess_String = ChairyData.CURRENT_PROGRESS
            self.CurrentProcess_Surface.fill(Styles.SPRLIGHTGRAY)
            txt = Styles.SANS_B4.render(self.CurrentProcess_String, 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.CurrentProcess_Surface.blit(txt, txt.get_rect(centerx=400, top=0))
            self.Bar_Length_ = 800 * min(1, (ChairyData.LOADPROGRESS / ChairyData.MAX_PROGRESS))

        self.Bar_Length = Animate(self.Bar_Length, self.Bar_Length_, 1.5, ANIMATION_OFFSET)

        if ChairyData.Ready and not self.Queued_Interface:
            self.Queued_Interface = True
            self.Executor.submit(Interface.Init)
            ChairyApp.Init_UpdateExecutor()

        if ChairyData.Ready and Interface.Ready and self.Bar_Length == 800:
            MainScene.Init()
            ExportDaily.Init()
            ExportMonthly.Init()
            ExportPeriod.Init()
            ExportSeats.Init()

            self.Executor.shutdown()
            self.Complete = True

        if self.Complete:
            self.Timer += TICK
            if self.Timer > 1000:
                Transition(MainScene())
        


    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        # 로딩 상황 렌더링
        if not self.Complete:
            DISPLAY.blit(self.CurrentProcess_Surface, (560, 970))
            draw.rect(DISPLAY, Styles.GRAY, [560, 1000, 800, 5])
            draw.rect(DISPLAY, Styles.BLACK, [560, 1000, self.Bar_Length, 5])
            RECTS.append([560, 970, 800, 35])
        else:
            RECTS.append(DISPLAY.fill(Styles.SPRLIGHTGRAY, [560, 970, 800, 35]))
            

    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(self.Asset_MasanHighSchool, (812, 509))
        SURFACE.blit(self.Asset_HR, (1028, 509))
        draw.rect(SURFACE, Styles.BLACK, [960, 480, 1, 120])