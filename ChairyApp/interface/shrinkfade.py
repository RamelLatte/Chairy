
from .Component import Component
from pygame import Surface
from pygame.transform import smoothscale_by

from ..optimization.animation import FineAnimateSpdUp
from ..optimization.positioning import center_center


class ShrinkFadeAnimation(Component):


    SURFACE: Surface
    Size: tuple[int]
    Center: tuple[int]
    
    RESULT: Surface

    PerformAnimation: bool

    Updated: bool

    ScaleBy: float
    CurrentScale: float
    
    CurrentAlpha: float

    BackgroundColor: tuple[int]

    Speed: float

    Done: bool

    
    def __init__(self, X: int, Y: int, surface: Surface, scaleBy: float, speed: float, backgroundColor: tuple[int]):

        self.Size = surface.get_size()

        self.RESULT = Surface(self.Size)
        self.SURFACE = surface.convert_alpha(self.RESULT)

        self.Center = (self.Size[0] / 2, self.Size[1] / 2)

        self.PerformAnimation = False

        self.Updated = True

        self.ScaleBy = scaleBy
        self.CurrentScale = 1.0

        self.CurrentAlpha = 255.

        self.BackgroundColor = backgroundColor

        self.Speed = speed

        self.Done = False

        super().__init__(X, Y, self.Size[0], self.Size[1])



    def perform(self):
        self.PerformAnimation = True



    def Update(self, A_OFFSET, TICK):

        if not self.PerformAnimation or self.Done:
            return self.Updated

        if self.CurrentAlpha > 0. and self.CurrentScale > self.ScaleBy:
            self.CurrentScale = FineAnimateSpdUp(True, self.CurrentScale, 1.05, self.ScaleBy, self.Speed, A_OFFSET)
        
        self.CurrentAlpha = max(0., 127 * ((self.CurrentScale - self.ScaleBy) / (1.0 - self.ScaleBy))) * 2

        self.RESULT.fill(self.BackgroundColor)

        tmp = smoothscale_by(self.SURFACE, self.CurrentScale)
        tmp.set_alpha(self.CurrentAlpha)
        self.RESULT.blit(tmp, center_center(self.Center[0], self.Center[1], tmp.get_size()))

        if self.CurrentAlpha == 0. and not self.Done:
            self.Done = True

        return True
    


    def Frame(self, DISP):
        self.Updated = False

        DISP.fill(self.BackgroundColor, self.calculateTrailRect_Y())
        DISP.blit(self.RESULT, (self.X, self.Y))

        return self.calculateRect()