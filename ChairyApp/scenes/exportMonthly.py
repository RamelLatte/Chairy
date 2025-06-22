from ..interface import Scene, Styles, Interface, SceneManager
from ..chairyData import MonthlyStatistics, ChairyData
from pygame import Surface, constants, draw
from .dialog import Dialog

from ..optimization.positioning import center_top, center_bottom, right_top, right_bottom, collidepoint



class StatisticDialog(Dialog):

    Statistic: MonthlyStatistics

    def __init__(self, s: MonthlyStatistics):
        self.Statistic = s
        super().__init__("통계를 내보내는 중...", "「월간 출석부」 통계를 내보내고 있습니다.")


    def task(self):
        from time import sleep

        self.set("통계 내보내기 완료!", self.Statistic.Write() + '\n로 저장되었습니다.')
        sleep(2)




class ExportMonthly(Scene):
    """ ### 월간 출석부 내보내기 """

    Preview: Surface # 에셋
    PreviewScreen: Surface # 미리보기 Surface

    DateSelection: Surface # 에셋

    CurrentStatistics: MonthlyStatistics # 현재 통계 데이터
    CurrentDate: tuple[int] # 선택된 연도 및 월

    IDs: list[str] # 학번 모음

    Index_Vertical: int  # 세로 인덱스
    Index_Horizonal: int # 가로 인덱스

    Total_Vertical: int  # 세로 길이
    Total_Horizonal: int # 가로 길이

    ShiftDown: bool # Shift 키 눌림

    Updated: bool # 내부 Surface가 갱신되었는지 여부



    def __init__(self):
        self.Identifier = 'ExportMonthly'

        self.Preview = SceneManager.loadAsset('/ChairyApp/assets/statistics/PreviewMonthly.png').convert()
        self.DateSelection = SceneManager.loadAsset('/ChairyApp/assets/statistics/DateSelection.png').convert()
        self.CurrentDate = (ChairyData.ROOMDATA.DATA_DATE.year, ChairyData.ROOMDATA.DATA_DATE.month)

        self.Updated = False

    
    def _Preview(self):
        """ 미리보기 렌더링 """

        self.PreviewScreen = Surface((1365, 892))
        self.PreviewScreen.fill(Styles.SPRLIGHTGRAY, (1350, 0, 15, 892))
        self.PreviewScreen.fill(Styles.SPRLIGHTGRAY, (0, 889, 1365, 3))

        if self.CurrentStatistics.Empty:
            self.PreviewScreen.fill(Styles.SPRLIGHTGRAY)
            txt = Styles.SANS_H4.render(f"{self.CurrentDate[0]}년 {self.CurrentDate[1]}월 데이터가 없습니다.", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.PreviewScreen.blit(txt, center_top(687, 422, txt.get_size()))
            txt = Styles.SANS_B4.render("자료가 있는 다른 날짜를 선택해 주십시오.", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.PreviewScreen.blit(txt, center_top(687, 474, txt.get_size()))
        else:

            self.PreviewScreen.blit(self.Preview, (0,0))

            dtStr: str = self.CurrentStatistics.Statistics['_DATA_DATES'][self.Index_Horizonal]
            txt = Styles.SANS_H5.render(f'{dtStr[0:4]}년 {dtStr[4:6]}월 {dtStr[6:8]}일', 1, Styles.BLACK, Styles.GRAY)
            self.PreviewScreen.blit(txt, center_top(725, 47, txt.get_size()))
            
            for i in range(self.Index_Vertical, min(self.Total_Vertical, self.Index_Vertical + 14)):
                y = 132 + (50 * (i - self.Index_Vertical))
                id = self.IDs[i]

                if (i - self.Index_Vertical) % 2 == 1:
                    txt = Styles.SANS_B3.render(str(i + 1), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(25, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(id), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(125, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics['_NAMES'][id]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(275, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][0]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(475, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][1]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(725, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][2]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(975, y, txt.get_size()))
                else:
                    txt = Styles.SANS_B3.render(str(i + 1), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(25, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(id), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(125, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics['_NAMES'][id]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(275, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][0]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(475, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][1]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(725, y, txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[id][self.Index_Horizonal][2]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(975, y, txt.get_size()))

            self.PreviewScreen.fill(Styles.SPRLIGHTGRAY, [1101, 443, 248, 50])
            txt = Styles.SANS_B4.render(f'← 왼쪽으로 {self.Index_Horizonal}개 더 있음', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.PreviewScreen.blit(txt, center_top(1225, 443, txt.get_size()))
            txt = Styles.SANS_B4.render(f'오른쪽으로 {self.Total_Horizonal - self.Index_Horizonal - 1}개 더 있음 →', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.PreviewScreen.blit(txt, center_bottom(1225, 493, txt.get_size()))

            if self.ShiftDown:
                txt = Styles.SANS_H4.render('가로 방향으로 훑어보는 중', 1, Styles.GREEN, Styles.SPRLIGHTGRAY)
            else:
                txt = Styles.SANS_H4.render('세로 방향으로 훑어보는 중', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)

            self.PreviewScreen.blit(txt, right_top(1350, 835, txt.get_size()))
            self.ShiftDown_Display = self.ShiftDown

            txt = Styles.SANS_B3.render('[SHIFT] 키를 누르며 마우스 휠을 돌리면 가로 방향으로 훑어볼 수 있습니다.', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            self.PreviewScreen.blit(txt, right_top(1350, 871, txt.get_size()))

            self._Scrollbars()

        self.Updated = True


    # ChatGPT가 써준 코드
    def _Scrollbars(self):
        """ 가로, 세로 스크롤바 렌더링 """

        # === 세로 스크롤바 ===
        list_height = 50 * 14  # 한 페이지에 최대 14개

        if self.Total_Vertical <= 14:
            # 데이터가 한 페이지면 스크롤바 필요 없음
            return

        # 바의 높이: 현재 표시 비율에 맞게
        bar_height = max(int((14 / self.Total_Vertical) * list_height), 20)
        max_scroll_index = self.Total_Vertical - 14
        scroll_ratio = self.Index_Vertical / max_scroll_index if max_scroll_index > 0 else 0

        # 바 배경 (연한 회색)
        draw.rect(self.PreviewScreen, Styles.LIGHTGRAY, (1355, 118, 10, list_height), border_radius=5)
        # 바 (짙은 회색)
        draw.rect(self.PreviewScreen, Styles.DARKGRAY, (1355, int(scroll_ratio * (list_height - bar_height)) + 118, 10, bar_height), border_radius=5)

        # === 가로 스크롤바 ===

        draw.rect(self.PreviewScreen, Styles.LIGHTGRAY, (0, 823, 1350, 10), border_radius=5)

        if self.Total_Horizonal > 1:
            scroll_ratio = 1 / self.Total_Horizonal
            scroll_width = 1350 * scroll_ratio
            scroll_pos = (1350 - scroll_width) * (self.Index_Horizonal / (self.Total_Horizonal - 1))
            draw.rect(self.PreviewScreen, Styles.DARKGRAY, (scroll_pos, 823, scroll_width, 10), border_radius=5)


    def _Statistics(self, yr: int, mn: int):
        """
        통계 정보 갱신
        - - -
        #### 매개변수:
        - **yr:** 연도
        - **mn:** 월
        """

        self.CurrentStatistics = MonthlyStatistics(yr, mn)
        if self.CurrentStatistics.Empty:
            return

        self.IDs = []
        for id in self.CurrentStatistics.Statistics.keys():
            if id not in ('_DATA_DATES', '_NAMES'):
                self.IDs.append(id)

        self.Index_Vertical  = 0
        self.Index_Horizonal = 0

        self.Total_Vertical  = len(self.IDs)
        self.Total_Horizonal = len(self.CurrentStatistics.Statistics['_DATA_DATES'])



    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        Interface.SC_QuitButton.Reset()

        Interface.SC_ExportButton.Reset(130, 780)
        Interface.SC_MonthSelection.Reset()

        self._Statistics(ChairyData.ROOMDATA.DATA_DATE.year, ChairyData.ROOMDATA.DATA_DATE.month)
        
        self.CurrentDate = (ChairyData.ROOMDATA.DATA_DATE.year, ChairyData.ROOMDATA.DATA_DATE.month)

        self.ShiftDown = False
        
        self._Preview()
        DISPLAY.blit(self.PreviewScreen, (492, 86))

        DISPLAY.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))

    
    def On_Update(self, ANIMATION_OFFSET, TICK):
        ...
    

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        
        if Interface.SC_TopBar.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SC_TopBar.Frame(DISPLAY))

        if Interface.SC_QuitButton.Update():
            RECTS.append(Interface.SC_QuitButton.Frame(DISPLAY))

        if Interface.SC_ExportButton.Update():
            RECTS.append(Interface.SC_ExportButton.Frame(DISPLAY))

        if Interface.SC_MonthSelection.Update():
            RECTS.appendRect(DISPLAY.blit(self.DateSelection, (80, 326)))
            Interface.SC_MonthSelection.Frame(DISPLAY)

        if self.Updated:
            self.Updated = False
            RECTS.appendRect(DISPLAY.blit(self.PreviewScreen, (492, 86)))


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))

        Interface.SC_TopBar.Frame(SURFACE)
        Interface.SC_QuitButton.Frame(SURFACE)
        Interface.SC_ExportButton.Frame(SURFACE)
        SURFACE.blit(self.DateSelection, (80, 326))
        Interface.SC_MonthSelection.Frame(SURFACE)

        self._Preview()
        SURFACE.blit(self.PreviewScreen, (492, 86))



    def Event_MouseButtonDown(self, POS, BUTTON):

        Interface.SC_QuitButton.MouseButtonDown(POS, BUTTON)
        Interface.SC_ExportButton.MouseButtonDown(POS, BUTTON)
        
        date = Interface.SC_MonthSelection.MouseButtonDown(POS, BUTTON)
        if date is not None:
            self.CurrentDate = date
            self._Statistics(date[0], date[1])
            self._Preview()

        if BUTTON == 4 and POS[0] > 490:
            if self.ShiftDown:
                if self.Index_Horizonal > 0:
                    self.Index_Horizonal -= 1
            else:
                if self.Index_Vertical > 0:
                    self.Index_Vertical -= 1
            self._Preview()

        elif BUTTON == 5 and POS[0] > 490:
            if self.ShiftDown:
                if self.Index_Horizonal + 1 < self.Total_Horizonal:
                    self.Index_Horizonal += 1
            else:
                if self.Index_Vertical + 14 < self.Total_Vertical:
                    self.Index_Vertical += 1

            self._Preview()


    def Event_MouseMotion(self, POS):
        
        Interface.SC_QuitButton.MouseMotion(POS)
        Interface.SC_ExportButton.MouseMotion(POS)
        Interface.SC_MonthSelection.MouseMotion(POS)

    
    def Event_MouseButtonUp(self, POS, BUTTON):

        if BUTTON != 1:
            return

        if Interface.SC_QuitButton.MouseButtonUp(POS, BUTTON):
            from .transition import Transition
            Transition(SceneManager.Scenes['MainScene'])
        
        if Interface.SC_ExportButton.MouseButtonUp(POS, BUTTON):
            StatisticDialog(self.CurrentStatistics)
        
        if Interface.SC_MonthSelection.MouseButtonUp(POS, BUTTON):
            self.CurrentDate = (ChairyData.ROOMDATA.DATA_DATE.year, ChairyData.ROOMDATA.DATA_DATE.month)
            self._Statistics(self.CurrentDate[0], self.CurrentDate[1])
            self._Preview()
        
        if collidepoint(667, 15, 131, 40, POS):
            Interface.SC_TopBar.attendance()
            SceneManager.setScene('ExportDaily')
        #elif collidepoint(822, 15, 131, 40, POS):
        #    Interface.SC_TopBar.monthly()
        elif collidepoint(967, 15, 131, 40, POS):
            Interface.SC_TopBar.period()
            SceneManager.setScene('ExportPeriod')
        elif collidepoint(1112, 15, 131, 40, POS):
            Interface.SC_TopBar.arrangement()
            SceneManager.setScene('ExportSeats')


    def Event_KeyDown(self, KEY):
        
        if KEY == constants.K_F9:
            from .transition import Transition
            Transition(SceneManager.Scenes['MainScene'])

        elif KEY in (constants.K_LSHIFT, constants.K_RSHIFT):
            if not self.ShiftDown:
                self.ShiftDown = True
                self._Preview()

    
    def Event_KeyUp(self, KEY):
        
        if KEY in (constants.K_LSHIFT, constants.K_RSHIFT) and self.ShiftDown:
            self.ShiftDown = False
            self._Preview()


    def On_Layer(self, ANIMATION_OFFSET, TICK, LAYER, RECTS):
        if Interface.LY_Notice.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.LY_Notice.Frame(LAYER))