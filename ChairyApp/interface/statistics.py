
from . import SceneManager, Styles
from .Component import Component
from pygame import Surface, SRCALPHA

from ..optimization.animation import Animate
from ..optimization.positioning import center_top



class TopBar(Component):
    """ ### 통계 화면 상단 바 """

    SURFACE_: Surface # 텍스트 레이어

    Asset_Bar: Surface
    Asset_Selection: Surface

    Selection_X     : int
    Selection_X_    : int

    POS_X   : int

    Updated : bool



    def __init__(self):
        super().__init__(660, 15, 600, 40)

        self.SURFACE_   = Surface((600, 40), (SRCALPHA))
        self.Asset_Bar = SceneManager.loadAsset('/ChairyApp/assets/statistics/StaticsticsSelection0.png').convert_alpha()
        self.Asset_Selection = SceneManager.loadAsset('/ChairyApp/assets/statistics/StaticsticsSelection1.png').convert_alpha()

        self.Reset()

    
    def attendance(self):
        """ "일간 출석부"로 상단 바 선택란 위치 조정 """
        self.POS_X = 660
        self.SURFACE_.fill((0, 0, 0, 0))
        txt = Styles.SANS_H5.render("일간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(82, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("월간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(227, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("교시별 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(372, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("시간별 좌석", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(517, 8, txt.get_size()))
        self.Selection_X_   = 0


    def monthly(self):
        """ "월간 출석부"로 상단 바 선택란 위치 조정 """
        self.POS_X = 660
        self.SURFACE_.fill((0, 0, 0, 0))
        txt = Styles.SANS_B3.render("일간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(82, 8, txt.get_size()))
        txt = Styles.SANS_H5.render("월간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(227, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("교시별 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(372, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("시간별 좌석", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(517, 8, txt.get_size()))
        self.Selection_X_   = 145


    def period(self):
        """ "교시별 출석부"로 상단 바 선택란 위치 조정 """
        self.POS_X = 660
        self.SURFACE_.fill((0, 0, 0, 0))
        txt = Styles.SANS_B3.render("일간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(82, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("월간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(227, 8, txt.get_size()))
        txt = Styles.SANS_H5.render("교시별 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(372, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("시간별 좌석", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(517, 8, txt.get_size()))
        self.Selection_X_   = 290


    def arrangement(self):
        """ "시간별 좌석"으로 상단 바 선택란 위치 조정 """
        self.POS_X = 28
        self.SURFACE_.fill((0, 0, 0, 0))
        txt = Styles.SANS_B3.render("일간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(82, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("월간 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(227, 8, txt.get_size()))
        txt = Styles.SANS_B3.render("교시별 출석부", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(372, 8, txt.get_size()))
        txt = Styles.SANS_H5.render("시간별 좌석", 1, Styles.DARKGRAY)
        self.SURFACE_.blit(txt, center_top(517, 8, txt.get_size()))
        self.Selection_X_   = 435

        
    
    def Reset(self):
        self.POS_X = 660
        self.X = self.POS_X
        self._X = self.X
        self.Selection_X    = 3
        self.Selection_X_   = 3
        self.Updated        = True
        self.attendance()

    
    def Update(self, A_OFFSET: float) -> bool:

        if self.Selection_X != self.Selection_X_:
            self.Updated = True
            self.Selection_X = Animate(self.Selection_X, self.Selection_X_, 2.0, A_OFFSET)

        if self.POS_X != self.X:
            self.Updated = True
            self.Animate_X(self.POS_X, 1.25, A_OFFSET)

        return self.Updated
    

    def Frame(self, DISP: Surface):
        self.Updated = False

        DISP.fill(Styles.SPRLIGHTGRAY, self.calculateTrailRect_X())
        DISP.blit(self.Asset_Bar, (self.X, 15))
        DISP.blit(self.Asset_Selection, (self.X + self.Selection_X, 15))
        DISP.blit(self.SURFACE_, (self.X, 15))

        return self.calculateRect()
