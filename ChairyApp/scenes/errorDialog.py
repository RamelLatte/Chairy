
from ..interface import Scene, SceneManager, Styles
from pygame import Surface, SRCALPHA, constants

from ..optimization.animation import Animate
from ..optimization.positioning import center_top



class ErrorDialog(Scene):
    """ ### 오류 안내창 """

    BackgroundScene     : Scene     # 배경 Scene
    BackgroundSceneTime : int       # 배경 Scene의 SCENE_TIME
    BackgroundSurface   : Surface   # 배경 Scene의 화면

    BgAlpha: float # 배경의 불투명도
    DialogY: float # 안내창의 위치 Y

    Dialog: Surface # 렌더링된 안내창

    IsError : bool  # 오류인지 여부
    Message : str   # 메시지
    Desc    : str   # 자세한 설명
    Fatal   : bool  # 치명적인지 여부

    Complete: bool # Dialog 가리기 여부

    FileName: str # 로그 파일의 위치



    def __init__(self, isError: bool, msg: str, descripion: str, fatal: bool, fnm: str):
        """
        #### 매개변수:
        - **isError:** 오류, 경고인지 여부
        - **msg:** 메시지
        - **description:** 자세한 설명
        - **fatal:** 발생한 오류나 경고가 치명적인지 여부
        - **fnm:** FileNaMe, 로그 파일의 위치
        """
        Scene.__init__(self)

        self.Identifier = 'ErrorDialog'

        self.IsError = isError
        self.Message = msg
        self.Desc    = descripion
        self.Fatal   = fatal

        self.Complete = False

        self.FileName = fnm

        self.BgAlpha = 255.
        self.DialogY = 1080.

        self.BackgroundSurface = Surface((1920, 1080))
        self.BackgroundSceneTime = SceneManager.SCENE_TIME
        self.BackgroundScene = SceneManager.CURRENT_SCENE

        SceneManager.setScene(self)



    def On_Init(self, DISPLAY):

        self.BackgroundSurface.fill(Styles.WHITE)

        try:
            self.BackgroundScene.Draw(self.BackgroundSurface)
            self.BackgroundSurface = self.BackgroundSurface.convert()
        except Exception:
            ...
        
        DISPLAY.blit(self.BackgroundSurface, (0, 0))

        self.Dialog = Surface((1920, 300), (SRCALPHA))
        self.Dialog.blit(SceneManager.loadAsset('/ChairyApp/assets/logging/LogDialog.png'), (0, 0))

        if self.IsError:
            self.Dialog.blit(SceneManager.loadAsset('/ChairyApp/assets/logging/Error.png'), (100, 120))
        else:
            self.Dialog.blit(SceneManager.loadAsset('/ChairyApp/assets/logging/Warning.png'), (100, 120))

        if self.Fatal:
            txt = Styles.SANS_H5.render('프로그램이 충돌했습니다', 1, Styles.WHITE, Styles.BLACK)
            self.Dialog.blit(txt, center_top(960, 30, txt.get_size()))
            txt = Styles.SANS_B4.render('오류로 인해 프로그램을 더 이상 이용할 수 없습니다. [ENTER] 키를 눌러 프로그램을 종료하십시오.', 1, Styles.WHITE, Styles.BLACK)
            self.Dialog.blit(txt, center_top(960, 225, txt.get_size()))
        else:
            txt = Styles.SANS_H5.render('문제가 발생했습니다', 1, Styles.WHITE, Styles.BLACK)
            self.Dialog.blit(txt, center_top(960, 30, txt.get_size()))
            txt = Styles.SANS_B4.render('프로그램은 계속 이용할 수 있습니다. [ENTER] 키를 눌러 계속하십시오.', 1, Styles.WHITE, Styles.BLACK)
            self.Dialog.blit(txt, center_top(960, 225, txt.get_size()))
        
        self.Dialog.blit(Styles.SANS_H4.render(self.Message, 1, Styles.BLACK, Styles.WHITE), (150, 107))
        self.Dialog.blit(Styles.SANS_B4.render(self.Desc, 1, Styles.BLACK, Styles.WHITE), (150, 146))

        txt = Styles.SANS_B4.render(f'자세한 오류 기록은 “/{self.FileName}” 파일을 참고합니다.', 1, Styles.WHITE, Styles.BLACK)
        self.Dialog.blit(txt, center_top(960, 247, txt.get_size()))

        DISPLAY.blit(self.Dialog, (0, self.DialogY))
    

    def On_Update(self, ANIMATION_OFFSET, TICK):

        if self.Complete:
            
            if self.BgAlpha < 255.:
                self.BgAlpha += TICK

                if self.BgAlpha > 255.:
                    self.BgAlpha = 255.    

            self.BackgroundSurface.set_alpha(self.BgAlpha)
            self.DialogY = Animate(self.DialogY, 1200, 1.25, ANIMATION_OFFSET)

        else:

            if self.BgAlpha > 128.:
                self.BgAlpha -= TICK

                if self.BgAlpha < 128.:
                    self.BgAlpha = 128.

            self.BackgroundSurface.set_alpha(self.BgAlpha)
            self.DialogY = Animate(self.DialogY, 780, 1.25, ANIMATION_OFFSET)
    

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):

        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(self.BackgroundSurface, (0, 0))

        DISPLAY.blit(self.Dialog, (0, self.DialogY))

        RECTS.updateFull()

        if not self.Fatal and self.Complete and self.DialogY > 1080 and self.BgAlpha == 255.:
            SceneManager.setScene(self.BackgroundScene, False)



    def Event_KeyDown(self, KEY):
        
        if KEY in (constants.K_RETURN, constants.K_KP_ENTER):

            if self.Fatal:
                self.Call_Quit()
            else:
                self.Complete = True