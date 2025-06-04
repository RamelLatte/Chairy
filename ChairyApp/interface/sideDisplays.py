
from datetime import datetime
from pygame import Surface, draw, gfxdraw
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
            return self.DateTime.strftime(f"오후 {self.DateTime.hour - 12}:%M")
        elif self.DateTime.hour == 12:
            return self.DateTime.strftime(f"오후 12:%M")
        elif self.DateTime.hour == 0:
            return self.DateTime.strftime("오전 12:%M")
        else:
            return self.DateTime.strftime("오전 %H:%M")

    

    def Reset(self):
        self.DateTime = datetime.now()
        self.minute = self.DateTime.minute
        self.Updated = True


    def Update(self):
        return self.Updated


    def Frame(self, DISP):
        draw.rect(DISP, Styles.SPRLIGHTGRAY, (1575, 35, 300, 50))
        DISP.blit(Styles.SANS_H4.render(self.DateTime.strftime("%m월 %d일"), 1, Styles.BLACK, Styles.SPRLIGHTGRAY), (1575, 46))

        tmp: Surface = Styles.SANS_H5.render(self.timeStr(), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        DISP.blit(tmp, right_top(1875, 35, tmp.get_size()))

        weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        tmp = Styles.SANS_B3.render(weekdays[self.DateTime.weekday()], 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
        DISP.blit(tmp, right_bottom(1875, 85, tmp.get_size()))
        self.Updated = False
        return array('i', (1575, 35, 300, 50))

    
        

class DietAndScheduleDisplay(Component):
    """ ### 식단 및 학사 일정표 """

    BasementAsset   : Surface
    Updated         : bool



    def __init__(self):
        super().__init__(1575, 391, 300, 648)

        self.BasementAsset = SM.loadAsset("/ChairyApp/assets/components/DietScheduleFrame.png").convert()
        self.Updated = False

    
    def Reset(self):
        self.Updated = False

    
    def Update(self):
        return True
    

    def Frame(self, DISP):
        DISP.blit(self.BasementAsset, (1575, 391))
        DISP.blit(Styles.SANS_H5.render(ChairyData.NEISDATA.DinnerInfoDate + "의 저녁 식단", 1, Styles.BLACK, Styles.WHITE), (1635, 416))

        if len(ChairyData.NEISDATA.Dish) > 0:
            for i in range(len(ChairyData.NEISDATA.Dish)):
                DISP.blit(Styles.SANS_B3.render(ChairyData.NEISDATA.Dish[i], 1, Styles.BLACK, Styles.WHITE), (1600, 457 + 30 * i))

            tmp = Styles.SANS_B3.render(ChairyData.NEISDATA.Kcal, 1, Styles.BLACK, Styles.WHITE)
            DISP.blit(tmp, right_top(1830, 717, tmp.get_size()))
        else:
            if ChairyData.NEISDATA.ErrorCode is None:
                txt = Styles.SANS_B3.render("식단 정보가 없습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            else:
                txt = Styles.SANS_B3.render("오류가 발생했습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            DISP.blit(txt, center_top(1722, 567, txt.get_size()))
            DISP.fill(Styles.WHITE, (1830, 717, 20, 22))

        if len(ChairyData.NEISDATA.Events) > 0:
            for i in range(len(ChairyData.NEISDATA.Events)):
                if ChairyData.NEISDATA.Events[i][1] == '해당없음' or ChairyData.NEISDATA.Events[i][1] == '해당 없음':
                    gfxdraw.aacircle(DISP, 1605, 866 + i * 61, 5, Styles.GREEN)
                    gfxdraw.filled_circle(DISP, 1605, 866 + i * 61, 5, Styles.GREEN)
                    DISP.blit(Styles.SANS_B5.render("영업일", 1, Styles.BLACK, Styles.WHITE), (1617, 880 + 61 * i))
                elif ChairyData.NEISDATA.Events[i][1] == '휴업일':
                    gfxdraw.aacircle(DISP, 1605, 866 + i * 61, 5, Styles.BLUE)
                    gfxdraw.filled_circle(DISP, 1605, 866 + i * 61, 5, Styles.BLUE)
                    DISP.blit(Styles.SANS_B5.render("휴업일", 1, Styles.BLACK, Styles.WHITE), (1617, 880 + 61 * i))
                elif ChairyData.NEISDATA.Events[i][1] == '공휴일':
                    gfxdraw.aacircle(DISP, 1605, 866 + i * 61, 5, Styles.RED)
                    gfxdraw.filled_circle(DISP, 1605, 866 + i * 61, 5, Styles.RED)
                    DISP.blit(Styles.SANS_B5.render("공휴일", 1, Styles.BLACK, Styles.WHITE), (1617, 880 + 61 * i))
                else:
                    gfxdraw.aacircle(DISP, 1605, 866 + i * 61, 5, Styles.YELLOW)
                    gfxdraw.filled_circle(DISP, 1605, 866 + i * 61, 5, Styles.YELLOW)
                    DISP.blit(Styles.SANS_B5.render("기타", 1, Styles.BLACK, Styles.WHITE), (1617, 880 + 61 * i))

                DISP.blit(Styles.SANS_B3.render(ChairyData.NEISDATA.Events[i][0], 1, Styles.BLACK, Styles.WHITE), (1617, 855 + 61 * i))

        else:
            if ChairyData.NEISDATA.ErrorCode is None:
                txt = Styles.SANS_B3.render("오늘 일정이 없습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            else:
                txt = Styles.SANS_B3.render("오류가 발생했습니다.", 1, Styles.DARKGRAY, Styles.WHITE)
            DISP.blit(txt, center_top(1722, 910, txt.get_size()))

        return array('i', (1575, 391, 300, 648))
    



class SeatingStatus(Component):
    """ ### 입실 현황황 """

    Asset       : Surface
    Bar         : Surface
    Updated     : bool

    Total   : int
    Occupied: int
    Users   : int
    Students: int

    Bar_Length_: float
    Bar_Length: float
    
    TxtTotal: Surface
    TxtOccupied: Surface
    TxtTotalUser: Surface
    TxtPercent: Surface
    TxtTotalStudent: Surface



    def __init__(self):
        super().__init__(1572, 124, 300, 218)

        self.Asset      = SM.loadAsset("/ChairyApp/assets/components/SeatingStatus.png").convert()
        self.Bar        = SM.loadAsset("/ChairyApp/assets/components/SeatingStatusBar.png").convert()
        self.Updated    = True
        self.Bar_Length_ = 0
        self.RoomUpdated()


    def RoomUpdated(self):
        """ RoomData가 업데이트 되었을 때 호출하며, 입실 현황을 갱신하고 내부 렌더링 작업을 수행함. """
        self.Updated = True
        self.Total       = 0
        self.Occupied    = 0
        self.Users       = len(ChairyData.ROOMDATA.UserNames)
        self.Students    = len(ChairyData.STUDENTS)

        for value in ChairyData.ROOMDATA.Current.values():
            self.Total += 1
            if 'OCC' in value[0] or 'RES' in value[0]:
                self.Occupied += 1

        self.TxtTotal = Styles.SANS_H5.render("전체 " + str(self.Total) + "석 중", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY)
        self.TxtOccupied = Styles.SANS_H5.render(str(self.Occupied) + "석 이용 중", 1, Styles.BLUE, Styles.SPRLIGHTGRAY)
        self.TxtTotalUser = Styles.SANS_H4.render(str(self.Users) + "명", 1, Styles.WHITE, Styles.BLUE)
        self.TxtPercent = Styles.SANS_H5.render(str(round((self.Occupied / self.Total * 100), 1)) + "%", 1, Styles.BLUE, Styles.SPRLIGHTGRAY)
        self.TxtTotalStudent = Styles.SANS_H4.render(str(self.Students) + "명", 1, Styles.WHITE, Styles.GREEN)

        self.Bar_Length = 300 * (self.Occupied / self.Total)



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
        DISP.blit(self.Asset, (1572, 124))
        DISP.blit(self.TxtTotal, (1580, 174))
        DISP.blit(self.TxtOccupied, right_top(1862, 174, self.TxtOccupied.get_size()))
        DISP.blit(self.Bar.subsurface((0, 0, self.Bar_Length_, 15)), (1572, 202))
        DISP.blit(self.TxtTotalUser, center_top(1654, 280, self.TxtTotalUser.get_size()))
        DISP.blit(self.TxtTotalStudent, center_top(1812, 280, self.TxtTotalStudent.get_size()))
        DISP.blit(self.TxtPercent, center_top(1725, 221, self.TxtPercent.get_size()))
        return array('i', (1572, 124, 300, 218))