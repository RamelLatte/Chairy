from ..interface import Scene, Styles, Interface, SceneManager
from ..chairyData import RoomData, ChairyData
from pygame import Surface, Rect, constants
from datetime import datetime, date, time, timedelta
from .dialog import Dialog
from ..Info import ChairyInfo

from ..Logging import LoggingManager as logging
from ..optimization.positioning import center_top, collidepoint
import openpyxl as xl



class StatisticDialog(Dialog):

    Seats: dict
    Datetime: datetime
    TotalSeats: int
    Occupied: int
    Vacant  : int

    def __init__(self, seats: dict, datetime: datetime, totalSeats: int, occupied: int, vacant: int):
        self.Seats = seats
        self.Datetime = datetime
        self.TotalSeats = totalSeats
        self.Occupied = occupied
        self.Vacant = vacant
        super().__init__("좌석표를 내보내는 중...", "좌석표를 내보내고 있습니다.")


    def run(self):

        logging.info(self.Datetime.strftime('좌석표 작성 시작: %Y.%m.%d. %H:%M:%S'))

        from time import sleep
        wb: xl.Workbook = xl.load_workbook(RoomData.DIRECTORY + "/school_data/arrangement.xlsx")

        ws = wb.active

        # 셀에 기입
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is None:
                    continue

                if '{' in str(cell.value).strip() and '}' in str(cell.value).strip():
                    code = str(cell.value).strip().split('{')[1].split('}')[0]
                    if code == 'datetime':
                        cell.value = self.Datetime.strftime('%Y.%m.%d %H:%M:%S')
                    elif code == 'total':
                        cell.value = self.TotalSeats
                    elif code == 'occupied':
                        cell.value = self.Occupied
                    elif code == 'vacant':
                        cell.value = self.Vacant
                    elif code == 'version':
                        cell.value = ChairyInfo.Version
                    elif code in self.Seats:
                        cell.value = self.Seats[code][1]
                    else:
                        cell.value = ''
                        

        import os
        if not os.path.exists(RoomData.DIRECTORY + '/Statistics/'):
            os.makedirs(RoomData.DIRECTORY + '/Statistics/')

        finalFile = self.Datetime.strftime('좌석표-%Y%m%d.%H%M%S-') + datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
        wb.save(RoomData.DIRECTORY + '/Statistics/' + finalFile)

        self.set("좌석표 내보내기 완료!", finalFile + '\n로 저장되었습니다.')
        logging.info(f'좌석표 작성 완료: {finalFile}')
        sleep(2)




class ExportSeats(Scene):
    """ ### 시간별 좌석 내보내기 """

    @staticmethod
    def Init():
        SceneManager.ExportSeats = ExportSeats()


    Structure: Surface  # 에셋
    AssetIcons: Surface # 에셋

    AssetSeatsTime: Surface     # 에셋
    AssetSeatsData: Surface     # 에셋
    AssetStudentInfo0: Surface  # 에셋
    AssetStudentInfo1: Surface  # 에셋

    Seats_R : list[Rect]    # Rects  : 좌석 아이콘의 위치
    Seats_P : list[Surface] # Preview: 미리보기 렌더링용 좌석 아이콘 임시 저장
    Seats_I : list[str]     # Index  : ID를 대입해서 위 2개 리스트의 Index 획득

    Total   : int   # 전체 좌석 수
    Occupied: int   # 점유 좌석 수
    Vacant  : int   # 여유 좌석 수

    DateSelection: Surface # 에셋

    CurrentRoomdata: RoomData # 현재 RoomData

    FirstLog: datetime # 첫 기록 발생 시점
    LastLog : datetime # 마지막 기록 발생 시점

    SelectedDate : date     # 선택한 날짜
    CurrentTime: datetime   # 조회중인 시점

    KeyDownShift: bool # Shift 누름 여부
    KeyDownCtrl: bool  # Ctrl 누름 여부
    KeyDownAlt: bool   # Alt 누름 여부

    Seats: dict # 특정 시점에서의 좌석 현황

    Updated: bool # 내부 미리보기 갱신 여부



    def __init__(self):
        self.Structure = SceneManager.loadAsset('/school_data/structure.png').convert()
        self.AssetIcons = [
            SceneManager.loadAsset('/ChairyApp/assets/seatIcons/VacantSeat0.png').convert(),
            SceneManager.loadAsset('/ChairyApp/assets/seatIcons/OccupiedSeat0.png').convert()
        ]
        self.DateSelection = SceneManager.loadAsset('/ChairyApp/assets/statistics/DateSelection.png').convert()
        self.AssetSeatsTime = SceneManager.loadAsset('/ChairyApp/assets/statistics/SeatsTime.png').convert()
        self.AssetSeatsData = SceneManager.loadAsset('/ChairyApp/assets/statistics/SeatsData.png').convert()
        self.AssetStudentInfo0 = SceneManager.loadAsset('/ChairyApp/assets/statistics/SeatsStudentInfo0.png').convert()
        self.AssetStudentInfo1 = SceneManager.loadAsset('/ChairyApp/assets/statistics/SeatsStudentInfo1.png').convert()

        self.Seats_P = []
        self.Seats_R = []
        self.Seats_I = []

        self.Total = 0
        self.Vacant = 0
        self.Occupied = 0

        self.KeyDownShift = False
        self.KeyDownCtrl = False
        self.KeyDownAlt = False

        self.Updated = False

    
    def _Roomdata(self, date: date = None):
        """
        날짜 지정 및 RoomData 불러오기
        - - -
        #### 매개변수:
        - **date:** 불러올 RoomData 날짜, 기본값은 None이며 이 경우 오늘 날짜가 지정됨.
        """

        if date is None:
            self.SelectedDate = ChairyData.ROOMDATA.DATA_DATE
            self.CurrentRoomdata = ChairyData.ROOMDATA

        else:
            self.SelectedDate = date
            self.CurrentRoomdata = RoomData.Load(date)
        
        self.FirstLog   = None
        self.LastLog    = None

        for log in self.CurrentRoomdata.Logs:
            dt = datetime.strptime(log['TimeStamp'], '%Y%m%d%H%M%S.%f')
            if self.FirstLog is None or self.FirstLog > dt:
                self.FirstLog = dt
            if self.LastLog is None or self.LastLog < dt:
                self.LastLog = dt

        if self.FirstLog is None:
            self.CurrentTime = datetime.combine(ChairyData.ROOMDATA.DATA_DATE, time(16, 30, 0))
        else:
            self.CurrentTime = self.FirstLog

                
        self.Seats = {}

        self.Total = len(self.CurrentRoomdata.Arrangement)

        self._Walk()


    def _Walk(self):
        """ 지정된 시간까지 좌석 데이터 훑기 """

        if len(self.CurrentRoomdata.Logs) <= 0:
            return
        
        self.Seats.clear()

        self.Vacant = self.Total
        self.Occupied = 0

        for index, log in enumerate(self.CurrentRoomdata.Logs):
            ts = datetime.strptime(log['TimeStamp'], '%Y%m%d%H%M%S.%f')
            # 이미 조회할 시간까지 데이터를 훑었으면 인덱스 저장하고 루프 빠져나감
            if ts > self.CurrentTime:
                break

            action = log['Action']
            seat = log['Seat']
            id_ = log['ID']
            name = log['Name']

            if action == 'ChkIn':
                self.Seats[seat] = [id_, name]
                self.Vacant -= 1
                self.Occupied += 1

            elif action == 'ChkOut':
                self.Seats.pop(seat, None)
                self.Vacant += 1
                self.Occupied -= 1

            elif action == 'Move':
                self.Seats.pop(log['From'], None)
                self.Seats[seat] = [id_, name]


    def _Preview(self):
        """ 내부 아이콘 렌더링 """

        self.Seats_P.clear()
        self.Seats_R.clear()
        self.Seats_I.clear()

        # 좌석 배치 구현
        for seat in self.CurrentRoomdata.Arrangement:
            self.Seats_I.append(seat[0])
            self.Seats_R.append(Rect(seat[1] + 660, seat[2] + 42, 50, 50))
            surface = Surface((50, 50))

            surface.blit(self.AssetIcons[0], (0, 0))
            txt = Styles.SANS_H5.render(seat[0], 1, Styles.BLUE)
            surface.blit(txt, center_top(25, 5, txt.get_size()))
            self.Seats_P.append(surface)

        # 좌석 배치 대입
        for seat, student in self.Seats.items():
            index = self.Seats_I.index(seat)

            self.Seats_P[index].blit(self.AssetIcons[1], (0, 0))
            txt = Styles.SANS_H5.render(seat, 1, Styles.RED)
            self.Seats_P[index].blit(txt, center_top(25, 5, txt.get_size()))
            txt = Styles.SANS_H6.render(student[1], 1, Styles.WHITE)
            self.Seats_P[index].blit(txt, center_top(25, 30, txt.get_size()))

        self.Updated = True


    def _DrawPreview(self, DISPLAY: Surface, RECTS: list[Rect] = None):
        """ 내부 미리보기 Surface 렌더링 """

        self._Preview()

        DISPLAY.blit(self.AssetSeatsTime, (435, 326))
        txt = Styles.SANS_H3.render(self.CurrentTime.strftime('%H:%M:%S'), 1, Styles.BLACK, Styles.WHITE)
        DISPLAY.blit(txt, center_top(530, 381, txt.get_size()))

        DISPLAY.blit(self.AssetSeatsData, (435, 543))

        if self.FirstLog is None:
            txt = Styles.SANS_H3.render('기록 없음', 1, Styles.BLACK, Styles.WHITE)
            DISPLAY.blit(txt, center_top(530, 618, txt.get_size()))
        else:
            txt = Styles.SANS_H3.render(self.FirstLog.strftime('%H:%M:%S'), 1, Styles.BLACK, Styles.WHITE)
            DISPLAY.blit(txt, center_top(530, 618, txt.get_size()))

        if self.FirstLog is None:
            txt = Styles.SANS_H3.render('기록 없음', 1, Styles.BLACK, Styles.WHITE)
            DISPLAY.blit(txt, center_top(530, 688, txt.get_size()))
        else:
            txt = Styles.SANS_H3.render(self.LastLog.strftime('%H:%M:%S'), 1, Styles.BLACK, Styles.WHITE)
            DISPLAY.blit(txt, center_top(530, 688, txt.get_size()))

        DISPLAY.blit(self.Structure, (660, 42))

        # 화면에 렌더링
        for index, surface in enumerate(self.Seats_P):
            DISPLAY.blit(surface, self.Seats_R[index])

        # RECTS
        if RECTS is not None:
            RECTS.append(Rect(652, 33, 1001, 1047))
            RECTS.append(Rect(435, 328, 191, 418))
            #RECTS.append(Rect(1692, 310, 200, 460))



    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        Interface.SC_QuitButton.Reset(130, 940)
        Interface.SC_ExportButton.Reset(203, 818)
        Interface.SC_DateSelection.Reset(89, 361)

        ChairyData.ROOMDATA.Save()
        self._Roomdata()

        self.Seats_P.clear()
        self.Seats_R.clear()
        self.Seats_I.clear()

        self.Total = 0
        self.Vacant = 0
        self.Occupied = 0

        DISPLAY.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))
        
        self._Preview()
        self.Updated = True

    
    def On_Update(self, ANIMATION_OFFSET, TICK):
        ...


    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):

        if Interface.SC_QuitButton.Update():
            RECTS.append(Interface.SC_QuitButton.Frame(DISPLAY))

        if Interface.SC_ExportButton.Update():
            RECTS.append(Interface.SC_ExportButton.Frame(DISPLAY))

        if Interface.SC_DateSelection.Update():
            RECTS.append(DISPLAY.blit(self.DateSelection, (61, 326)))
            Interface.SC_DateSelection.Frame(DISPLAY)

        if self.Updated:
            self.Updated = False
            self._DrawPreview(DISPLAY, RECTS)
            RECTS.append(Rect(640, 0, 1280, 1080))

        if Interface.SC_TopBar.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SC_TopBar.Frame(DISPLAY))


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        SURFACE.blit(Styles.SANS_B5.render("또는 [F9]를 다시 누릅니다", 1, Styles.DARKGRAY, Styles.SPRLIGHTGRAY), (1718, 60))

        Interface.SC_QuitButton.Frame(SURFACE)
        Interface.SC_ExportButton.Frame(SURFACE)
        SURFACE.blit(self.DateSelection, (61, 326))
        Interface.SC_DateSelection.Frame(SURFACE)

        self._Preview()
        self._DrawPreview(SURFACE)

        Interface.SC_TopBar.Frame(SURFACE)



    def Event_MouseButtonDown(self, POS, BUTTON):

        Interface.SC_QuitButton.MouseButtonDown(POS, BUTTON)
        Interface.SC_ExportButton.MouseButtonDown(POS, BUTTON)
        Interface.SC_DateSelection.MouseButtonDown(POS, BUTTON)

        # 스크롤 올림
        if BUTTON == 4 and POS[0] > 430:

            if self.KeyDownShift:
                self.CurrentTime += timedelta(minutes=1)
            elif self.KeyDownCtrl:
                self.CurrentTime += timedelta(seconds=30)
            elif self.KeyDownAlt:
                self.CurrentTime += timedelta(seconds=1)
            else:
                self.CurrentTime += timedelta(minutes=10)

            if self.CurrentTime.day == self.SelectedDate.day + 1 and self.CurrentTime.hour >= 5:
                self.CurrentTime = datetime.combine(self.SelectedDate + timedelta(days=1), time(5, 0, 0))

            self._Walk()
            self._Preview()

        # 스크롤 내림
        elif BUTTON == 5 and POS[0] > 430:
            
            if self.KeyDownShift:
                self.CurrentTime -= timedelta(minutes=1)
            elif self.KeyDownCtrl:
                self.CurrentTime -= timedelta(seconds=30)
            elif self.KeyDownAlt:
                self.CurrentTime -= timedelta(seconds=1)
            else:
                self.CurrentTime -= timedelta(minutes=10)

            if self.CurrentTime.day == self.SelectedDate.day and self.CurrentTime.hour < 5:
                self.CurrentTime = datetime.combine(self.SelectedDate, time(5, 0, 0))

            self._Walk()
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
            StatisticDialog(self.Seats, self.CurrentTime, self.Total, self.Occupied, self.Vacant)
        
        date = Interface.SC_DateSelection.MouseButtonUp(POS, BUTTON)
        if date != None:
            self._Roomdata(date)
            Interface.SC_DateSelection._Render()
            self._Preview()
        
        if collidepoint(45, 15, 131, 40, POS):
            Interface.SC_TopBar.attendance()
            SceneManager.setScene(SceneManager.ExportDaily)
        if collidepoint(190, 15, 131, 40, POS):
            Interface.SC_TopBar.monthly()
            SceneManager.setScene(SceneManager.ExportMonthly)
        elif collidepoint(335, 15, 131, 40, POS):
            Interface.SC_TopBar.period()
            SceneManager.setScene(SceneManager.ExportPeriod)
        #elif collidepoint(1112, 15, 131, 40, POS):
        #    Interface.SC_TopBar.arrangement()


    def Event_KeyDown(self, KEY):
        
        if KEY == constants.K_F9:
            from .transition import Transition
            Transition(SceneManager.MainScene)
        elif KEY in (constants.K_LSHIFT, constants.K_RSHIFT):
            self.KeyDownShift = True
        elif KEY in (constants.K_LCTRL, constants.K_RCTRL):
            self.KeyDownCtrl = True
        elif KEY in (constants.K_LALT, constants.K_RALT):
            self.KeyDownAlt = True


    def Event_KeyUp(self, KEY):

        if KEY in (constants.K_LSHIFT, constants.K_RSHIFT):
            self.KeyDownShift = False
        elif KEY in (constants.K_LCTRL, constants.K_RCTRL):
            self.KeyDownCtrl = False
        elif KEY in (constants.K_LALT, constants.K_RALT):
            self.KeyDownAlt = False