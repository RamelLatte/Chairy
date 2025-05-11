
from pygame import Surface, Rect
from .Component import Component
from .Styles import Styles
from .Scene import SceneManager as SM

from ..optimization.animation import Animate



class IdInputDialog(Component):
    """ ### 학번 입력란 """

    Text1       : Surface
    _Text1      : Surface
    TextL1      : int
    _TextL1     : int
    TextPos1    : int
    Scrolling1  : bool

    Text2       : Surface
    _Text2      : Surface
    TextL2      : int
    _TextL2     : int
    TextPos2    : int
    Scrolling2  : bool

    Text3       : Surface
    _Text3      : Surface
    TextL3      : int
    _TextL3     : int
    TextPos3    : int
    Scrolling3  : bool

    Text4       : Surface
    _Text4      : Surface
    TextL4      : int
    _TextL4     : int
    TextPos4    : int
    Scrolling4  : bool

    AssetStudentIdBox   : Surface

    SURFACE     : Surface
    Updated     : bool

    StudentId   : list[str]

    Moving  : bool
    Rect_   : Rect

    Y_      : int


    def __init__(self):
        super().__init__()
        
        self.SURFACE    = Surface((300, 108))
        self.AssetStudentIdBox  = SM.loadAsset("/ChairyApp/assets/components/studentIdBox.png").convert(self.SURFACE)
        self.Reset()
   

    def text1(self):
        """ 첫번째 칸을 갱신함. """
        if self.Scrolling1:
            self.Text1 = self._Text1.copy()
            self.TextL1 = self._TextL1
        else:
            self.Scrolling1 = True
        if self.StudentId[0] == '-':
            self._Text1 = Styles.SERIF_H1.render("-", True, Styles.DARKGRAY, Styles.WHITE)
        else:
            self._Text1 = Styles.SERIF_H1.render(self.StudentId[0], True, Styles.BLUE, Styles.WHITE)
        self._TextL1 = (68 - self._Text1.get_width()) / 2
        self.TextPos1 = 8


    def text2(self):
        """ 두번째 칸을 갱신함. """
        if self.Scrolling2:
            self.Text2 = self._Text2.copy()
            self.TextL2 = self._TextL2
        else:
            self.Scrolling2 = True
        if self.StudentId[1] == '-':
            self._Text2 = Styles.SERIF_H1.render("-", True, Styles.DARKGRAY, Styles.WHITE)
        else:
            self._Text2 = Styles.SERIF_H1.render(self.StudentId[1], True, Styles.BLUE, Styles.WHITE)
        self._TextL2 = 77 + ((68 - self._Text2.get_width()) / 2)
        self.TextPos2 = 8


    def text3(self):
        """ 세번째 칸을 갱신함. """
        if self.Scrolling3:
            self.Text3 = self._Text3.copy()
            self.TextL3 = self._TextL3
        else:
            self.Scrolling3 = True
        if self.StudentId[2] == '-':
            self._Text3 = Styles.SERIF_H1.render("-", True, Styles.DARKGRAY, Styles.WHITE)
        else:
            self._Text3 = Styles.SERIF_H1.render(self.StudentId[2], True, Styles.BLUE, Styles.WHITE)
        self._TextL3 = 154 + ((68 - self._Text3.get_width()) / 2)
        self.TextPos3 = 8


    def text4(self):
        """ 네번째 칸을 갱신함. """
        if self.Scrolling4:
            self.Text4 = self._Text4.copy()
            self.TextL4 = self._TextL4
        else:
            self.Scrolling4 = True
        if self.StudentId[3] == '-':
            self._Text4 = Styles.SERIF_H1.render("-", True, Styles.DARKGRAY, Styles.WHITE)
        else:
            self._Text4 = Styles.SERIF_H1.render(self.StudentId[3], True, Styles.BLUE, Styles.WHITE)
        self._TextL4 = 231 + ((68 - self._Text4.get_width()) / 2)
        self.TextPos4 = 8

    
    def text(self, index: int):
        """ 매개변수로 지정하여 {index}칸을 갱신함. **index는 0, 1, 2, 3 중 하나로 해야함.**"""
        if index == 0:
            self.text1()
        elif index == 1:
            self.text2()
        elif index == 2:
            self.text3()
        elif index == 3:
            self.text4()


    
    def Reset(self, x = 115, y = 492):
        self.X = x
        self.Y = y
        self.Y_= y

        self.TextPos1   = 6
        self.TextPos2   = 6
        self.TextPos3   = 6
        self.TextPos4   = 6

        self.StudentId  = ['-', '-', '-', '-']

        self.Text1 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self.Text2 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self.Text3 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self.Text4 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)

        self.TextL1 = (68 - self.Text1.get_width()) / 2
        self.TextL2 = 77 + ((68 - self.Text2.get_width()) / 2)
        self.TextL3 = 154 + ((68 - self.Text3.get_width()) / 2)
        self.TextL4 = 231 + ((68 - self.Text4.get_width()) / 2)

        self._Text1 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self._Text2 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self._Text3 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)
        self._Text4 = Styles.SERIF_H1.render("-", 1, Styles.DARKGRAY, Styles.WHITE)

        self._TextL1 = (68 - self._Text1.get_width()) / 2
        self._TextL2 = 77 + ((68 - self._Text2.get_width()) / 2)
        self._TextL3 = 154 + ((68 - self._Text3.get_width()) / 2)
        self._TextL4 = 231 + ((68 - self._Text4.get_width()) / 2)

        self.Scrolling1 = False
        self.Scrolling2 = False
        self.Scrolling3 = False
        self.Scrolling4 = False

        self.SURFACE.fill(Styles.SPRLIGHTGRAY)
        self.SURFACE.blit(self.AssetStudentIdBox, (0, 0))
        self.SURFACE.blit(self.AssetStudentIdBox, (77, 0))
        self.SURFACE.blit(self.AssetStudentIdBox, (154, 0))
        self.SURFACE.blit(self.AssetStudentIdBox, (231, 0))

        self.SURFACE.blit(self.Text1, (self.TextL1, self.TextPos1))
        self.SURFACE.blit(self.Text2, (self.TextL2, self.TextPos2))
        self.SURFACE.blit(self.Text3, (self.TextL3, self.TextPos3))
        self.SURFACE.blit(self.Text4, (self.TextL4, self.TextPos4))

        self.Updated = True


    def Update(self, A_OFFSET):

        if self.Scrolling1:
            self.Updated = True
            self.TextPos1 = Animate(self.TextPos1, 110, 1.25, A_OFFSET)

            self.SURFACE.blit(self.AssetStudentIdBox, (0, 0))
            self.SURFACE.blit(self._Text1, (self._TextL1, self.TextPos1 - 100))
            self.SURFACE.blit(self.Text1, (self.TextL1, self.TextPos1))

            if self.TextPos1 > 108:
                self.TextPos1 = 8
                self.Text1 = self._Text1.copy()
                self.TextL1 = self._TextL1
                self._Text1 = None
                self.Scrolling1 = False

        if self.Scrolling2:
            self.Updated = True
            self.TextPos2 = Animate(self.TextPos2, 110, 1.25, A_OFFSET)

            self.SURFACE.blit(self.AssetStudentIdBox, (77, 0))
            self.SURFACE.blit(self._Text2, (self._TextL2, self.TextPos2 - 100))
            self.SURFACE.blit(self.Text2, (self.TextL2, self.TextPos2))

            if self.TextPos2 > 108:
                self.TextPos2 = 8
                self.Text2 = self._Text2.copy()
                self.TextL2 = self._TextL2
                self._Text2 = None
                self.Scrolling2 = False

        if self.Scrolling3:
            self.Updated = True
            self.TextPos3 = Animate(self.TextPos3, 110, 1.25, A_OFFSET)

            self.SURFACE.blit(self.AssetStudentIdBox, (154, 0))
            self.SURFACE.blit(self._Text3, (self._TextL3, self.TextPos3 - 100))
            self.SURFACE.blit(self.Text3, (self.TextL3, self.TextPos3))

            if self.TextPos3 > 108:
                self.TextPos3 = 8
                self.Text3 = self._Text3.copy()
                self.TextL3 = self._TextL3
                self._Text3 = None
                self.Scrolling3 = False

        if self.Scrolling4:
            self.Updated = True
            self.TextPos4 = Animate(self.TextPos4, 110, 1.25, A_OFFSET)

            self.SURFACE.blit(self.AssetStudentIdBox, (231, 0))
            self.SURFACE.blit(self._Text4, (self._TextL4, self.TextPos4 - 100))
            self.SURFACE.blit(self.Text4, (self.TextL4, self.TextPos4))

            if self.TextPos4 > 108:
                self.TextPos4 = 8
                self.Text4 = self._Text4.copy()
                self.TextL4 = self._TextL4
                self._Text4 = None
                self.Scrolling4 = False

        return self.Updated or (self.Y != self.Y_)


    def Frame(self, DISP: Surface) -> Rect:
        self.Updated = False

        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 108, 300, - d + 1))
                DISP.blit(self.SURFACE, (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 300, 109 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 300, d + 2))
                DISP.blit(self.SURFACE, (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 300, 108 + d)
        else:
            return DISP.blit(self.SURFACE, (self.X, self.Y))