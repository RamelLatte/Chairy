from .Component import Component
from pygame import Surface
from .Styles import Styles
from .Scene import SceneManager as SM



class SetPasswordButton(Component):
    """ ### 비밀번호 설정 버튼 """

    Assets  : tuple[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool

    Alpha: float
    Show: bool


    def __init__(self, x = 172, y = 1080):
        super().__init__(x, y, 185, 50)
        
        self.Assets = (
                    SM.loadAsset('/ChairyApp/assets/components/Password0.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/Password1.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/Password2.png').convert()
                )
        self.Reset()


    def Reset(self, x = 172, y = 1080):
        self.MoveTo(x, y)

        self.MouseIn = False
        self.Clicked = False

        self.newMouseFields(1)
        self.setMouseField(0, 0, 0, 185, 50)

        self.reset()


    def show(self):
        self.Show = True


    def hide(self):
        self.Button = 0
        self.MouseIn = False
        self.Clicked = False
        self.Show = False

    
    def reset(self):
        self.Show   = True
        self.MoveTo(self.X, 1080)

        self.Button = 0
        self.Alpha = 255.

        self.Assets[0].set_alpha(255)

        self.Updated = True

    
    def Update(self, TICK):

        if self.Show:
            if self.Alpha < 255.:
                self.Alpha += TICK * 2
                if self.Alpha > 255.:
                    self.Alpha = 255.
                self.Assets[0].set_alpha(self.Alpha)
                return True
        else:
            if self.Alpha > 0.:
                self.Alpha -= TICK * 2
                if self.Alpha < 0.:
                    self.Alpha = 0.
                self.Assets[0].set_alpha(self.Alpha)
                return True

        return (self.Updated or self.Y != self._Y)
    

    def Frame(self, DISP):
        self.Updated = False

        r = self.calculateRect()

        DISP.fill(Styles.SPRLIGHTGRAY, r)

        DISP.blit(self.Assets[self.Button], (self.X, self.Y))

        return r
        

    def _collide(self, POS) -> bool:
        return self.collidepoint(0, POS)
    

    def MouseMotion(self, POS):
        if not self.Show:
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
        if BUTTON != 1 or not self.Show:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1 or not self.Show:
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
    


class DeletePasswordButton(Component):
    """ ### 비밀번호 삭제 버튼 """

    Assets  : tuple[Surface]
    Button  : int

    Updated : bool

    MouseIn : bool
    Clicked : bool

    Show: bool


    def __init__(self, x = 172, y = 877):
        super().__init__(x, y, 185, 50)
        
        self.Assets = (
                    SM.loadAsset('/ChairyApp/assets/components/RemovePassword0.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/RemovePassword1.png').convert(),
                    SM.loadAsset('/ChairyApp/assets/components/RemovePassword2.png').convert()
                )
        self.Reset()


    def Reset(self, x = 172, y = 877):
        self.MoveTo(x, y)

        self.MouseIn = False
        self.Clicked = False

        self.newMouseFields(1)
        self.setMouseField(0, 0, 0, 185, 50)

        self.reset()


    def show(self):
        self.Show = True
        self.Updated = True


    def hide(self):
        self.Button = 0
        self.MouseIn = False
        self.Clicked = False
        self.Show = False
        self.Updated = True

    
    def reset(self):
        self.Show   = True
        self.MoveTo(self.X, 877)

        self.Button = 0
        self.Updated = True

    
    def Update(self, TICK):
        return (self.Updated or self.Y != self._Y)
    

    def Frame(self, DISP):
        self.Updated = False

        r = self.calculateRect()

        DISP.fill(Styles.SPRLIGHTGRAY, r)

        if self.Show:
            DISP.blit(self.Assets[self.Button], (self.X, self.Y))

        return r
        

    def _collide(self, POS) -> bool:
        return self.collidepoint(0, POS)
    

    def MouseMotion(self, POS):
        if not self.Show:
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
        if BUTTON != 1 or not self.Show:
            return
        
        if self._collide(POS) and not self.Clicked:
            self.Clicked = True
            self.Button = 2
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON) -> bool:
        if BUTTON != 1 or not self.Show:
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
    


class PasswordDialog(Component):

    SURFACE: Surface

    CurrentStep: str
    Color: tuple[int]

    Assets: tuple[Surface]
    SlotAsset: Surface

    Alpha: float
    Show: bool

    Updated: bool

    Password: str
    Delay: int
    CompleteDelay: int

    Freeze: bool


    def __init__(self, x, y, step: str = '비밀번호 입력', newPassword: bool = False, Hidden: bool = True, color: tuple[int] = Styles.BLACK):
        super().__init__(x, y, 290, 343)

        self.SURFACE = Surface((290, 343))

        self.CurrentStep = step
        self.NewPassword = newPassword
        self.Color = color

        self.Assets = (
            SM.loadAsset('/ChairyApp/assets/components/Password.png').convert(self.SURFACE),
            SM.loadAsset('/ChairyApp/assets/components/SetPassword.png').convert(self.SURFACE)
        )

        self.SlotAsset = SM.loadAsset('/ChairyApp/assets/components/PasswordFilled.png').convert(self.SURFACE)

        if Hidden:
            self.Alpha = 0.
            self.Show = False
        else:
            self.Alpha = 255.
            self.Show = True

        self.Updated = True
        self.Freeze = False

        self.Password = ''
        self.Delay = 0
        self.CompleteDelay = 10

        self._Render()


    def show(self):
        self.Show = True


    def hide(self):
        self.Show = False


    def hideInstantly(self):
        self.Show = False
        self.Alpha = 0.
        self.SURFACE.set_alpha(self.Alpha)
        self.Updated = True


    def step(self, step: str = '비밀번호 입력', newPassword: bool = False, color: tuple[int] = Styles.BLACK):
        self.CurrentStep = step
        self.NewPassword = newPassword
        self.Color = color

        self._Render()
    

    def getPassword(self) -> str:
        return self.Password
    

    def append(self, num: int):

        if self.Freeze or len(self.Password) >= 4:
            return
        
        if len(self.Password) == 3:
            self.Delay = self.CompleteDelay

        self.Password += str(num)
        self._Render()


    def delete(self):

        if self.Freeze or len(self.Password) <= 0:
            return

        self.Password = self.Password[:len(self.Password)-1]
        self._Render()


    def clear(self):
        self.Password = ''
        self._Render()


    def freeze(self):
        self.Freeze = True


    def unfreeze(self):
        self.Freeze = False


    def done(self) -> bool:
        return not self.Freeze and len(self.Password) == 4 and self.Delay <= 0


    def _Render(self):

        self.SURFACE.fill(Styles.SPRLIGHTGRAY, (0, 0, 290, 33))
        self.SURFACE.blit(self.Assets[1 if self.NewPassword else 0], (0, 33))

        for index in range(len(self.Password)):
            self.SURFACE.blit(self.SlotAsset, (18 + 68 * index, 55))

        self.SURFACE.blit(Styles.SANS_H5.render(self.CurrentStep, 1, self.Color, Styles.SPRLIGHTGRAY), (10, 0))
        self.SURFACE.set_alpha(self.Alpha)

        self.Updated = True


    def Reset(self, x, y):
        self.Alpha = 255.
        self.Show = True
        self.SURFACE.set_alpha(self.Alpha)
        self.Updated = True
        return super().Reset(x, y)
    

    def Update(self, TICK):

        if self.Delay > 0:
            self.Delay -= 1

        if self.Show:

            if self.Alpha < 255.:
                self.Alpha += TICK * 2

                if self.Alpha > 255.:
                    self.Alpha = 255.

                self.SURFACE.set_alpha(self.Alpha)
                self.Updated = True

        else:

            if self.Alpha > 0.:
                self.Alpha -= TICK * 2

                if self.Alpha < 0.:
                    self.Alpha = 0.

                self.SURFACE.set_alpha(self.Alpha)
                self.Updated = True

        return self.Updated
    

    def Frame(self, DISP):
        self.Updated = False
        
        r = self.calculateRect()

        DISP.fill(Styles.SPRLIGHTGRAY, r)
        DISP.blit(self.SURFACE, (self.X, self.Y))

        return r