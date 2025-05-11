
from .Component import Component
from pygame import Surface, Rect
from .Styles import Styles
from .Scene import SceneManager as SM

from ..optimization.positioning import collidepoint



class CancelButton(Component):
    """ ### 취소 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool

    Y_      : int


    def __init__(self):
        super().__init__()
        
        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/components/CancelBtn0.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/CancelBtn1.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/CancelBtn2.png').convert()
                ]
        self.Reset()


    def Reset(self, x = 123, y = 1080):
        self.X = x
        self.Y = y

        self.Button = 0

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True
        self.Y_ = self.Y

    
    def reset(self):
        self.Show   = True
        self.Y      = 1080
        self.Y_     = 1080
        self.Updated = True

    
    def Update(self):
        return (self.Updated or self.Y != self.Y_)
    

    def Frame(self, DISP):
        self.Updated = False

        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 60, 283, - d + 1))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 283, 61 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 283, d + 2))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 283, 60 + d)
        else:
            return DISP.blit(self.Assets[self.Button], (self.X, self.Y))
        

    def _collide(self, POS) -> bool:
        return collidepoint(self.X, self.Y, 283, 60, POS)
    

    def MouseMotion(self, POS):

        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False
    



class CheckoutButton(Component):
    """ ### 퇴실 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool

    Y_      : int

    Alpha   : float
    Alpha_  : float
    Show    : bool


    def __init__(self):
        super().__init__()

        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/components/CheckoutBtn0.png'),
                    SM.loadAsset('/ChairyApp/assets/components/CheckoutBtn1.png'),
                    SM.loadAsset('/ChairyApp/assets/components/CheckoutBtn2.png')
                ]
        self.Reset()

    def Reset(self, x = 123, y = 1080):
        self.X = 123
        self.Y = 1080
        
        self.Button = 0

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True
        self.Y_ = self.Y

        self.Alpha  = 255.
        self.Alpha_ = 255.
        self.Show   = True

    
    def hide(self):
        self.Button = 0
        self.Show   = False


    def show(self):
        self.Show = True

    
    def reset(self):
        self.Show   = True
        self.Y      = 1080
        self.Y_     = 1080
        self.Alpha  = 255.
        self.Alpha_ = 255.
        self.Assets[0].set_alpha(255)
        self.Updated = True

    
    def Update(self, TICK: int):
        if self.Show:

            if self.Alpha < 255:
                self.Alpha += TICK * 2

                if self.Alpha > 255:
                    self.Alpha = 255.

                self.Assets[0].set_alpha(self.Alpha)

                return True

        else:

            if self.Alpha > 0:
                self.Alpha -= TICK * 2

                if self.Alpha < 0:
                    self.Alpha = 0.

                self.Assets[0].set_alpha(self.Alpha)

                return True

        return (self.Updated or self.Y != self.Y_)
    

    def Frame(self, DISP):
        self.Updated = False
        
        if self.Alpha != self.Alpha_:
            DISP.fill(Styles.SPRLIGHTGRAY, [self.X, self.Y, 283, 60])
            self.Alpha_ = self.Alpha

        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 60, 283, - d + 1))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 283, 61 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 283, d + 2))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 283, 60 + d)
        else:
            return DISP.blit(self.Assets[self.Button], (self.X, self.Y))
        

    def _collide(self, POS) -> bool:
        return collidepoint(self.X, self.Y, 283, 60, POS)
    

    def MouseMotion(self, POS):

        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False
    



class MoveButton(Component):
    """ ### 이동동 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool
    Enabled : bool

    MouseIn : bool
    Clicked : bool

    Y_      : int

    Alpha   : float
    Alpha_  : float
    Show    : bool


    def __init__(self):
        super().__init__()

        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/components/MoveBtn0.png'),
                    SM.loadAsset('/ChairyApp/assets/components/MoveBtn1.png'),
                    SM.loadAsset('/ChairyApp/assets/components/MoveBtn2.png'),
                    SM.loadAsset('/ChairyApp/assets/components/MoveBtn3.png')
                ]
        self.Reset()


    def Reset(self, x = 123, y = 1080):
        self.X = x
        self.Y = y

        self.Button = 0

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True
        self.Enabled = True
        self.Y_ = self.Y

        self.Alpha  = 255.
        self.Alpha_ = 255.
        self.Show   = True


    def enable(self):
        self.Enabled = True
        self.Button = 0
        self.Updated = True


    def disable(self):
        self.Enabled = False
        self.Button = 3
        self.Updated = True


    def hide(self):
        self.Button = 0
        self.Alpha = 255.
        self.Show   = False


    def show(self):
        self.Alpha = 0.
        self.Show = True


    def reset(self):
        self.Show   = True
        self.Y      = 1080
        self.Y_     = 1080
        self.Alpha  = 255.
        self.Alpha_ = 255.
        self.Assets[0].set_alpha(255)
        self.Updated = True

    
    def Update(self, TICK: int):
        if self.Show:

            if self.Alpha < 255:
                self.Alpha += TICK * 2

                if self.Alpha > 255:
                    self.Alpha = 255.

                self.Assets[0].set_alpha(self.Alpha)

                return True

        else:

            if self.Alpha > 0:
                self.Alpha -= TICK * 2

                if self.Alpha < 0:
                    self.Alpha = 0.

                self.Assets[0].set_alpha(self.Alpha)

                return True

        return (self.Updated or self.Y != self.Y_)
    

    def Frame(self, DISP):
        self.Updated = False

        if self.Alpha != self.Alpha_:
            DISP.fill(Styles.SPRLIGHTGRAY, [self.X, self.Y, 283, 60])
            self.Alpha_ = self.Alpha

        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 60, 283, - d + 1))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 283, 61 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 283, d + 2))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 283, 60 + d)
        else:
            return DISP.blit(self.Assets[self.Button], (self.X, self.Y))
        

    def _collide(self, POS) -> bool:
        return collidepoint(self.X, self.Y, 283, 60, POS)
    

    def MouseMotion(self, POS):
        if not self.Enabled:
            return

        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1 or not self.Enabled:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1 or not self.Enabled:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False
    



class StatisticsExitButton(Component):
    """ ### 통계 화면에서 '처음 화면으로 돌아가기' 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool


    def __init__(self):
        super().__init__()

        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/statistics/StatisticsCancelBtn0.png'),
                    SM.loadAsset('/ChairyApp/assets/statistics/StatisticsCancelBtn1.png'),
                    SM.loadAsset('/ChairyApp/assets/statistics/StatisticsCancelBtn2.png'),
                ]
        self.Reset(0, 0)


    def Reset(self, x, y):
        self.X = x
        self.Y = y
        self.Button = 0

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True

    
    def Update(self):
        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False

        DISP.blit(self.Assets[self.Button], (1680, 15))
        return Rect(1680, 15, 200, 40)
        

    def _collide(self, POS) -> bool:
        return collidepoint(1680, 15, 200, 40, POS)
    

    def MouseMotion(self, POS):
        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False
    



class StatisticsExportButton(Component):
    """ ### 통계 내보내기 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool


    def __init__(self, x, y):
        super().__init__()

        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/statistics/Export0.png'),
                    SM.loadAsset('/ChairyApp/assets/statistics/Export1.png'),
                    SM.loadAsset('/ChairyApp/assets/statistics/Export2.png'),
                ]
        self.Reset(x, y)


    def Reset(self, x, y):
        self.Button = 0
        self.X = x
        self.Y = y

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True

    
    def Update(self):
        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False

        DISP.blit(self.Assets[self.Button], (self.X, self.Y))
        return Rect(self.X, self.Y, 250, 70)
        

    def _collide(self, POS) -> bool:
        return collidepoint(self.X, self.Y, 250, 70, POS)
    

    def MouseMotion(self, POS):
        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False
 
 


class HideMediaButton(Component):
    """ ### 미디어 정보 접기 버튼 """

    Assets  : list[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool

    Y_      : int


    def __init__(self):
        super().__init__()
        
        self.Assets = [
                    SM.loadAsset('/ChairyApp/assets/media/Hide0.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/media/Hide1.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/media/Hide2.png').convert()
                ]
        self.Reset()


    def Reset(self, x = 165, y = 1080):
        self.X = x
        self.Y = y

        self.Button = 0

        self.MouseIn = False
        self.Clicked = False

        self.Updated = True
        self.Y_ = self.Y

    
    def reset(self):
        self.Show   = True
        self.Y      = 1080
        self.Y_     = 1080
        self.Updated = True

    
    def Update(self):
        return (self.Updated or self.Y != self.Y_)
    

    def Frame(self, DISP):
        self.Updated = False

        if self.Y != self.Y_:
            d = self.Y - self.Y_
            if d < 0:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y + 50, 210, - d + 1))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y, 210, 51 - d)
            else:
                DISP.fill(Styles.SPRLIGHTGRAY, Rect(self.X, self.Y_ - 1, 210, d + 2))
                DISP.blit(self.Assets[self.Button], (self.X, self.Y))
                self.Y_ = self.Y
                return Rect(self.X, self.Y_, 210, 50 + d)
        else:
            return DISP.blit(self.Assets[self.Button], (self.X, self.Y))
        

    def _collide(self, POS) -> bool:
        return collidepoint(self.X, self.Y, 210, 50, POS)
    

    def MouseMotion(self, POS):

        if self._collide(POS):

            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

                if self.Clicked:
                    self.Button = 2
                else:
                    self.Button = 1

        else:
            
            if self.MouseIn:
                self.MouseIn = False
                self.Button = 0
                self.Updated = True

    
    def MouseButtonDown(self, POS, BUTTON):
        if BUTTON != 1:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1:
            return False
        
        if self.Clicked:
            self.Clicked = False
            self.Updated = True

            if self._collide(POS):
                self.Button = 1
                return True
            else:
                self.Button = 0
            
        return False