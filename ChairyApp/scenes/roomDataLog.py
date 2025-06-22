
from ..interface    import Scene, Styles, SceneManager, Interface
from ..chairyData   import ChairyData, RoomData
from pygame         import Surface, draw, K_ESCAPE
from datetime       import datetime, date
from array import array

from ..optimization.positioning import center_center, center_top



class RoomdataLog(Scene):

    Data: RoomData
    Date: date

    DateSelection: Surface
    Frame: Surface

    Icons: tuple[Surface]

    Updated: bool

    Index: int

    Total: int
    TotalCheckIn: int
    TotalCheckOut: int
    TotalMove: int
    TotalPassword: int

    
    def __init__(self):
        self.Identifier = 'RoomdataLog'

        self.DateSelection = SceneManager.loadAsset('/ChairyApp/assets/statistics/DateSelection.png').convert()
        self.Frame = SceneManager.loadAsset('/ChairyApp/assets/components/RoomDataLog.png').convert()
        self.Icons = (
            SceneManager.loadAsset('/ChairyApp/assets/components/ChkInIcon.png').convert(),
            SceneManager.loadAsset('/ChairyApp/assets/components/ChkOutIcon.png').convert(),
            SceneManager.loadAsset('/ChairyApp/assets/components/MoveIcon.png').convert(),
            SceneManager.loadAsset('/ChairyApp/assets/components/PasswordIcon.png').convert()
        )
        self.Updated = False

    
    def On_Init(self, DISPLAY):
        Interface.SC_QuitButton.Reset()
        Interface.SC_DateSelection.Reset(92, 450)

        self._Init()

        self.Draw(DISPLAY)


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)

        SURFACE.blit(self.DateSelection, (64, 415))
        Interface.SC_QuitButton.Frame(SURFACE)
        Interface.SC_DateSelection.Frame(SURFACE)
        
        SURFACE.blit(Styles.SANS_B5.render("또는 [ESC]를 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1724, 60))

        self._RenderTitle(SURFACE)
        self._RenderPreview(SURFACE)


    def _Init(self, Date: date = None):

        if Date is None:
            self.Data = ChairyData.ROOMDATA
            self.Date = ChairyData.ROOMDATA.DATA_DATE
        else:
            self.Data = RoomData.Load(Date)
            self.Date = Date

        self.Index = 0

        self.TotalCheckIn = 0
        self.TotalCheckOut = 0
        self.TotalMove = 0
        self.TotalPassword = 0

        if self.Data is not None:
            self.Total = len(self.Data.Logs)

            for log in self.Data.Logs:

                if log['Action'] == 'ChkIn':
                    self.TotalCheckIn += 1
                elif log['Action'] == 'ChkOut':
                    self.TotalCheckOut += 1
                elif log['Action'] == 'Move':
                    self.TotalMove += 1
                elif log['Action'] == 'Password':
                    self.TotalPassword += 1

        else:
            self.Total = 0


    def _RenderTitle(self, DISP: Surface):
        DISP.fill(Styles.SPRLIGHTGRAY, (64, 116, 350, 256))

        DISP.blit(Styles.SANS_H2.render('전체 기록', 1, Styles.BLACK, Styles.SPRLIGHTGRAY), (64, 116))
        DISP.blit(Styles.ANTON_H4.render(self.Date.strftime('%Y%m%d.json'), 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (64, 181))

        DISP.blit(Styles.SANS_B3.render(f'● 전체 기록 수: {self.Total}', 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (64, 238))
        DISP.blit(Styles.SANS_B3.render(f'● 입실 기록 수: {self.TotalCheckIn}', 1, Styles.BLUE, Styles.SPRLIGHTGRAY), (64, 267))
        DISP.blit(Styles.SANS_B3.render(f'● 퇴실 기록 수: {self.TotalCheckOut}', 1, Styles.RED, Styles.SPRLIGHTGRAY), (64, 296))
        DISP.blit(Styles.SANS_B3.render(f'● 이동 기록 수: {self.TotalMove}', 1, Styles.ORANGE, Styles.SPRLIGHTGRAY), (64, 325))
        DISP.blit(Styles.SANS_B3.render(f'● 비밀번호 변경 수: {self.TotalPassword}', 1, Styles.YELLOW, Styles.SPRLIGHTGRAY), (64, 354))


    def _RenderPreview(self, DISP: Surface):

        DISP.fill(Styles.SPRLIGHTGRAY, (462, 95, 1428, 961))

        if self.Total == 0:

            txt = Styles.SANS_H4.render("기록 없음", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1178, 508, txt.get_size()))
            txt = Styles.SANS_B4.render("해당 일자에는 아무 기록도 발생하지 않았습니다.", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1178, 559, txt.get_size()))
            return

        if self.Data is not None:
        
            log: dict

            txt = Styles.SANS_B3.render('행동', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(559, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('시간', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(807, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('학번', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1052, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('이름', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1209, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('이전 자리', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1377, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('선택한 자리', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1534, 100, txt.get_size()))
            txt = Styles.SANS_B3.render('비고', 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1731, 100, txt.get_size()))


            for index in range(self.Index, min(self.Total, self.Index + 11)):
                log = self.Data.Logs[index]

                index -= self.Index

                DISP.blit(self.Frame, (462, 131 + 85 * index))

                if log['Action'] == 'ChkIn':
                    DISP.blit(self.Icons[0], center_center(505, 170 + 85 * index, self.Icons[0].get_size()))
                    DISP.blit(Styles.SANS_H4.render('입실', 1, Styles.BLUE, Styles.WHITE), (541, 155 + 85 * index))
                elif log['Action'] == 'ChkOut':
                    DISP.blit(self.Icons[1], center_center(505, 170 + 85 * index, self.Icons[1].get_size()))
                    DISP.blit(Styles.SANS_H4.render('퇴실', 1, Styles.RED, Styles.WHITE), (541, 155 + 85 * index))
                elif log['Action'] == 'Move':
                    DISP.blit(self.Icons[2], center_center(505, 170 + 85 * index, self.Icons[2].get_size()))
                    DISP.blit(Styles.SANS_H4.render('이동', 1, Styles.ORANGE, Styles.WHITE), (541, 155 + 85 * index))
                elif log['Action'] == 'Password':
                    DISP.blit(self.Icons[3], center_center(505, 170 + 85 * index, self.Icons[3].get_size()))
                    DISP.blit(Styles.SANS_H4.render('암호', 1, Styles.YELLOW, Styles.WHITE), (541, 155 + 85 * index))

                if 'TimeStamp' in log:
                    txt = Styles.ANTON_H4.render(datetime.strptime(log['TimeStamp'], '%Y%m%d%H%M%S.%f').strftime('%Y-%m-%d | %H:%M:%S.%f'), 1, Styles.DARKGRAY, Styles.WHITE)
                    DISP.blit(txt, center_center(807, 169 + 85 * index, txt.get_size()))

                if 'ID' in log:
                    txt = Styles.ANTON_H2.render(log['ID'], 1, Styles.BLUE, Styles.WHITE)
                    DISP.blit(txt, center_center(1052, 169 + 85 * index, txt.get_size()))

                if 'Name' in log:
                    txt = Styles.SANS_H4.render(log['Name'], 1, Styles.GREEN, Styles.WHITE)
                    DISP.blit(txt, center_center(1209, 169 + 85 * index, txt.get_size()))

                if 'From' in log:
                    txt = Styles.SANS_H4.render(log['From'], 1, Styles.PURPLE, Styles.WHITE)
                    DISP.blit(txt, center_center(1377, 169 + 85 * index, txt.get_size()))

                if 'Seat' in log:
                    txt = Styles.SANS_H4.render(log['Seat'], 1, Styles.PURPLE, Styles.WHITE)
                    DISP.blit(txt, center_center(1534, 169 + 85 * index, txt.get_size()))

                if 'Comment' in log:
                    txt = Styles.SANS_H4.render(log['Comment'], 1, Styles.PURPLE, Styles.WHITE)
                    DISP.blit(txt, center_center(1731, 169 + 85 * index, txt.get_size()))

            ## 스크롤바 ##
            list_height = 925  # 한 페이지에 최대 15개

            if self.Total <= 11:
                # 데이터가 한 페이지면 스크롤바 필요 없음
                return

            # 바의 높이: 현재 표시 비율에 맞게
            bar_height = max(int((11 / self.Total) * list_height), 20)
            max_scroll_index = self.Total - 11
            scroll_ratio = self.Index / max_scroll_index if max_scroll_index > 0 else 0

            # 바 배경 (연한 회색)
            draw.rect(DISP, Styles.LIGHTGRAY, (1880, 131, 10, list_height), border_radius=5)
            # 바 (짙은 회색)
            draw.rect(DISP, Styles.DARKGRAY, (1880, int(scroll_ratio * (list_height - bar_height)) + 131, 10, bar_height), border_radius=5)

        else: 

            txt = Styles.SANS_H4.render("해당 데이터를 찾을 수 없습니다.", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1178, 508, txt.get_size()))
            txt = Styles.SANS_B4.render("다른 날짜로 다시 시도해주십시오.", 1, Styles.BLACK, Styles.SPRLIGHTGRAY)
            DISP.blit(txt, center_top(1178, 559, txt.get_size()))


    def Event_KeyDown(self, KEY):
        if KEY == K_ESCAPE:
            SceneManager.setScene('MainScene')


    def Event_MouseMotion(self, POS):
        Interface.SC_DateSelection.MouseMotion(POS)
        Interface.SC_QuitButton.MouseMotion(POS)


    def Event_MouseButtonDown(self, POS, BUTTON):
        Interface.SC_DateSelection.MouseButtonDown(POS, BUTTON)
        Interface.SC_QuitButton.MouseButtonDown(POS, BUTTON)

        if BUTTON == 4 and POS[0] > 450:
            if self.Index > 0:
                self.Index -= 1
            else:
                self.Index = 0
            self.Updated = True

        elif BUTTON == 5 and POS[0] > 450:
            if self.Index + 11 < self.Total:
                self.Index += 1
                self.Updated = True


    def Event_MouseButtonUp(self, POS, BUTTON):
        Date = Interface.SC_DateSelection.MouseButtonUp(POS, BUTTON)

        if Date is not None:
            Interface.SC_DateSelection._Render()
            self._Init(Date)
            self.Updated = True

        if Interface.SC_QuitButton.MouseButtonUp(POS, BUTTON):
            SceneManager.setScene('MainScene')


    def On_Update(self, ANIMATION_OFFSET, TICK):
        return self.Updated
    

    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):

        if Interface.SC_QuitButton.Update():
           RECTS.append(Interface.SC_QuitButton.Frame(DISPLAY))

        if Interface.SC_DateSelection.Update():
           RECTS.append(Interface.SC_DateSelection.Frame(DISPLAY))

        if self.Updated:
            self.Updated = False

            self._RenderTitle(DISPLAY)
            RECTS.append(array('i', (64, 116, 350, 256)))

            self._RenderPreview(DISPLAY)
            RECTS.append(array('i', (462, 95, 1428, 961)))


    def On_Layer(self, ANIMATION_OFFSET, TICK, LAYER, RECTS):
        if Interface.LY_Notice.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.LY_Notice.Frame(LAYER))