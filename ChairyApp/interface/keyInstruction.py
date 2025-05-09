
from pygame import Surface, Rect
from .Component import Component
from .Styles import Styles
from .Scene import SceneManager as SM

from ..optimization.animation import Animate


class KeyInstructionDisplay(Component):
    """ ### 입력 가이드 """

    Asset   : list[Surface]

    Use     : int # 0: Mouse, 1: Keypad, 2: Both
    _Use    : int

    SURFACE : Surface

    Pos: float

    Y_  : int

    def __init__(self):
        super().__init__()
        
        self.SURFACE = Surface((223, 29))
        self.Asset = [ 
                        SM.loadAsset("/ChairyApp/assets/components/useMouse.png").convert(self.SURFACE),
                        SM.loadAsset("/ChairyApp/assets/components/useKeypad.png").convert(self.SURFACE),
                        SM.loadAsset("/ChairyApp/assets/components/useBoth.png").convert(self.SURFACE),
                        SM.loadAsset("/ChairyApp/assets/components/wait.png").convert(self.SURFACE)
                    ]

        self.Reset()

     
    def useMouse(self):
        """ 마우스를 사용하라고 표시 """
        self._Use = 0


    def useKeypad(self):
        """ 키패드를 사용하라고 표시 """
        self._Use = 1


    def useBoth(self):
        """ 마우스/키패드 둘 다 된다고 표시 """
        self._Use = 2


    def wait(self):
        """ 잠시 기다리라고 표시 """
        self._Use = 3

    

    def Reset(self, x = 153, y = 619):
        self.Use = 0
        self._Use = 1
        self.Pos = 0

        self.SURFACE.blit(self.Asset[0], (0, 0))
        
        self.X = x
        self.Y = y
        self.Y_ = y

    
    def Update(self, A_OFFSET):
        if self.Use != self._Use or self.Pos != 0:
            self.Pos = Animate(self.Pos, 30, 1.25, A_OFFSET)

            if self.Pos > 28:
                self.Pos = 0
                self.Use = self._Use
                self.SURFACE.blit(self.Asset[self.Use], (0, 0))

            self.SURFACE.blit(self.Asset[self._Use], (0, self.Pos - 29))
            self.SURFACE.blit(self.Asset[self.Use], (0, self.Pos))

            return True
        
        return (self.Y != self.Y_)
    

    def Frame(self, DISP: Surface) -> Rect:
        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 29, 223, - d + 1))
                DISP.blit(self.SURFACE, (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 223, 30 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 233, d + 2))
                DISP.blit(self.SURFACE, (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 223, 29 + d)
        else:
            return DISP.blit(self.SURFACE, (self.X, self.Y))