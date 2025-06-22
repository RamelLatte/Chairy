
from datetime import datetime
from pygame import Surface, draw, gfxdraw, SRCALPHA
from .Component import Component
from .Styles import Styles
from .Scene import SceneManager as SM
from ..chairyData import ChairyData
from array import array

from ..optimization.animation import Animate
from ..optimization.positioning import right_top, right_bottom, center_top



class DateTimeDisplay(Component):
    """ ### 날짜 및 시간 """

    DateTime    : datetime
    Updated     : bool



    def __init__(self):
        super().__init__(1575, 35, 300, 50)

        self.Reset()


    def minuteChanged(self):
        """ 매 분마다 호출해야함. """
        self.DateTime = datetime.now()
        self.Updated = True


    def timeStr(self) -> str:
        """ 시간을 읽을 수 있는 문자열로 변환. """
        if self.DateTime.hour > 12:
            return self.DateTime.strftime(f"PM {self.DateTime.hour - 12:02d}:%M")
        elif self.DateTime.hour == 12:
            return self.DateTime.strftime(f"PM 12:%M")
        elif self.DateTime.hour == 0:
            return self.DateTime.strftime("AM 12:%M")
        else:
            return self.DateTime.strftime("AM %H:%M")

    

    def Reset(self):
        self.DateTime = datetime.now()
        self.minute = self.DateTime.minute
        self.Updated = True


    def Update(self):
        return self.Updated


    def Frame(self, DISP):
        draw.rect(DISP, Styles.SPRLIGHTGRAY, (1567, 50, 302, 51))

        # 시간 렌더링
        tmp: Surface = Styles.ANTON_H2.render(self.timeStr(), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        DISP.blit(tmp, (1567, 52))

        # 날짜 렌더링
        tmp = Styles.SANS_H4.render(self.DateTime.strftime("%m월 %d일"), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        DISP.blit(tmp, right_top(1869, 48, tmp.get_size()))

        # 요일 렌더링
        weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        tmp = Styles.SANS_B3.render(weekdays[self.DateTime.weekday()], 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        DISP.blit(tmp, right_bottom(1869, 106, tmp.get_size()))
        self.Updated = False
        return array('i', (1567, 48, 302, 54))

    
        

class DietAndScheduleDisplay(Component):
    """ ### 식단 및 학사 일정표 """

    ScheduleFrame   : Surface
    DietFrame       : Surface
    Updated         : bool


    def __init__(self):
        super().__init__(1575, 391, 300, 648)

        self.ScheduleFrame = SM.loadAsset("/ChairyApp/assets/components/ScheduleFrame.png").convert()
        self.DietFrame     = SM.loadAsset("/ChairyApp/assets/components/DietFrame.png").convert()
        self.Updated = False

    
    def Reset(self):
        self.Updated = False

    
    def Update(self):
        return True
    

    def Frame(self, DISP):
        # 스케줄
        DISP.blit(self.ScheduleFrame, (1567, 129))

        if len(ChairyData.NEISDATA.Events) > 0:
            for i in range(len(ChairyData.NEISDATA.Events)):
                if ChairyData.NEISDATA.Events[i][1] == '해당없음' or ChairyData.NEISDATA.Events[i][1] == '해당 없음':
                    gfxdraw.aacircle(DISP, 1605, 170 + i * 61, 5, Styles.GREEN)
                    gfxdraw.filled_circle(DISP, 1605, 170 + i * 61, 5, Styles.GREEN)
                    DISP.blit(Styles.SANS_B5.render("영업일", 1, Styles.BLACK, Styles.WHITE), (1617, 184 + 61 * i))
                elif ChairyData.NEISDATA.Events[i][1] == '휴업일':
                    gfxdraw.aacircle(DISP, 1605, 170 + i * 61, 5, Styles.BLUE)
                    gfxdraw.filled_circle(DISP, 1605, 170 + i * 61, 5, Styles.BLUE)
                    DISP.blit(Styles.SANS_B5.render("휴업일", 1, Styles.BLACK, Styles.WHITE), (1617, 184 + 61 * i))
                elif ChairyData.NEISDATA.Events[i][1] == '공휴일':
                    gfxdraw.aacircle(DISP, 1605, 170 + i * 61, 5, Styles.RED)
                    gfxdraw.filled_circle(DISP, 1605, 170 + i * 61, 5, Styles.RED)
                    DISP.blit(Styles.SANS_B5.render("공휴일", 1, Styles.BLACK, Styles.WHITE), (1617, 184 + 61 * i))
                else:
                    gfxdraw.aacircle(DISP, 1605, 170 + i * 61, 5, Styles.YELLOW)
                    gfxdraw.filled_circle(DISP, 1605, 170 + i * 61, 5, Styles.YELLOW)
                    DISP.blit(Styles.SANS_B5.render("기타", 1, Styles.BLACK, Styles.WHITE), (1617, 184 + 61 * i))

                DISP.blit(Styles.SANS_B3.render(ChairyData.NEISDATA.Events[i][0], 1, Styles.BLACK, Styles.WHITE), (1617, 159 + 61 * i))

        else:
            if ChairyData.NEISDATA.ErrorCode is None:
                txt = Styles.SANS_B3.render("오늘 일정이 없습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            else:
                txt = Styles.SANS_B3.render("오류가 발생했습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            DISP.blit(txt, center_top(1722, 220, txt.get_size()))


        # 식단
        DISP.blit(self.DietFrame, (1567, 367))
        DISP.blit(Styles.SANS_H5.render(ChairyData.NEISDATA.DinnerInfoDate + "의 저녁 식단", 1, Styles.BLACK, Styles.WHITE), (1629, 392))

        if len(ChairyData.NEISDATA.Dish) > 0:
            for i in range(len(ChairyData.NEISDATA.Dish)):
                DISP.blit(Styles.SANS_B3.render(ChairyData.NEISDATA.Dish[i], 1, Styles.BLACK, Styles.WHITE), (1592, 433 + 30 * i))

            tmp = Styles.SANS_B3.render(ChairyData.NEISDATA.Kcal, 1, Styles.BLACK, Styles.WHITE)
            DISP.blit(tmp, right_top(1830, 693, tmp.get_size()))
        else:
            if ChairyData.NEISDATA.ErrorCode is None:
                txt = Styles.SANS_B3.render("식단 정보가 없습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            else:
                txt = Styles.SANS_B3.render("오류가 발생했습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            DISP.blit(txt, center_top(1722, 567, txt.get_size()))
            DISP.fill(Styles.WHITE, (1834, 694, 21, 21))

        return array('i', (1567, 129, 310, 608))
    



class SeatingStatus(Component):
    """ ### 입실 현황 """

    Asset       : Surface
    Bar         : Surface
    Updated     : bool

    Total   : int
    Occupied: int

    Bar_Length_: float
    Bar_Length: float
    
    Layer: Surface


    def __init__(self):
        super().__init__(1572, 124, 300, 218)

        self.Asset      = SM.loadAsset("/ChairyApp/assets/components/SeatingStatus.png").convert()
        self.Bar        = SM.loadAsset("/ChairyApp/assets/components/SeatingStatusBar.png").convert()
        self.Updated    = True
        self.Bar_Length_ = 0
        self.Layer = Surface((310, 100), SRCALPHA)
        self.RoomUpdated()


    def RoomUpdated(self):
        """ RoomData가 업데이트 되었을 때 호출하며, 입실 현황을 갱신하고 내부 렌더링 작업을 수행함. """
        self.Updated = True
        self.Total       = 0
        self.Occupied    = 0

        self.Layer.fill((0, 0, 0, 0))

        for value in ChairyData.ROOMDATA.Current.values():
            self.Total += 1
            if 'OCC' in value[0] or 'RES' in value[0]:
                self.Occupied += 1

        self.Layer.blit(Styles.SANS_H5.render("총", 1, Styles.DARKGRAY), (17, 36))
        tmp = Styles.ANTON_H4.render(str(self.Total), 1, Styles.DARKGRAY)
        self.Layer.blit(tmp, (38, 26))
        self.Layer.blit(Styles.SANS_H5.render("석 중", 1, Styles.DARKGRAY), (40 + tmp.get_width(), 36))

        self.Layer.blit(Styles.SANS_H5.render("석 이용 중", 1, Styles.ORANGE), (225, 36))
        tmp = Styles.ANTON_H3.render(str(self.Occupied), 1, Styles.ORANGE)
        self.Layer.blit(tmp, right_bottom(222, 66, tmp.get_size()))

        tmp = Styles.ANTON_H5.render(str(round((self.Occupied / self.Total * 100), 1)) + "%", 1, Styles.ORANGE)
        self.Layer.blit(tmp, (240, 59))

        self.Bar_Length = 220 * (self.Occupied / self.Total)



    def Reset(self):
        self.Updated    = True
        self.Bar_Length_ = 0
        self.RoomUpdated()


    def Update(self, A_OFFSET):
        if self.Bar_Length != self.Bar_Length_:
            self.Bar_Length_ = Animate(self.Bar_Length_, self.Bar_Length, 1.0, A_OFFSET)
            self.Updated = True
        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False
        DISP.blit(self.Asset, (1567, 765))
        DISP.blit(self.Layer, (1567, 765))
        DISP.blit(self.Bar.subsurface((0, 0, min(self.Bar_Length_, 220), 15)), (1580, 832))
        return array('i', (1567, 765, 310, 100))
    


class QuickAccessButtons(Component):

    Buttons: tuple[tuple[Surface]]

    Hover: int
    Clicked: int

    _Hover: int
    _Clicked: int

    Updated: bool
    Enabled: bool


    def __init__(self):
        self.Buttons = (
            (
                SM.loadAsset('/ChairyApp/assets/components/StatisticsButton0.png'),
                SM.loadAsset('/ChairyApp/assets/components/StatisticsButton1.png'),
                SM.loadAsset('/ChairyApp/assets/components/StatisticsButton2.png'),
                SM.loadAsset('/ChairyApp/assets/components/StatisticsButton3.png')
            ),
            (
                SM.loadAsset('/ChairyApp/assets/components/PhotoLibraryButton0.png'),
                SM.loadAsset('/ChairyApp/assets/components/PhotoLibraryButton1.png'),
                SM.loadAsset('/ChairyApp/assets/components/PhotoLibraryButton2.png'),
                SM.loadAsset('/ChairyApp/assets/components/PhotoLibraryButton3.png')
            ),
            (
                SM.loadAsset('/ChairyApp/assets/components/LogButton0.png'),
                SM.loadAsset('/ChairyApp/assets/components/LogButton1.png'),
                SM.loadAsset('/ChairyApp/assets/components/LogButton2.png'),
                SM.loadAsset('/ChairyApp/assets/components/LogButton3.png')
            ),
            (
                SM.loadAsset('/ChairyApp/assets/components/ResetButton0.png'),
                SM.loadAsset('/ChairyApp/assets/components/ResetButton1.png'),
                SM.loadAsset('/ChairyApp/assets/components/ResetButton2.png'),
                SM.loadAsset('/ChairyApp/assets/components/ResetButton3.png')
            )
        )

        self.Hover = -1
        self.Clicked = -1

        self._Hover = -1
        self._Clicked = -1

        self.Updated = True
        self.Enabled = True

        self.newMouseFields(4)
        self.setMouseField(0, 5, 5, 50, 50)
        self.setMouseField(1, 75, 0, 50, 50)
        self.setMouseField(2, 145, 0, 50, 50)
        self.setMouseField(3, 215, 0, 50, 50)

        super().__init__(1587, 885, 270, 80)


    def Update(self):
        return self.Updated
    

    def Reset(self):
        self.Hover = -1
        self.Clicked = -1

        self._Hover = -1
        self._Clicked = -1

        self.Updated = True
        self.Enabled = True
    

    def Frame(self, DISP):

        if self.Enabled:

            for i in range(4):

                if self.Hover == i:

                    if self.Clicked == self.Hover:
                        DISP.blit(self.Buttons[self.Hover][2], (1587 + i * 70, 885))

                    else:
                        DISP.blit(self.Buttons[self.Hover][1], (1587 + i * 70, 885))

                else:

                    DISP.blit(self.Buttons[i][0], (1587 + i * 70, 885))

        else:
            
            DISP.blit(self.Buttons[0][3], (1587, 885))
            DISP.blit(self.Buttons[1][3], (1657, 885))
            DISP.blit(self.Buttons[2][3], (1727, 885))
            DISP.blit(self.Buttons[3][3], (1797, 885))
        
        return array('i', (1587, 885, 270, 80))
    

    def MouseButtonDown(self, POS, BUTTON):

        if BUTTON != 1 or not self.Enabled:
            return
        
        self.Clicked = self.collideindex(POS)

        if self.Clicked != self._Clicked:
            self._Clicked = self.Clicked
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON):

        if BUTTON != 1 or not self.Enabled:
            return
        
        clicked = self.Clicked
        
        self.Clicked = -1

        if self.Clicked != self._Clicked:
            self._Clicked = self.Clicked
            self.Updated = True

        if clicked != -1 and clicked == self.Hover:
            return clicked
        
        return -1


    def MouseMotion(self, POS):

        if not self.Enabled:
            return
        
        self.Hover = self.collideindex(POS)

        if self.Hover != self._Hover:
            self._Hover = self.Hover
            self.Updated = True


    def disable(self):
        self.Clicked = -1
        self.Hover = -1
        self.Enabled = False
        self.Updated = True


    def enable(self):
        self.Enabled = True
        self.Updated = True