
from .Component import Component
from . import Styles
from pygame import Surface, Rect
from ..chairyData import ChairyData as CD
from .Scene import SceneManager as SM
import calendar, datetime
from os.path import exists

from ..optimization.positioning import collidepoint, center_top, center_bottom



class DateSelectionTemplate(Component):
    """ ### 날짜 선택란 기본 틀 """

    SURFACE: Surface

    ResetBtns: list[Surface]
    ResetBtn : int

    TodayBtns: list[Surface]
    TodayBtn : int

    Calendar: list[list[int]]

    Calendar_R: list[Rect]
    Calendar_0: list[Surface] # 기본 상태
    Calendar_1: list[Surface] # 마우스가 위에 있는 상태
    Calendar_2: list[Surface] # 마우스를 클릭한 상태
    Calendar_D: list[int]
    Calendar_S: list[bool]

    Year : int
    Month: int

    Current: int
    
    SelectedDate: datetime.date

    Updated : bool

    Hover: int
    Clicked: int


    def __init__(self):
        super().__init__()
        self.Reset()


    def _Render(self, update_surface: bool = True):
        """ 내부 캘린더 렌더링 작업 """

        calendar.setfirstweekday(calendar.SUNDAY)
        self.Calendar = calendar.monthcalendar(self.Year, self.Month)
        self.Calendar_R.clear()
        self.Calendar_0.clear()
        self.Calendar_1.clear()
        self.Calendar_2.clear()
        self.Calendar_D.clear()
        self.Calendar_S.clear()

        tmpSurface : Surface

        for week in range(len(self.Calendar)): # 주차
            for weekday, day in enumerate(self.Calendar[week]): # 요일

                if day == 0:
                    continue

                self.Calendar_D.append(day)

                # 선택된 날짜에 해당되는 경우
                if self.Year == self.SelectedDate.year and self.Month == self.SelectedDate.month and day == self.SelectedDate.day:
                    tmpSurface = Surface((35, 35))
                    tmpSurface.fill(Styles.DARKGRAY)
                    txt = Styles.SANS_H5.render(str(day), 1, Styles.WHITE, Styles.DARKGRAY)
                    tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                    self.Calendar_0.append(tmpSurface)
                    self.Calendar_1.append(tmpSurface)
                    self.Calendar_2.append(tmpSurface)
                    self.Calendar_S.append(True)
                
                # 오늘인 경우
                elif self.Month == CD.ROOMDATA.DATA_DATE.month and self.Year == CD.ROOMDATA.DATA_DATE.year and day == CD.ROOMDATA.DATA_DATE.day:
                    tmpSurface = Surface((35, 35))
                    tmpSurface.fill(Styles.SPRLIGHTGRAY)
                    txt = Styles.SANS_H5.render(str(day), 1, Styles.BLUE, Styles.SPRLIGHTGRAY)
                    tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                    self.Calendar_0.append(tmpSurface)

                    tmpSurface = Surface((35, 35))
                    tmpSurface.fill(Styles.LIGHTBLUE)
                    txt = Styles.SANS_H5.render(str(day), 1, Styles.WHITE, Styles.LIGHTBLUE)
                    tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                    self.Calendar_1.append(tmpSurface)

                    tmpSurface = Surface((35, 35))
                    tmpSurface.fill(Styles.BLUE)
                    txt = Styles.SANS_H5.render(str(day), 1, Styles.LIGHTBLUE, Styles.BLUE)
                    tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                    self.Calendar_2.append(tmpSurface)
                    self.Calendar_S.append(True)

                # 그 이외인 경우
                else:
                    # 통계가 있으면
                    if self.Enabled(self.Year, self.Month, day):
                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.SPRLIGHTGRAY)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_0.append(tmpSurface)
                        
                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.LIGHTGRAY)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.DARKGRAY, Styles.LIGHTGRAY)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_1.append(tmpSurface)

                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.GRAY)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.LIGHTGRAY, Styles.GRAY)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_2.append(tmpSurface)

                        self.Calendar_S.append(True)

                    # 통계가 없으면
                    else:
                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.WHITE)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.LIGHTGRAY, Styles.WHITE)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_0.append(tmpSurface)
                        self.Calendar_1.append(tmpSurface)
                        self.Calendar_2.append(tmpSurface)
                        self.Calendar_S.append(False)


                self.Calendar_R.append(Rect(weekday * 43, 46 + (week * 43), 35, 35))

        if update_surface:
            self._Surface()


    # Overridable
    def Enabled(self) -> bool:
        """ 그 일자의 데이터가 존재하는지 여부 """
        return False


    def _Surface(self):
        """ 내부 Surface 갱신 """

        self.SURFACE.fill(Styles.WHITE)

        # 년/월
        txt = Styles.SANS_H4.render(str(self.Year) + "년 " + str(self.Month) + "월", 1, Styles.BLACK, Styles.WHITE)
        self.SURFACE.blit(txt, center_top(146, 0, txt.get_size()))

        # 선택한 날짜로 돌아가기
        self.SURFACE.blit(self.ResetBtns[self.ResetBtn], (0, 304))

        # 오늘 날짜로 돌아가기
        self.SURFACE.blit(self.TodayBtns[self.TodayBtn], (220, 304))

        # 스크롤 안내문
        txt = Styles.SANS_B4.render("스크롤하여 년/월을 바꿉니다.", 1, Styles.DARKGRAY, Styles.WHITE)
        self.SURFACE.blit(txt, center_bottom(146, 358, txt.get_size()))

        # 캘린더
        for i in range(len(self.Calendar_R)):
            if i != self.Hover and i != self.Clicked:
                self.SURFACE.blit(self.Calendar_0[i], self.Calendar_R[i])

        if self.Clicked != -1:
            self.SURFACE.blit(self.Calendar_2[self.Clicked], self.Calendar_R[self.Clicked])
        elif self.Hover != -1:
            self.SURFACE.blit(self.Calendar_1[self.Hover], self.Calendar_R[self.Hover])

        self.Updated = True


    
    def Reset(self, x = 108, y = 361):
        self.X = x
        self.Y = y
        self.SURFACE = Surface((293, 358))
        self.SelectedDate = CD.ROOMDATA.DATA_DATE
        self.Year = CD.ROOMDATA.DATA_DATE.year
        self.Month = CD.ROOMDATA.DATA_DATE.month
        self.Hover = -1
        self.Clicked = -1

        self.Calendar_R = []
        self.Calendar_0 = []
        self.Calendar_1 = []
        self.Calendar_2 = []
        self.Calendar_D = []
        self.Calendar_S = []

        self.ResetBtns = [
            SM.loadAsset('/ChairyApp/assets/statistics/Reset0.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/Reset1.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/Reset2.png').convert(self.SURFACE)
        ]
        self.ResetBtn = 0

        self.TodayBtns = [
            SM.loadAsset('/ChairyApp/assets/statistics/Today0.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/Today1.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/Today2.png').convert(self.SURFACE)
        ]
        self.TodayBtn = 0

        self._Render()


    def Update(self):
        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False
        return DISP.blit(self.SURFACE, (self.X, self.Y))
    


    def MouseButtonDown(self, POS, BUTTON): # 4: 스크롤 올림, 5: 스크롤 내림
        
        if not collidepoint(self.X - 28, self.Y - 16, 350, 420, POS):
            return

        if BUTTON == 4:
            self.Month -= 1

            if self.Month == 0:
                self.Year -= 1
                self.Month = 12

            self._Render(False)

            self.MouseMotion(POS)

            self._Surface()

        elif BUTTON == 5:
            self.Month += 1

            if self.Month == 13:
                self.Year += 1
                self.Month = 1

            self._Render(False)

            self.MouseMotion(POS)

            self._Surface()

        elif BUTTON == 1:

            if collidepoint(self.X, self.Y + 304, 209, 30, POS):
                self.ResetBtn = 2
                self._Surface()
                return
            
            if collidepoint(self.X + 220, self.Y + 304, 73, 30, POS):
                self.TodayBtn = 2
                self._Surface()
                return
            
            self.Clicked = -1
        
            for ri, rect in enumerate(self.Calendar_R):

                if rect.collidepoint(POS[0] - self.X, POS[1] - self.Y):
                    self.Clicked = ri
                    break
            
            self._Surface()


    def MouseButtonUp(self, POS, BUTTON):
        if BUTTON != 1:
            return None
        
        if self.ResetBtn > 0:
            self.ResetBtn = 0
            self.Year = self.SelectedDate.year
            self.Month = self.SelectedDate.month
            self._Render(True)
            return None
        
        if self.TodayBtn > 0:
            self.TodayBtn = 0
            self.SelectedDate = CD.ROOMDATA.DATA_DATE
            self.Year = self.SelectedDate.year
            self.Month = self.SelectedDate.month
            self._Render(True)
            return CD.ROOMDATA.DATA_DATE
        
        date = None
        if self.Clicked != -1:
            if self.Clicked == self.Hover:
                date = datetime.date(self.Year, self.Month, self.Calendar_D[self.Clicked])
                self.SelectedDate = date
            if not self.Calendar_S[self.Clicked]:
                return None
            self.Clicked = -1
            self._Surface()

        return date


    def MouseMotion(self, POS):

        if self.ResetBtn < 2:
            if collidepoint(self.X, self.Y + 304, 209, 30, POS):
                self.ResetBtn = 1
            else:
                self.ResetBtn = 0

        if self.TodayBtn < 2:
            if collidepoint(self.X + 220, self.Y + 304, 73, 30, POS):
                self.TodayBtn = 1
            else:
                self.TodayBtn = 0

        if not collidepoint(self.X - 28, self.Y - 16, 350, 420, POS):
            self.TodayBtn = 0
            self.ResetBtn = 0

            if self.Clicked != -1:
                self.Clicked = -1
            if self.Hover != -1:
                self.Hover = -1
                
            self._Surface()
            return

        self.Hover = -1
        
        for ri, rect in enumerate(self.Calendar_R):

            if rect.collidepoint(POS[0] - self.X, POS[1] - self.Y):
                self.Hover = ri
                break

        if self.Hover != -1 and self.Clicked != -1 and self.Clicked != self.Hover:
            self.Clicked = self.Hover
        
        self._Surface()




class DateSelection(DateSelectionTemplate):
    """ ### 년/월/일 선택란 """

    def Enabled(self, year: int, month: int, day: int):
        return exists(datetime.date(year, month, day).strftime(SM.DIRECTORY + '/RoomData/%Y%m/%Y%m%d.json'))




class MonthSelection(Component):
    """ ### 년/월 선택란 """

    SURFACE: Surface

    Asset   : Surface

    ResetBtns: list[Surface]
    ResetBtn : int

    Calendar: list[list[int]]

    Calendar_R: list[Rect]
    Calendar_0: list[Surface] # 기본 상태
    Calendar_D: list[int]

    Year : int
    Month: int

    Current: int

    Updated : bool


    def __init__(self):
        super().__init__()
        self.Reset()


    def _Render(self, update_surface: bool = True):
        """ 내부 캘린더 렌더링 작업 """

        calendar.setfirstweekday(calendar.SUNDAY)
        self.Calendar = calendar.monthcalendar(self.Year, self.Month)
        self.Calendar_R.clear()
        self.Calendar_0.clear()
        self.Calendar_D.clear()

        tmpSurface : Surface

        for week in range(len(self.Calendar)): # 주차
            for weekday, day in enumerate(self.Calendar[week]): # 요일

                if day == 0:
                    continue

                self.Calendar_D.append(day)

                # 오늘인 경우
                if self.Month == CD.ROOMDATA.DATA_DATE.month and self.Year == CD.ROOMDATA.DATA_DATE.year and day == CD.ROOMDATA.DATA_DATE.day:
                    tmpSurface = Surface((35, 35))
                    tmpSurface.fill(Styles.DARKGRAY)
                    txt = Styles.SANS_H5.render(str(day), 1, Styles.WHITE, Styles.DARKGRAY)
                    tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                    self.Calendar_0.append(tmpSurface)

                # 그 이외인 경우
                else:
                    # 통계가 있으면
                    if SM.exists(datetime.date(self.Year, self.Month, day).strftime('/RoomData/%Y%m/%Y%m%d.json')):
                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.BLUE)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.WHITE, Styles.BLUE)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_0.append(tmpSurface)

                    # 통계가 없으면
                    else:
                        tmpSurface = Surface((35, 35))
                        tmpSurface.fill(Styles.LIGHTRED)
                        txt = Styles.SANS_H5.render(str(day), 1, Styles.WHITE, Styles.LIGHTRED)
                        tmpSurface.blit(txt, center_top(17, 7, txt.get_size()))
                        self.Calendar_0.append(tmpSurface)

                self.Calendar_R.append(Rect(weekday * 43, 76 + (week * 43), 35, 35))

        if update_surface:
            self._Surface()


    # Overridable
    def Enabled(self) -> bool:
        return False


    def _Surface(self):
        """ 내부 Surface 갱신 """

        self.SURFACE.fill(Styles.WHITE)

        # 년/월
        txt = Styles.SANS_H4.render(str(self.Year) + "년 " + str(self.Month) + "월", 1, Styles.BLACK, Styles.WHITE)
        self.SURFACE.blit(txt, center_top(146, 0, txt.get_size()))

        # 이번 달로 되돌리기
        self.SURFACE.blit(self.ResetBtns[self.ResetBtn], (42, 334))

        # 스크롤 안내문
        txt = Styles.SANS_B4.render("스크롤하여 년/월을 바꿉니다.", 1, Styles.DARKGRAY, Styles.WHITE)
        self.SURFACE.blit(txt, center_bottom(146, 388, txt.get_size()))

        # 상태 구분 안내
        self.SURFACE.blit(self.Asset, (23, 42))

        # 캘린더
        for i, r in enumerate(self.Calendar_R):
            self.SURFACE.blit(self.Calendar_0[i], r)

        self.Updated = True


    
    def Reset(self, x = 108, y = 342):
        self.X = x
        self.Y = y
        self.SURFACE = Surface((293, 388))
        self.Year = CD.ROOMDATA.DATA_DATE.year
        self.Month = CD.ROOMDATA.DATA_DATE.month

        self.Calendar_R = []
        self.Calendar_0 = []
        self.Calendar_D = []

        self.Asset = SM.loadAsset('/ChairyApp/assets/statistics/MonthSelection.png').convert(self.SURFACE)

        self.ResetBtns = [
            SM.loadAsset('/ChairyApp/assets/statistics/ResetMonth0.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/ResetMonth1.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/statistics/ResetMonth2.png').convert(self.SURFACE)
        ]
        self.ResetBtn = 0

        self._Render()

    
    def Update(self):
        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False
        return DISP.blit(self.SURFACE, (self.X, self.Y))
    

    def MouseButtonDown(self, POS, BUTTON): # 4: 스크롤 올림, 5: 스크롤 내림
        
        if not collidepoint(self.X - 28, self.Y - 16, 350, 420, POS):
            return None

        if BUTTON == 4:
            self.Month -= 1

            if self.Month == 0:
                self.Year -= 1
                self.Month = 12

            self._Render(False)

            self.MouseMotion(POS)

            self._Surface()

        elif BUTTON == 5:
            self.Month += 1

            if self.Month == 13:
                self.Year += 1
                self.Month = 1

            self._Render(False)

            self.MouseMotion(POS)

            self._Surface()

        elif BUTTON == 1 and collidepoint(self.X + 42, self.Y + 334, 209, 30, POS):
                self.ResetBtn = 2
                self._Surface()

        return (self.Year, self.Month)


    def MouseButtonUp(self, POS, BUTTON):
        if BUTTON != 1:
            return False
        
        if self.ResetBtn > 0:
            self.ResetBtn = 0
            self.Year = CD.ROOMDATA.DATA_DATE.year
            self.Month = CD.ROOMDATA.DATA_DATE.month
            self._Render(True)
            return True
        
        return False


    def MouseMotion(self, POS):

        if self.ResetBtn < 2:
            if collidepoint(self.X + 42, self.Y + 334, 209, 30, POS):
                self.ResetBtn = 1
            else:
                self.ResetBtn = 0

        if not collidepoint(self.X - 28, self.Y - 16, 350, 420, POS):
            self.ResetBtn = 0
            return
        
        self._Surface()