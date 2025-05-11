from ..interface import Scene, Styles, Interface, SceneManager
from ..chairyData import DailyStatistics, ChairyData
from pygame import Surface, constants, draw
from .dialog import Dialog

from ..optimization.positioning import collidepoint, center_top



class StatisticDialog(Dialog):

    Statistic: DailyStatistics

    def __init__(self, s: DailyStatistics):
        self.Statistic = s
        super().__init__("통계를 내보내는 중...", "「일간 출석부」 통계를 내보내고 있습니다.")


    def run(self):
        from time import sleep

        self.set("통계 내보내기 완료!", self.Statistic.Write() + '\n로 저장되었습니다.')
        sleep(2)




class ExportDaily(Scene):
    """ ### 일간 출석부 내보내기 """


    @staticmethod
    def Init():
        SceneManager.ExportDaily = ExportDaily()


    Preview: Surface # 에셋
    PreviewScreen: Surface # 미리보기 Surface
    DateSelection: Surface # 에셋

    CurrentStatistics: DailyStatistics # 현재 통계 데이터
    # Statistics: [<StudentID>, <Name>, <LastChkIn>, <LastChkOut>, <LastSeat>, <MoveCount>]

    Index: int # 인덱스
    Total: int # 길이

    Updated: bool # 내부 Surface가 갱신되었는지 여부



    def __init__(self):
        self.Preview = SceneManager.loadAsset('/ChairyApp/assets/statistics/PreviewDaily.png').convert()
        self.DateSelection = SceneManager.loadAsset('/ChairyApp/assets/statistics/DateSelection.png').convert()
        self.Index = 0
        self.Updated = False


    def _Preview(self):
        """ 미리보기 렌더링 """
        self.PreviewScreen = Surface((1365, 889))
        self.PreviewScreen.fill(Styles.SPRLIGHTGRAY, [1350, 0, 15, 889])
        self.PreviewScreen.blit(self.Preview, (0,0))

        if self.CurrentStatistics.Empty:
            self.PreviewScreen.blit(Styles.SANS_B3.render('(데이터 없음)', 1, Styles.BLACK, Styles.LIGHTGRAY), (675, 82))

        else:
            # Statistics: [<StudentID>, <Name>, <LastChkIn>, <LastChkOut>, <LastSeat>, <MoveCount>]
            for i in range(self.Index, min(self.Total, self.Index + 15)):
                if (i - self.Index) % 2 == 0:
                    txt = Styles.SANS_B3.render(str(i + 1), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(25, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][0]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(125, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][1]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(275, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][2]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(475, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][3]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(725, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][4]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(975, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][5]), 1, Styles.BLACK, Styles.LIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(1225, 82 + (50 * (i - self.Index)), txt.get_size()))
                else:
                    txt = Styles.SANS_B3.render(str(i + 1), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(25, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][0]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(125, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][1]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(275, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][2]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(475, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][3]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(725, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][4]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(975, 82 + (50 * (i - self.Index)), txt.get_size()))
                    txt = Styles.SANS_B3.render(str(self.CurrentStatistics.Statistics[i][5]), 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
                    self.PreviewScreen.blit(txt, center_top(1225, 82 + (50 * (i - self.Index)), txt.get_size()))

            self._Scrollbar()

        self.Updated = True


    # ChatGPT가 써준 코드
    def _Scrollbar(self):
        """ 스크롤바 렌더링링 """
        list_height = 50 * 15  # 한 페이지에 최대 15개

        if self.Total <= 15:
            # 데이터가 한 페이지면 스크롤바 필요 없음
            return

        # 바의 높이: 현재 표시 비율에 맞게
        bar_height = max(int((15 / self.Total) * list_height), 20)
        max_scroll_index = self.Total - 15
        scroll_ratio = self.Index / max_scroll_index if max_scroll_index > 0 else 0

        # 바 배경 (연한 회색)
        draw.rect(self.PreviewScreen, Styles.LIGHTGRAY, (1355, 68, 10, list_height), border_radius=5)
        # 바 (짙은 회색)
        draw.rect(self.PreviewScreen, Styles.DARKGRAY, (1355, int(scroll_ratio * (list_height - bar_height)) + 68, 10, bar_height), border_radius=5)



    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        Interface.SC_QuitButton.Reset(130, 940)
        Interface.SC_ExportButton.Reset(130, 780)
        Interface.SC_DateSelection.Reset()

        ChairyData.ROOMDATA.Save()
        self.CurrentStatistics = DailyStatistics(ChairyData.ROOMDATA.DATA_DATE)
        self.Index = 0
        self.Total = len(self.CurrentStatistics.Statistics)

        DISPLAY.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))
        
        self._Preview()
        self.Updated = True

    
    def On_Update(self, ANIMATION_OFFSET, TICK):
        ...
    

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        
        if Interface.SC_TopBar.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SC_TopBar.Frame(DISPLAY))

        if Interface.SC_QuitButton.Update():
            RECTS.append(Interface.SC_QuitButton.Frame(DISPLAY))

        if Interface.SC_ExportButton.Update():
            RECTS.append(Interface.SC_ExportButton.Frame(DISPLAY))

        if Interface.SC_DateSelection.Update():
            RECTS.append(DISPLAY.blit(self.DateSelection, (80, 326)))
            Interface.SC_DateSelection.Frame(DISPLAY)

        if self.Updated:
            self.Updated = False
            RECTS.append(DISPLAY.blit(self.PreviewScreen, (492, 86)))


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))

        Interface.SC_TopBar.Frame(SURFACE)
        Interface.SC_QuitButton.Frame(SURFACE)
        Interface.SC_ExportButton.Frame(SURFACE)
        SURFACE.blit(self.DateSelection, (80, 326))
        Interface.SC_DateSelection.Frame(SURFACE)

        self._Preview()
        SURFACE.blit(self.PreviewScreen, (492, 86))



    def Event_MouseButtonDown(self, POS, BUTTON):

        Interface.SC_QuitButton.MouseButtonDown(POS, BUTTON)
        Interface.SC_ExportButton.MouseButtonDown(POS, BUTTON)
        Interface.SC_DateSelection.MouseButtonDown(POS, BUTTON)

        if BUTTON == 4 and POS[0] > 490:
            if self.Index > 0:
                self.Index -= 1
            else:
                self.Index = 0
            self._Preview()

        elif BUTTON == 5 and POS[0] > 490:
            if self.Index + 15 < self.Total:
                self.Index += 1
                self._Preview()


    def Event_MouseMotion(self, POS):
        
        Interface.SC_QuitButton.MouseMotion(POS)
        Interface.SC_ExportButton.MouseMotion(POS)
        Interface.SC_DateSelection.MouseMotion(POS)

    
    def Event_MouseButtonUp(self, POS, BUTTON):

        if BUTTON != 1:
            return

        if Interface.SC_QuitButton.MouseButtonUp(POS, BUTTON):
            from .transition import Transition
            Transition(SceneManager.MainScene)
        
        if Interface.SC_ExportButton.MouseButtonUp(POS, BUTTON):
            StatisticDialog(self.CurrentStatistics)
        
        date = Interface.SC_DateSelection.MouseButtonUp(POS, BUTTON)
        if date != None:
            self.CurrentStatistics = DailyStatistics(date)
            Interface.SC_DateSelection._Render()
            self.Index = 0
            self.Total = len(self.CurrentStatistics.Statistics) if not self.CurrentStatistics.Empty else 0
            self._Preview()
            self.Updated = True
        
        #if oRect(0, 0, 667, 15, 131, 40).collidepoint(POS):
        #    Interface.SC_TopBar.attendance()
        if collidepoint(822, 15, 131, 40, POS):
            Interface.SC_TopBar.monthly()
            SceneManager.setScene(SceneManager.ExportMonthly)
        elif collidepoint(967, 15, 131, 40, POS):
            Interface.SC_TopBar.period()
            SceneManager.setScene(SceneManager.ExportPeriod)
        elif collidepoint(1112, 15, 131, 40, POS):
            Interface.SC_TopBar.arrangement()
            SceneManager.setScene(SceneManager.ExportSeats)


    def Event_KeyDown(self, KEY):
        
        if KEY == constants.K_F9:
            from .transition import Transition
            Transition(SceneManager.MainScene)