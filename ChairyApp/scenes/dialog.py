
from ..interface import Scene, SceneManager, Styles
from pygame import Surface, SRCALPHA
from threading import Thread

from ..Logging import LoggingManager as logging
from ..optimization.animation import Animate, AnimateSpdUp
from ..optimization.positioning import center_top, center_center, center_bottom



class Dialog(Scene, Thread):
    """ ### 안내창 """

    BackgroundScene     : Scene     # 배경 Scene
    BackgroundSurface   : Surface   # 배경 Scene의 화면

    Asset: Surface # Dialog 기본 에셋

    BgAlpha: float # 배경의 불투명도
    DialogY: float # Dialog의 Y 위치

    Dialog: Surface # 렌더링된 Dialog

    Title: str       # 제목
    Description: str # 설명 텍스트
    Lower: str       # 하단 텍스트

    Complete: bool # Dialog 완료 여부

    Done: bool # 작업 완료 여부
    Except: bool # 오류 여부
    Except_: Exception # 오류


    def __init__(self, title: str, desc: str, lower: str = '잠시만 기다려주십시오...'):
        """
        #### 매개변수:
        - **title:** 제목
        - **desc:** 설명 텍스트
        - **lower:** 하단 텍스트, 기본값이 정해져 있음.
        """
        Scene.__init__(self)

        self.Identifier = 'Dialog'

        self.Title = title
        self.Description = desc
        self.Lower = lower

        self.BgAlpha = 255.
        self.DialogY = 1080.

        self.BackgroundSurface = Surface((1920, 1080))
        self.BackgroundScene = SceneManager.CURRENT_SCENE

        self.Complete = False

        self.Done = False
        self.Except = False
        self.Except_ = None

        SceneManager.setSceneRaw(self)
        super().__init__()


    def _Update(self):
        """ 내부 렌더링 작업을 수행함. """
        self.Dialog = Surface((500, 200), (SRCALPHA))
        self.Dialog.blit(self.Asset, (0, 0))
        txt = Styles.SANS_H4.render(self.Title, 1, Styles.BLACK, Styles.WHITE)
        self.Dialog.blit(txt, center_top(250, 25, txt.get_size()))

        if '\n' in self.Description:
            for index, line in enumerate(self.Description.split('\n'), start=0):
                txt = Styles.SANS_B4.render(line, 1, Styles.BLACK, Styles.WHITE)
                self.Dialog.blit(txt, center_center(250, 100 + (index * 20), txt.get_size()))
        else:
            txt = Styles.SANS_B4.render(self.Description, 1, Styles.BLACK, Styles.WHITE)
            self.Dialog.blit(txt, center_center(250, 100, txt.get_size()))
        txt = Styles.SANS_B4.render(self.Lower, 1, Styles.DARKGRAY, Styles.WHITE)
        self.Dialog.blit(txt, center_bottom(250, 175, txt.get_size()))
        self.Dialog.convert_alpha()

    
    def set(self, title: str, desc: str, lower: str = '잠시만 기다려주십시오...'):
        """
        텍스트를 지정하고 내부 렌더링 작업을 수행함.
        - - -
        #### 매개변수:
        - **title:** 제목
        - **desc:** 설명 텍스트
        - **lower:** 하단 텍스트, 기본값이 정해져 있음.
        """
        self.Title = title
        self.Description = desc
        self.Lower = lower
        self._Update()


    def task(self):
        """
        Dialog가 표시되는 동안 수행할 작업 로직, **Dialog가 표시될 때 따로 Thread가 호출되어 해당 메서드를 실행함.**
        
        해당 메서드가 완료되면 Dialog를 숨기며, **상속을 통해 task() 메서드를 Override하여 다른 기능을 수행하도록 할 수 있음.**
        """
        
        from time import sleep
        sleep(2.25)


    def run(self):

        try:
            self.task()
            self.Complete = True
        except Exception as e:
            self.Except = True
            self.Except_ = e
        finally:
            self.Done = True


    def On_Init(self, DISPLAY):
        self.Asset = SceneManager.loadAsset('/ChairyApp/assets/components/Dialog.png').convert_alpha(DISPLAY)
        self._Update()

        self.start()

        self.BackgroundScene.Draw(self.BackgroundSurface)
        self.BackgroundSurface = self.BackgroundSurface.convert()
        DISPLAY.blit(self.BackgroundSurface, (0, 0))

    
    def On_Update(self, ANIMATION_OFFSET, TICK):

        if not self.Complete and self.Done:
            if self.Except:
                logging.error('작업 처리 도중 오류가 발생했습니다.', self.Except_)
            self.Complete = True

        # Thread 완료
        if self.Complete:

            self.BackgroundScene.On_Update(ANIMATION_OFFSET, TICK)
            
            if self.BgAlpha < 255.:
                self.BgAlpha += TICK

                if self.BgAlpha > 255.:
                    self.BgAlpha = 255.    

            self.BackgroundSurface.set_alpha(self.BgAlpha)
            self.DialogY = AnimateSpdUp(False, self.DialogY, 1200, 1080, 1.5, ANIMATION_OFFSET)

            return

        # 처음 시작
        if self.BgAlpha > 128.:
            self.BgAlpha -= TICK

            if self.BgAlpha < 128.:
                self.BgAlpha = 128.

        self.BackgroundSurface.set_alpha(self.BgAlpha)

        self.DialogY = Animate(self.DialogY, 860, 1.5, ANIMATION_OFFSET)
    

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):

        if self.Complete:
            self.BackgroundScene.On_Render(ANIMATION_OFFSET, TICK, DISPLAY, RECTS)
        
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(self.BackgroundSurface, (0, 0))

        DISPLAY.blit(self.Dialog, (710, self.DialogY))

        RECTS.updateFull()

        if self.Complete and self.DialogY == 1080 and self.BgAlpha == 255.:
            SceneManager.setSceneRaw(self.BackgroundScene, False)