
from .Component import Component
from pygame import Surface
from ..chairyData import StudentData, ChairyData
from .Styles import Styles
from datetime import datetime
from .Scene import SceneManager as SM

from ..optimization.positioning import center_center, right_top



class StudentInfoBox(Component):
    """ ### 입력된 학생 정보 """

    Asset_Frame_Normal  : Surface
    Asset_Frame_Reserved: Surface

    SURFACE: Surface

    Alpha   : float
    Updated : bool
    Show    : bool


    @staticmethod
    def timeStr(dt: datetime) -> tuple[str]:
        """
        datetime 클래스를 읽을 수 있는 문자열로 변환함.
        - - -
        #### 매개변수:
        - **dt:** 문자열로 변환할 시간
        """
        if dt.hour > 12:
            return ('오후', dt.strftime(f"{dt.hour - 12:02d}:%M"))
        elif dt.hour == 12:
            return ('오후', dt.strftime("12:%M"))
        elif dt.hour == 0:
            return ('오전', dt.strftime("12:%M"))
        else:
            return ('오전', dt.strftime("%H:%M"))


    def __init__(self, x = 120, y = 1080):
        super().__init__(x, y, 290, 450)
        
        self.SURFACE = Surface((290, 450))
        self.Asset_Frame_Normal   = SM.loadAsset("/ChairyApp/assets/components/StudentInfo0.png").convert(self.SURFACE)
        self.Asset_Frame_Reserved = SM.loadAsset("/ChairyApp/assets/components/StudentInfo1.png").convert(self.SURFACE)

        self.Reset()

        
    def show(self):
        """ 표시 """
        self.Show = True

    def hide(self):
        """ 가리기 """
        self.Show = False


    def info(self, SID: str):
        """
        학생 정보를 업데이트하고 내부 Surface를 렌더링함.
        - - -
        #### 매개변수:
        - **SID:** 학번
        """
        self.SURFACE.fill(Styles.SPRLIGHTGRAY, (0, 0, 290, 4))

        sd: StudentData = ChairyData.STUDENTS[SID]

        if not sd.SeatReserved:
            self.SURFACE.blit(self.Asset_Frame_Normal, (0, 4))

            if sd.LastUsedSeat != None:
                t = Styles.ANTON_H4.render(sd.LastUsedSeat, 1, Styles.PURPLE, Styles.WHITE)
                self.SURFACE.blit(t, center_center(217, 311, t.get_size()))
            else:
                t = Styles.ANTON_H4.render("?", 1, Styles.DARKGRAY, Styles.WHITE)
                self.SURFACE.blit(t, center_center(217, 311, t.get_size()))

        else:
            self.SURFACE.blit(self.Asset_Frame_Reserved, (0, 4))

            if sd.ReservedSeat != None:
                t = Styles.SANS_H3.render(sd.ReservedSeat, 1, Styles.PURPLE, Styles.WHITE)
                self.SURFACE.blit(t, center_center(217, 311, t.get_size()))        

        t = Styles.SANS_H4.render(sd.Name, 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        self.SURFACE.blit(t, right_top(280, -4, t.get_size()))

        for i in range(7):
            if sd.WeeklyCheckInStamp[i]:
                self.SURFACE.fill(Styles.GREEN, (27 + 35 * i, 119, 25, 30))
        self.SURFACE.fill(Styles.ORANGE, (27 + 35 * ChairyData.ROOMDATA.DATA_DATE.weekday(), 119, 25, 30))
        
        if sd.LastChkIn != None:
            ts = StudentInfoBox.timeStr(sd.LastChkIn)

            self.SURFACE.blit(Styles.SANS_H5.render(ts[0], 1, Styles.BLUE, Styles.WHITE), (20, 222))
            t = Styles.ANTON_H3.render(ts[1], 1, Styles.BLUE, Styles.WHITE)
            self.SURFACE.blit(t, right_top(128, 202, t.get_size()))
        else:
            self.SURFACE.blit(Styles.SANS_H4.render("기록 없음", 1, Styles.GRAY, Styles.WHITE), (22, 209))

        if sd.LastChkOut != None:
            ts = StudentInfoBox.timeStr(sd.LastChkOut)

            self.SURFACE.blit(Styles.SANS_H5.render(ts[0], 1, Styles.BLUE, Styles.WHITE), (163, 222))
            t = Styles.ANTON_H3.render(ts[1], 1, Styles.BLUE, Styles.WHITE)
            self.SURFACE.blit(t, right_top(271, 202, t.get_size()))
        else:
            self.SURFACE.blit(Styles.SANS_H4.render("기록 없음", 1, Styles.GRAY, Styles.WHITE), (165, 209))

        self.Updated = True



    def Reset(self, x = 120, y = 1080):
        self.MoveTo(x, y)

        self.Alpha = 255.
        self.Updated = False
        self.Show   = False


    def Update(self, A_OFFSET, TICK: int):
        updated = False
        
        if self.Show:

            if self.Y != 374:
                updated = True

            self.Animate_Y(374, 1.0, A_OFFSET)

            if self.Alpha < 255:
                self.Alpha += TICK * 1.5

                if self.Alpha > 255:
                    self.Alpha = 255

                updated = True

        else:

            if self.Y != 1080:
                updated = True

            self.AnimateSpdUp_Y(False, 340, 1080, 1.0, A_OFFSET)

            if self.Alpha > 0:
                self.Alpha -= TICK

                if self.Alpha < 0:
                    self.Alpha = 0

                updated = True
        
        return (self.Updated or updated)
    

    def Frame(self, DISP: Surface):
        self.Updated = False

        self.SURFACE.set_alpha(self.Alpha)

        r = self.calculateRect()

        DISP.fill(Styles.SPRLIGHTGRAY, r)
        DISP.blit(self.SURFACE, (self.X, self.Y))

        return r
    

    def getSurface(self):
        return self.SURFACE.copy()