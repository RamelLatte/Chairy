
from .Component import Component
from pygame import Surface, SRCALPHA
from .Styles import Styles
from .Scene import SceneManager as SM
from datetime import datetime

from ..optimization.positioning import center_top



class StudentHoverInfo(Component):
    """ ### 마우스 옆으로 띄우는 간략한 학생 정보 """

    Asset: Surface
    Updated     : bool

    SURFACE: Surface

    Show: bool

    M_POS: tuple[int]


    def __init__(self, layer1: Surface):
        super().__init__(0, 0, 190, 90)

        self.Asset = SM.loadAsset('/ChairyApp/assets/layer/StudentInfo.png').convert_alpha(layer1)
        self.SURFACE = Surface((190, 90), (SRCALPHA))

        self.Show = False
        self.M_POS = (0, 0)
        self.Reset()


    def timeStr(self, T: datetime) -> str:
        """ 시간을 읽을 수 있는 문자열로 변환. """
        if T.hour > 12:
            return T.strftime(f"오후 {T.hour - 12}:%M 입실")
        elif T.hour == 12:
            return T.strftime(f"오후 12:%M 입실")
        elif T.hour == 0:
            return T.strftime("오전 12:%M 입실")
        else:
            return T.strftime("오전 %H:%M 입실")


    def render(self, ID: str, Name: str, ChkIn: datetime):
        self.SURFACE.fill((0, 0, 0, 0))

        self.SURFACE.blit(self.Asset, (0, 0))
        txt = Styles.ANTON_H5.render(ID, 1, Styles.WHITE, Styles.BLACK)
        self.SURFACE.blit(txt, center_top(43, 3, txt.get_size()))
        del txt

        self.SURFACE.blit(Styles.SANS_H5.render(Name, 1, Styles.WHITE, Styles.BLACK), (80, 22))

        if ChkIn is not None:
            self.SURFACE.blit(Styles.SANS_B5.render(self.timeStr(ChkIn), 1, Styles.WHITE, Styles.BLACK), (80, 45))
        else:
            self.SURFACE.blit(Styles.SANS_B5.render('입실 시간 기록 없음', 1, Styles.WHITE, Styles.BLACK), (80, 45))

        self.Updated = True


    def show(self):
        self.Show = True
        self.Updated = True
        self.X = self.M_POS[0] + 15
        self.Y = self.M_POS[1] + 15


    def hide(self):
        self.Show = False
        self.Updated = True
    

    def Reset(self):
        self.Updated = False


    def Update(self):
        return self.Updated


    def Frame(self, DISP):
        self.Updated = False
        
        r = self.calculateRect()

        DISP.fill((0, 0, 0, 0), r)

        if self.Show:
            DISP.blit(self.SURFACE, (self.X, self.Y))

        return r
    

    def MouseMotion(self, POS):
        self.M_POS = POS

        if self.Show:
            self.X = POS[0] + 15
            self.Y = POS[1] + 15



class Notice(Component):
    """ ### 레이어에 띄우는 안내문 """

    Assets: list[Surface]
    Index: int
    Show: bool
    Time: int


    def __init__(self, layer1: Surface):
        super().__init__(753, -114, 414, 114)

        self.Assets = [
            SM.loadAsset('/ChairyApp/assets/layer/Idle0.png').convert_alpha(layer1),
            SM.loadAsset('/ChairyApp/assets/layer/Idle1.png').convert_alpha(layer1),
            SM.loadAsset('/ChairyApp/assets/layer/IdFirst.png').convert_alpha(layer1),
            SM.loadAsset('/ChairyApp/assets/layer/LowEnergy.png').convert_alpha(layer1)
        ]
        self.Index = 0
        self.Show = False
        self.Time = 0
        self.Reset()


    def show_Idle0(self):
        self.Index = 0
        self.Y = -114
        self.Time = 0
        self.Show = True


    def show_Idle1(self):
        self.Index = 1
        self.Y = -114
        self.Time = 0
        self.Show = True


    def show_IdFirst(self):
        self.Index = 2
        self.Y = -114
        self.Time = 0
        self.Show = True


    def show_LowEnergy(self):
        self.Index = 3
        self.Y = -114
        self.Time = 0
        self.Show = True


    def hide(self):
        self.Show = False
    

    def Reset(self):
        ...


    def Update(self, A_OFFSET, TICK):
        if self.Show:
            self.Time += TICK

            if self.Time > 2000:
                self.Show = False
                self.Time = 0

            self.Animate_Y(15, 1.5, A_OFFSET)

            return True
        
        elif self.Y != -114:
            self.AnimateSpdUp_Y(True, 15, -114, 2.5, A_OFFSET)

            return True

        return False


    def Frame(self, DISP):
        r = self.calculateRect()

        if self.Y > -114:
            DISP.fill((0, 0, 0, 0), r)
            DISP.blit(self.Assets[self.Index], (753, self.Y))

        return r