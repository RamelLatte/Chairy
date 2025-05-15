
from pygame import Surface, Rect
from pygame.constants import RLEACCEL

from ChairyApp.chairyData import ChairyData
from .Component import Component
from .Styles import Styles
from .Scene import SceneManager as SM

from ..optimization.positioning import center_top



class SeatsDataVerifyError(Exception):

    SeatsId: str

    def __init__(self, id: str):
        self.SeatsId = id
        super().__init__("좌석 데이터가 잘못됨: [" + id + "]번 좌석을 찾을 수 없음.")



class SeatsDisplay(Component):
    """ ### 좌석표 """

    Asset_Structure         : Surface
    Asset_PreviewVacant     : Surface
    Asset_PreviewOccupied   : Surface
    Asset_Vacant0           : Surface
    Asset_Vacant1           : Surface
    Asset_VacantReserved0   : Surface
    Asset_VacantReserved1   : Surface
    Asset_Occupied0         : Surface
    Asset_Occupied1         : Surface
    Asset_CurrentSeat       : Surface

    ProcessedStructureImage : Surface

    CurrSurf    : Surface
    SeatIDs     : list[str]
    SeatNames   : list[str]
    SeatOccupied: list[bool]
    SeatReserved: list[bool]
    SeatSurf    : list[Surface]
    SeatSurf_   : list[Surface]
    SeatSurf_P  : list[Surface]
    SeatRect    : list[Rect]

    Alpha : float
    ShowSeats: bool

    SURFACE: Surface

    Updated: bool

    ClickedIndex: int

    MySeat  : str



    def __init__(self, x = 530, y = 35):
        super().__init__(x, y, 1002, 1045)
        
        self.SURFACE = Surface((1002, 1045))
        self.Asset_Structure        = SM.loadAsset("/school_data/structure.png").convert(self.SURFACE)
        self.Asset_PreviewVacant    = SM.loadAsset("/ChairyApp/assets/seatIcons/PreviewVacant.png").convert(self.SURFACE)
        self.Asset_PreviewOccupied  = SM.loadAsset("/ChairyApp/assets/seatIcons/PreviewOccupied.png").convert(self.SURFACE)
        self.Asset_Vacant0          = SM.loadAsset("/ChairyApp/assets/seatIcons/VacantSeat0.png").convert(self.SURFACE)
        self.Asset_Vacant1          = SM.loadAsset("/ChairyApp/assets/seatIcons/VacantSeat1.png").convert(self.SURFACE)
        self.Asset_VacantReserved0  = SM.loadAsset("/ChairyApp/assets/seatIcons/VacantReservedSeat0.png").convert(self.SURFACE)
        self.Asset_VacantReserved1  = SM.loadAsset("/ChairyApp/assets/seatIcons/VacantReservedSeat1.png").convert(self.SURFACE)
        self.Asset_Occupied0        = SM.loadAsset("/ChairyApp/assets/seatIcons/OccupiedSeat0.png").convert(self.SURFACE)
        self.Asset_Occupied1        = SM.loadAsset("/ChairyApp/assets/seatIcons/OccupiedSeat1.png").convert(self.SURFACE)
        self.Asset_CurrentSeat      = SM.loadAsset("/ChairyApp/assets/seatIcons/CurrentSeat.png").convert(self.SURFACE)

        self.Reset()


    def updateSeatSurf(self):
        """ 내부 Surface 및 아이콘을 갱신함. """

        for id, seat in ChairyData.ROOMDATA.Current.items():
            if id == None:
                continue

            if id not in self.SeatIDs:
                raise SeatsDataVerifyError(id)
            elif str(seat[2]).strip() not in ("", "None"):
                self.SeatNames[self.SeatIDs.index(id)] = seat[2]

        if self.MySeat != None and self.MySeat in self.SeatIDs:
            i = self.SeatIDs.index(self.MySeat)
            self.CurrSurf = self.Asset_CurrentSeat.copy()
            txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.GREEN)
            self.CurrSurf.blit(txt, center_top(25, 5, txt.get_size()))

        for i in range(len(self.SeatIDs)):

            if ChairyData.ROOMDATA.isReserved(self.SeatIDs[i]):

                self.SeatReserved[i] = True

                self.SeatSurf_P[i].blit(self.Asset_PreviewOccupied, (0, 0))
                txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.DARKGRAY)
                self.SeatSurf_P[i].blit(txt, center_top(25, 5, txt.get_size()))

                if ChairyData.ROOMDATA.isVacant(self.SeatIDs[i]):
                    self.SeatOccupied[i] = False

                    self.SeatSurf[i].blit(self.Asset_VacantReserved0, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.YELLOW)
                    self.SeatSurf[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_[i].blit(self.Asset_VacantReserved1, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.LIGHTYELLOW)
                    self.SeatSurf_[i].blit(txt, center_top(25, 5, txt.get_size()))

                else:
                    self.SeatOccupied[i] = True

                    self.SeatSurf[i].blit(self.Asset_Occupied0, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.RED)
                    self.SeatSurf[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_[i].blit(self.Asset_Occupied1, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.LIGHTRED)
                    self.SeatSurf_[i].blit(txt, center_top(25, 5, txt.get_size()))

                txt = Styles.SANS_H6.render(self.SeatNames[i], 1, Styles.WHITE)
                self.SeatSurf[i].blit(txt, center_top(25, 30, txt.get_size()))
                self.SeatSurf_[i].blit(txt, center_top(25, 30, txt.get_size()))
                self.SeatSurf_P[i].blit(txt, center_top(25, 30, txt.get_size()))

            else:

                self.SeatReserved[i] = False

                if ChairyData.ROOMDATA.isVacant(self.SeatIDs[i]):
                    self.SeatOccupied[i] = False

                    self.SeatSurf[i].blit(self.Asset_Vacant0, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.BLUE)
                    self.SeatSurf[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_[i].blit(self.Asset_Vacant1, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.LIGHTBLUE)
                    self.SeatSurf_[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_P[i].blit(self.Asset_PreviewVacant, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.DARKGRAY)
                    self.SeatSurf_P[i].blit(txt, center_top(25, 5, txt.get_size()))
                else:
                    self.SeatOccupied[i] = True

                    self.SeatSurf[i].blit(self.Asset_Occupied0, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.RED)
                    self.SeatSurf[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_[i].blit(self.Asset_Occupied1, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.LIGHTRED)
                    self.SeatSurf_[i].blit(txt, center_top(25, 5, txt.get_size()))

                    self.SeatSurf_P[i].blit(self.Asset_PreviewOccupied, (0, 0))
                    txt = Styles.SANS_H5.render(self.SeatIDs[i], 1, Styles.DARKGRAY)
                    self.SeatSurf_P[i].blit(txt, center_top(25, 5, txt.get_size()))

                    txt = Styles.SANS_H6.render(self.SeatNames[i], 1, Styles.WHITE)
                    self.SeatSurf[i].blit(txt, center_top(25, 30, txt.get_size()))
                    self.SeatSurf_[i].blit(txt, center_top(25, 30, txt.get_size()))
                    self.SeatSurf_P[i].blit(txt, center_top(25, 30, txt.get_size()))

            
    def show(self):
        """ 좌석을 표시함. """
        self.ShowSeats = True
        self.Alpha = 0.


    def hide(self):
        """ 좌석을 숨기고 미리보기로 전환함. """
        self.ShowSeats = False
        self.Alpha = 255.


    def mySeat(self, seatID: str):
        """
        내 좌석이 어딘지 기록함.
        - - -
        #### 매개변수:
        - **seatID:** 좌석 번호
        """
        self.MySeat = seatID
        self.Updated = True


    
    def Reset(self, x = 530, y = 35):
        self.MoveTo(x, y)

        self.Alpha = 0.

        self.CurrSurf   = Surface((50, 50))
        self.SeatIDs    = []
        self.SeatNames  = []
        self.SeatOccupied = []
        self.SeatReserved = []
        self.SeatSurf   = []
        self.SeatSurf_  = []
        self.SeatSurf_P = []
        self.SeatRect   = []

        self.Updated = True
        self.ShowSeats = False

        self.ClickedIndex = -1
        self.MySeat = None

        for a in ChairyData.ROOMDATA.Arrangement:
            self.SeatIDs.append(a[0])
            self.SeatNames.append(None)
            self.SeatOccupied.append(False)
            self.SeatReserved.append(False)
            self.SeatRect.append(Rect(a[1], a[2], 50, 50))
            self.SeatSurf.append(Surface((50, 50)))
            self.SeatSurf_.append(Surface((50, 50)))
            self.SeatSurf_P.append(Surface((50, 50)))

        self.updateSeatSurf()

        self.SURFACE.blit(self.Asset_Structure, (0, 0))

        for i in range(len(self.SeatIDs)):
            self.SURFACE.blit(self.SeatSurf_P[i], self.SeatRect[i])

    
    def Update(self, TICK):
        
        if self.ShowSeats:

            if self.Alpha < 255:
                self.Alpha += TICK * 2

                if self.Alpha > 255:
                    self.Alpha = 255.

                for i in range(len(self.SeatIDs)):
                    if self.SeatIDs[i] == self.MySeat:
                        self.CurrSurf.set_alpha(self.Alpha, RLEACCEL)
                        self.SURFACE.blit(self.CurrSurf, self.SeatRect[i])
                    else:
                        self.SeatSurf[i].set_alpha(self.Alpha, RLEACCEL)

                        self.SURFACE.blit(self.SeatSurf_P[i], self.SeatRect[i])

                        self.SURFACE.blit(self.SeatSurf[i], self.SeatRect[i])

                return True

        else:

            if self.Alpha > 0:
                self.Alpha -= TICK * 2

                if self.Alpha < 0:
                    self.Alpha = 0.

                for i in range(len(self.SeatIDs)):
                    if self.SeatIDs[i] == self.MySeat:
                        self.CurrSurf.set_alpha(self.Alpha, RLEACCEL)
                        self.SURFACE.blit(self.CurrSurf, self.SeatRect[i])

                    self.SeatSurf[i].set_alpha(self.Alpha, RLEACCEL)
                    
                    self.SURFACE.blit(self.SeatSurf_P[i], self.SeatRect[i])

                    self.SURFACE.blit(self.SeatSurf[i], self.SeatRect[i])

                return True
            
        return self.Updated


    def Frame(self, DISP):
        if self.Updated:
            self.Updated = False

        return DISP.blit(self.SURFACE, (self.X, self.Y))
    


    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        for index, rect in enumerate(self.SeatRect):
            if rect.collidepoint(POS[0] - self.X, POS[1] - self.Y):
                if self.SeatIDs[index] == self.MySeat:
                    return

                self.SURFACE.blit(self.SeatSurf_[index], self.SeatRect[index])
                self.ClickedIndex = index
                self.Updated = True
    

    def MouseButtonUp(self, POS, BUTTON) -> int:
        if BUTTON != 1 or self.ClickedIndex == -1:
            return -1
        
        self.SURFACE.blit(self.SeatSurf[self.ClickedIndex], self.SeatRect[self.ClickedIndex])
        self.Updated = True
        
        if self.SeatOccupied[self.ClickedIndex] or self.SeatReserved[self.ClickedIndex]:
            return -1

        ci = self.ClickedIndex
        self.ClickedIndex = -1
        if self.SeatRect[ci].collidepoint(POS[0] - self.X, POS[1] - self.Y):
            return ci
        else:
            return -1