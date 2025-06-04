
from pygame.font import Font
from pygame import Surface
from .Component import Component
from .Styles import Styles



class ScrollingTextbox(Component):
    """ ### 스크롤 애니메이션이 포함된 단일 줄 텍스트 박스 """

    FONT    : Font
    HEIGHT  : int
    WIDTH   : int

    textY   : int
    _textY  : int

    Text    : Surface
    _Text   : Surface

    Shift   : bool

    SURFACE : Surface


    def __init__(self, width: int, font: Font, text: str, color: tuple[int], x = 115, y = 432):
        self.HEIGHT = font.get_height()

        super().__init__(x, y, width, self.HEIGHT)
        
        self.Reset(width, font, text, color)


    def set(self, text: str, color: tuple[int]):
        """
        텍스트 박스의 텍스트를 바꿈.
        - - -
        #### 매개변수:
        - **text:** 전환할 텍스트
        - **color:** 텍스트의 색깔
        """
        if self.Shift:
            self.Text = self._Text.copy()
        else:
            self.Shift = True
        self._Text = self.FONT.render(text, True, color, Styles.SPRLIGHTGRAY)
        self._textY = 0



    def Reset(self, width: int, font: Font, text: str, color: tuple[int], x = 115, y = 432):
        self.MoveTo(x, y)

        self.FONT = font
        self.WIDTH = width
        self.Text = self.FONT.render(text, True, color, Styles.SPRLIGHTGRAY)
        self._Text = self.FONT.render(text, True, color, Styles.SPRLIGHTGRAY)
        self.textY = 0
        self._textY = 0
        self.Shift = True

        self.SURFACE = Surface((width, self.HEIGHT))


    def Update(self, A_OFFSET):
        if self.Shift:
            self._textY += (self.HEIGHT - self._textY + 2) * A_OFFSET

            if self._textY > self.HEIGHT:
                self._textY = 0
                self.Text = self._Text.copy()
                self._Text = None
                self.Shift = False

            return True

        return (self.Y != self._Y)


    def Frame(self, DISP: Surface):
        self.SURFACE.fill(Styles.SPRLIGHTGRAY)
        if self.Shift:
            self.SURFACE.blit(self._Text, (0, self._textY - self.HEIGHT))
        self.SURFACE.blit(self.Text, (0, self._textY))
        DISP.blit(self.SURFACE, (self.X, self.Y))

        DISP.fill(Styles.SPRLIGHTGRAY, self.calculateTrailRect_Y())
        DISP.blit(self.SURFACE, (self.X, self.Y))

        return self.calculateRect()