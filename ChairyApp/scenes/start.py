
from ..interface    import Scene, Styles
from ..interface    import SceneManager
from .exportDaily   import ExportDaily
from .exportMonthly import ExportMonthly
from .exportPeriod  import ExportPeriod
from .exportSeats   import ExportSeats
from .mainScene     import MainScene
from .transition    import Transition
from pygame         import Surface, Rect, draw



class StartScene(Scene):
    """
    ### 시작 장면

    이 장면에서 일부 Components들을 초기화함.
    """

    Asset_MasanHighSchool: Surface
    Asset_HR: Surface


    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        self.Asset_MasanHighSchool = SceneManager.loadAsset("/ChairyApp/assets/MasanHighSchool.png").convert(DISPLAY)
        self.Asset_HR = SceneManager.loadAsset("/ChairyApp/assets/startSceneLogo.png").convert(DISPLAY)

        MainScene.Init()
        ExportDaily.Init()
        ExportMonthly.Init()
        ExportPeriod.Init()
        ExportSeats.Init()


    def On_Update(self, ANIMATION_OFFSET, TICK):

        if SceneManager.SCENE_TIME > 500:
            Transition(MainScene())
        

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        DISPLAY.fill(Styles.SPRLIGHTGRAY, [0, 480, 1920, 120])
        DISPLAY.blit(self.Asset_MasanHighSchool, (812, 509))
        DISPLAY.blit(self.Asset_HR, (1028, 509))
        draw.rect(DISPLAY, Styles.BLACK, [960, 480, 1, 120])
        RECTS.append(Rect(812, 480, 278, 120))


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(self.Asset_MasanHighSchool, (812, 509))
        SURFACE.blit(self.Asset_HR, (1028, 509))
        draw.rect(SURFACE, Styles.BLACK, [960, 480, 1, 120])