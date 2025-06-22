
from ..interface import Scene, SceneManager, Styles, Interface
from pygame import Surface

from ..optimization.rects import EmptyDRManager
from ..optimization.animation import AnimateSpdUp, Animate



class Transition(Scene):
    """
    ### 전환 효과 구현용 장면
    
    두 장면 사이의 전환 효과를 구현함.
    이 클래스도 궁극적으로는 Scene 클래스를 상속받았기에 여타 다른 장면들과 다를게 없음.

    대신, 두 Scene을 받아 Transition 클래스가 직접 내부 Surface로 렌더링하고 계산을 수행하는 것임.
    """

    Surface_A: Surface # 현재 장면
    Surface_B: Surface # 전환할 장면

    Scene_A: Scene # 현재 장면이 렌더링될 화면
    Scene_B: Scene # 전환할 장면이 렌더링될 화면

    Alpha: float        # 불투명도
    AnimationStep: bool # 애니메이션 단계(0 또는 1임)
    Position: int       # 화면 위치

    Continue: bool # 전환 효과가 끝났는지 여부



    def __init__(self, NextScene: Scene):
        self.Scene_A = SceneManager.CURRENT_SCENE
        self.Surface_A = Surface((1920, 1080))
        self.Surface_A.fill(Styles.SPRLIGHTGRAY)
        SceneManager.CURRENT_SCENE.Draw(self.Surface_A)

        self.Scene_B = NextScene
        self.Surface_B = Surface((1920, 1080))
        self.Surface_B.fill(Styles.SPRLIGHTGRAY)
        NextScene.On_Init(self.Surface_B)
        NextScene.Draw(self.Surface_B)

        self.Position = 0
        self.Alpha = 255.
        self.AnimationStep = False
        self.Continue = False

        SceneManager.setSceneRaw(self)


    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.WHITE)
        DISPLAY.blit(self.Surface_A, (self.Position, 0))


    def On_Update(self, ANIMATION_OFFSET, TICK):
        
        if self.AnimationStep:
            self.Scene_B.On_Update(ANIMATION_OFFSET, TICK)

            self.Position = Animate(self.Position, 0, 1.0, ANIMATION_OFFSET)
            self.Alpha += TICK

            if self.Alpha >= 255.:
                self.Alpha = 255.

            if self.Position < 1:
                self.Position = 0
                self.Continue = True
        
        else:
            self.Scene_A.On_Update(ANIMATION_OFFSET, TICK)

            if self.Alpha > 0.:
                self.Position = AnimateSpdUp(True, self.Position, 5, -1080, 2, ANIMATION_OFFSET)
                self.Alpha -= TICK

                if self.Alpha <= 0.:
                    self.Alpha = 0.
                    self.Position = 500
                    self.AnimationStep = True

        if SceneManager.SCENE_TIME > 3000:
            SceneManager.setSceneRaw(self.Scene_B)


    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)

        if self.AnimationStep:
            self.Scene_B.On_Render(ANIMATION_OFFSET, TICK, self.Surface_B, EmptyDRManager())
            self.Surface_B.set_alpha(self.Alpha)
            DISPLAY.blit(self.Surface_B, (self.Position, 0))
        else:
            self.Scene_A.On_Render(ANIMATION_OFFSET, TICK, self.Surface_A, EmptyDRManager())
            self.Surface_A.set_alpha(self.Alpha)
            DISPLAY.blit(self.Surface_A, (self.Position, 0))
        RECTS.updateFull()

        if self.Continue:
            SceneManager.setSceneRaw(self.Scene_B, False)


    def Event_Quit(self):
        self.Scene_B.Event_Quit()