
from threading import Thread
from .interface import Styles
from .chairyData import ChairyData
import pygame as pg



class StartDialog(Thread):
    """ ### 시작 창 """


    def __init__(self, DIR: str, DISPLAY: pg.Surface, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        self.ASSET = pg.image.load(DIR + "/ChairyApp/assets/StartDialog.png")
        self.DISP = DISPLAY
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    
    def run(self):

        self.ASSET = self.ASSET.convert(self.DISP)

        W = 0
        W_ = 0
        
        CLK = pg.time.Clock()
        tick = 0
        
        while 1:
            tick = CLK.tick(60)
            
            self.DISP.blit(self.ASSET, (0, 0))

            W_ = (ChairyData.LOADPROGRESS / ChairyData.MAX_PROGRESS) * 300

            if W != W_:
                W += (W_ - W) * tick * 0.02

            pg.draw.rect(self.DISP, Styles.DARKGRAY, [100, 231, W, 4])

            if W > 299:
                break

            pg.display.update()
            
            pg.event.get()

        return