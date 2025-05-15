
from .Component import Component
from pygame import Surface, Rect
from ..chairyData import StudentData, ChairyData
from .Styles import Styles
from datetime import datetime
from .Scene import SceneManager as SM

from ..optimization.positioning import center_center



class StudentInfoBox(Component):
    """ ### 입력된 학생 정보 """

    Asset_Frame_Normal  : Surface
    Asset_Frame_Reserved: Surface
    Asset_Blue_Stamp    : Surface
    Asset_Yellow_Stamp  : Surface

    SURFACE: Surface

    Alpha   : float
    Updated : bool
    Show    : bool


    @staticmethod
    def timeStr(dt: datetime) -> str:
        """
        datetime 클래스를 읽을 수 있는 문자열로 변환함.
        - - -
        #### 매개변수:
        - **dt:** 문자열로 변환할 시간
        """
        if dt.hour > 12:
            return dt.strftime(f"오후 {dt.hour - 12}:%M")
        elif dt.hour == 12:
            return dt.strftime(f"오후 12:%M")
        elif dt.hour == 0:
            return dt.strftime("오전 12:%M")
        else:
            return dt.strftime("오전 %H:%M")


    def __init__(self, x = 123, y = 1080):
        super().__init__(x, y, 284, 548)
        
        self.SURFACE = Surface((284, 548))
        self.Asset_Frame_Normal   = SM.loadAsset("/ChairyApp/assets/components/StudentInfo1.png").convert(self.SURFACE)
        self.Asset_Frame_Reserved = SM.loadAsset("/ChairyApp/assets/components/StudentInfo2.png").convert(self.SURFACE)
        self.Asset_Blue_Stamp     = SM.loadAsset("/ChairyApp/assets/components/WeekStampBlue.png").convert(self.SURFACE)
        self.Asset_Yellow_Stamp   = SM.loadAsset("/ChairyApp/assets/components/WeekStampYellow.png").convert(self.SURFACE)

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
        sd: StudentData = ChairyData.STUDENTS[SID]

        if not sd.SeatReserved:
            self.SURFACE.blit(self.Asset_Frame_Normal, (0, 0))

            lastSeat = sd.getLastUsedSeat()

            if lastSeat != None:
                t = Styles.SANS_H3.render(lastSeat, 1, Styles.DARKGRAY, Styles.WHITE)
                self.SURFACE.blit(t, center_center(142, 517, t.get_size()))        
            else:
                t = Styles.SANS_H3.render("기록 없음", 1, Styles.DARKGRAY, Styles.WHITE)
                self.SURFACE.blit(t, center_center(142, 517, t.get_size()))        

        else:
            self.SURFACE.blit(self.Asset_Frame_Reserved, (0, 0))

            if sd.ReservedSeat != None:
                t = Styles.SANS_H3.render(sd.ReservedSeat, 1, Styles.DARKGRAY, Styles.WHITE)
                self.SURFACE.blit(t, center_center(142, 517, t.get_size()))        

        t = Styles.SANS_H3.render(sd.Name, 1, Styles.BLUE, Styles.WHITE)
        self.SURFACE.blit(t, center_center(142, 67, t.get_size()))

        for i in range(7):
            if sd.WeeklyCheckInStamp[i]:
                self.SURFACE.blit(self.Asset_Blue_Stamp, (42 * i, 172))
        self.SURFACE.blit(self.Asset_Yellow_Stamp, (42 * ChairyData.ROOMDATA.DATA_DATE.weekday(), 172))

        lastChkIn = sd.getLastCheckIn()
        
        if lastChkIn != None:
            t = Styles.SANS_H3.render(StudentInfoBox.timeStr(lastChkIn), 1, Styles.DARKGRAY, Styles.WHITE)
            self.SURFACE.blit(t, center_center(142, 293, t.get_size()))
        else:
            t = Styles.SANS_H3.render("기록 없음", 1, Styles.DARKGRAY, Styles.WHITE)
            self.SURFACE.blit(t, center_center(142, 293, t.get_size()))

        lastChkOut = sd.getLastCheckOut()

        if lastChkOut != None:
            t = Styles.SANS_H3.render(StudentInfoBox.timeStr(lastChkOut), 1, Styles.DARKGRAY, Styles.WHITE)
            self.SURFACE.blit(t, center_center(142, 405, t.get_size()))
        else:
            t = Styles.SANS_H3.render("기록 없음", 1, Styles.DARKGRAY, Styles.WHITE)
            self.SURFACE.blit(t, center_center(142, 405, t.get_size()))

        self.Updated = True



    def Reset(self, x = 123, y = 1080):
        self.MoveTo(x, y)

        self.Alpha = 255.
        self.Updated = False
        self.Show   = False


    def Update(self, A_OFFSET, TICK: int):
        updated = False
        
        if self.Show:

            if self.Y != 390:
                updated = True

            self.Animate_Y(390, 1.0, A_OFFSET)

            if self.Alpha < 255:
                self.Alpha += TICK * 1.5

                if self.Alpha > 255:
                    self.Alpha = 255

                updated = True

        else:

            if self.Y != 1080:
                updated = True

            self.AnimateSpdUp_Y(False, 356, 1080, 1.0, A_OFFSET)

            if self.Alpha > 0:
                self.Alpha -= TICK

                if self.Alpha < 0:
                    self.Alpha = 0

                updated = True
        
        return (self.Updated or updated)
    

    def Frame(self, DISP: Surface) -> Rect:
        self.Updated = False

        self.SURFACE.set_alpha(self.Alpha)

        r = self.calculateRect()

        DISP.fill(Styles.SPRLIGHTGRAY, r)
        DISP.blit(self.SURFACE, (self.X, self.Y))

        return r