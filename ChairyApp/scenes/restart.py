
from ..interface    import Scene, Styles, SceneManager, Interface
from ..chairyData   import ChairyData
from ..UpdateExecutor import UpdateExecutor
from .transition    import Transition
from pygame         import Surface, draw, Rect

from ..optimization.animation import Animate

from concurrent.futures import ThreadPoolExecutor, Future
from ..Logging import LoggingManager as logging


class RestartScene(Scene):
    """
    ### 시작 장면

    이 장면에서 Chairy 구동을 위한 다양한 요소를 준비함.
    """

    Asset_MasanHighSchool: Surface
    Asset_HR: Surface

    CurrentProcess_Surface  : Surface
    CurrentProcess_String   : str

    Bar_Length: float
    Bar_Length_: float

    Executor: ThreadPoolExecutor
    Task    : Future

    Timer: int


    def __init__(self):
        super().__init__()
        UpdateExecutor.Freeze()
        self.Identifier = 'start'


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

        self.Timer = 0

        # 로고 렌더링
        DISPLAY.fill(Styles.SPRLIGHTGRAY, [0, 480, 1920, 120])
        DISPLAY.blit(self.Asset_MasanHighSchool, (812, 509))
        DISPLAY.blit(self.Asset_HR, (1028, 509))
        draw.rect(DISPLAY, Styles.BLACK, [960, 480, 1, 120])

        # 데이터 불러오기
        self.Task = self.Executor.submit(ChairyData.Restart)


    def On_Update(self, ANIMATION_OFFSET, TICK):

        if self.CurrentProcess_String != ChairyData.CURRENT_PROGRESS:
            self.CurrentProcess_String = ChairyData.CURRENT_PROGRESS
            self.CurrentProcess_Surface.fill(Styles.SPRLIGHTGRAY)
            txt = Styles.SANS_B4.render(self.CurrentProcess_String, 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.CurrentProcess_Surface.blit(txt, txt.get_rect(centerx=400, top=0))
            self.Bar_Length_ = 800 * min(1, (ChairyData.LOADPROGRESS / ChairyData.MAX_PROGRESS))

        self.Bar_Length = Animate(self.Bar_Length, self.Bar_Length_, 1.5, ANIMATION_OFFSET)

        if self.Task.done():

            exc = self.Task.exception()

            if exc:
                logging.error('데이터를 재설정하는 도중 오류가 발생했습니다.', exc, True)

            self.Executor.shutdown()
            UpdateExecutor.Unfreeze()
            self.Timer += TICK
            if self.Timer > 1000:
                Transition(SceneManager.MainScene)
        


    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        # 로딩 상황 렌더링
        if not self.Task.done():
            DISPLAY.blit(self.CurrentProcess_Surface, (560, 970))
            draw.rect(DISPLAY, Styles.GRAY, [560, 1000, 800, 5])
            draw.rect(DISPLAY, Styles.BLACK, [560, 1000, self.Bar_Length, 5])
            RECTS.append(Rect(560, 970, 800, 35))
        else:
            RECTS.append(DISPLAY.fill(Styles.SPRLIGHTGRAY, [560, 970, 800, 35]))
            

    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(self.Asset_MasanHighSchool, (812, 509))
        SURFACE.blit(self.Asset_HR, (1028, 509))
        draw.rect(SURFACE, Styles.BLACK, [960, 480, 1, 120])