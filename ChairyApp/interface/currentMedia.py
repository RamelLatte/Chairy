
from .Component import Component
from .Scene import SceneManager
from .Styles import Styles
from ..chairyData import ChairyData
from pygame import Surface, Rect, transform, SRCALPHA, BLEND_RGBA_MULT



SPRLIGHTGRAY = (Styles.SPRLIGHTGRAY[0], Styles.SPRLIGHTGRAY[1], Styles.SPRLIGHTGRAY[2], 255)



class CurrentMedia(Component):
    """ ### 현재 재생 중인 미디어 """

    Asset_Mask: Surface
    Asset_Icon: Surface

    Mask_Title: Surface
    Mask_Mouse: Surface

    SURFACE: Surface
    SURFACE_: Surface

    Updated: bool
    
    Init: bool

    MouseIn: bool

    
    def __init__(self, x = 56, y = 1080):
        self.SURFACE = Surface((460, 90), (SRCALPHA))
        self.Init = False

        self.Asset_Icon = SceneManager.loadAsset('/ChairyApp/assets/media/iconSmall.png').convert()
        self.Asset_Mask = SceneManager.loadAsset('/ChairyApp/assets/media/maskSmall.png').convert_alpha(self.SURFACE)
        self.Mask_Title = SceneManager.loadAsset('/ChairyApp/assets/media/maskTitle.png').convert_alpha(self.SURFACE)
        self.Mask_Mouse = SceneManager.loadAsset('/ChairyApp/assets/media/maskMouse.png').convert_alpha()
        self.Reset()
        super().__init__(x, y, 460, 90)


    # 만능 ChatGPT가 작성한 함수
    @staticmethod
    def crop_and_scale(surface: Surface, target_size=(80, 80)):
        """
        지정된 Surface를 지정된 크기로 자르고 중앙에 맞춰줌.
        - - - 
        #### 매개변수:
        - **surface:** 자르고 조정할 Surface
        - **target_size:** 최종 Surface 크기
        """

        width, height = surface.get_size()

        # 중앙 기준으로 정사각형 영역 계산
        if width > height:
            # 가로가 더 길면
            offset = (width - height) // 2
            crop_rect = Rect(offset, 0, height, height)
        else:
            # 세로가 더 길거나 같으면
            offset = (height - width) // 2
            crop_rect = Rect(0, offset, width, width)
        
        # 잘라내기
        cropped_surface = surface.subsurface(crop_rect).copy()

        # 스케일링
        scaled_surface = transform.smoothscale(cropped_surface, target_size)

        return scaled_surface



    def Reset(self, x = 56, y = 1080):
        self.MoveTo(x, y)

        self.MouseIn = False

        self.newMouseFields(1)
        self.setMouseField_DisplayPos(0, self.X, self.Y, 80, 80)

        if not self.Init:
            self.Render()


    def Render(self):
        if ChairyData.CURRENT_MEDIA == None or not ChairyData.CURRENT_MEDIA.Updated:
            return
        
        ChairyData.CURRENT_MEDIA.Updated = False
        self.Updated = True

        self.SURFACE.fill(SPRLIGHTGRAY)

        self.SURFACE.blit(self.Asset_Icon, (0, 0))

        self.SURFACE.blit(Styles.SANS_B5.render('이 기기에서 재생 중', 1, Styles.GREEN, Styles.SPRLIGHTGRAY), (95, 8))
        self.SURFACE.blit(Styles.SANS_H4.render(ChairyData.CURRENT_MEDIA.Title, 1, Styles.BLACK, Styles.SPRLIGHTGRAY), (95, 24))
        self.SURFACE.blit(Styles.SANS_B4.render(ChairyData.CURRENT_MEDIA.Artist, 1, Styles.BLACK, Styles.SPRLIGHTGRAY), (95, 58))
        self.SURFACE.blit(self.Mask_Title, (80, 0), special_flags=(BLEND_RGBA_MULT))
        
        if ChairyData.CURRENT_MEDIA.Thumbnail is not None:
            masked = Surface((80, 80), (SRCALPHA))
            masked = CurrentMedia.crop_and_scale(ChairyData.CURRENT_MEDIA.getThumbnail().convert_alpha(masked))
            
            # 여기! convert_alpha(self.SURFACE) 이런 거 절대 쓰지마 - ChatGPT
            # 진짜 해봤는데 안써도 된다 - RamelLatte
            masked.blit(self.Asset_Mask, (0, 0), special_flags=(BLEND_RGBA_MULT))

            self.SURFACE.blit(masked, (0, 0))

        if not self.Init:
            self.Init = True

        self.SURFACE_ = self.SURFACE.copy()
        self.SURFACE_.blit(self.Mask_Mouse, (0, 0))

    
    def Update(self):
        return (self.Updated or self.Y != self._Y)


    def Frame(self, DISP):
        self.Updated = False

        DISP.fill(SPRLIGHTGRAY, self.calculateTrailRect_Y())

        if self.MouseIn:
            DISP.blit(self.SURFACE_, (self.X, self.Y))
        else:
            DISP.blit(self.SURFACE, (self.X, self.Y))

        return self.calculateRect()
    

    def MouseMotion(self, POS):
        
        if self.collidepoint(0, POS):
            
            if not self.MouseIn:
                self.MouseIn = True
                self.Updated = True

        elif self.MouseIn:

            self.MouseIn = False
            self.Updated = True


    def MouseButtonUp(self, POS, BUTTON):
        return (BUTTON == 1 and self.MouseIn)