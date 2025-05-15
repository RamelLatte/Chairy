
from ..interface import Scene, SceneManager, Styles, Interface
from pygame import Surface, Rect, SRCALPHA, BLEND_RGBA_MULT
from ..chairyData import ChairyData

from ..optimization.animation import AnimateSpdUp, Animate


class Media(Scene):
    """ ### 이 기기에서 재생 중인 미디어 """


    ID_Group_Y: int

    InteractionStep: int
    # 0: mainScene에서 전환 애니메이션 1
    # 1: mainScene에서 전환 애니메이션 2
    # 2: 아무 애니메이션 안함, 타이틀 스크롤링
    # 3: mainScene으로 전환 애니메이션 1
    # 4: mainScene으로 전환 애니메이션 2

    Surface_Top     : Surface # 상단부
    Surface_Bottom  : Surface # 하단부
    Y               : int     # 현재 Y좌표
    Y_              : int     # 직전 프레임의 Y좌표

    Txt_Album   : Surface # 렌더링된 앨범명

    Txt_Title   : Surface # 렌더링된 트랙명
    Scroll_Title: bool    # 트랙명 좌우 스크롤 여부
    ScrollDirection: bool # 트랙명 좌우 스크롤 방향
    TxtPos_Title: int     # 현재 트랙명 스크롤 위치
    TxtPos_Title_: int    # 목표 트랙명 스크롤 위치

    Txt_Artist  : Surface # 렌더링된 게시자명

    Mask_Album  : Surface # 앨범 마스킹용 에셋
    Mask_Title  : Surface # 트랙명 마스킹용 에셋

    Asset_Album : Surface # 앨범 썸네일 기본 에셋



    def __init__(self):
        self.ID_Group_Y = 432
        self.Y = 1080
        self.Y_ = self.Y
        self.InteractionStep = 0
        self.ScrollDirection = False
        self.TxtPos_Title = 0
        self.TxtPos_Title_ = 0
        
        self.Render()
        
        super().__init__()

    
    def Render(self):
        """ 내부 렌더링 작업 """
        self.Surface_Top    = Surface((227, 294), (SRCALPHA))
        self.Surface_Bottom = Surface((438, 113), (SRCALPHA))

        self.Asset_Album = SceneManager.loadAsset('/ChairyApp/assets/media/iconLarge.png').convert(self.Surface_Top)
        self.Mask_Album  = SceneManager.loadAsset('/ChairyApp/assets/media/maskLarge.png').convert(self.Surface_Top)
        self.Mask_Title  = SceneManager.loadAsset('/ChairyApp/assets/media/maskTitleLarge.png').convert_alpha(self.Surface_Bottom)

        self.Surface_Top.fill((0, 0, 0, 0))
        self.Surface_Top.blit(Styles.SANS_H4.render('이 기기에서 재생 중', 1, Styles.GREEN), (4, 0))
        self.Surface_Top.blit(self.Asset_Album, (0, 64))

        if ChairyData.CURRENT_MEDIA.Thumbnail is not None:
            thumbnail = Surface((200, 200), (SRCALPHA))
            thumbnail.blit(Interface.OT_CurrentMedia.crop_and_scale(ChairyData.CURRENT_MEDIA.getThumbnail(), (200, 200)), (0, 0))
            thumbnail.blit(self.Mask_Album, (0, 0), special_flags=(BLEND_RGBA_MULT))
            self.Surface_Top.blit(thumbnail, (0, 64))

        SceneManager.SCENE_TIME = 0
        self.ScrollDirection = False
        self.TxtPos_Title = 0
        self.TxtPos_Title_ = 0

        self.Txt_Album = Styles.SANS_H5.render(ChairyData.CURRENT_MEDIA.Album, 1, Styles.DARKGRAY)

        self.Txt_Title = Styles.SANS_H3.render(ChairyData.CURRENT_MEDIA.Title, 1, Styles.BLACK)
        self.Scroll_Title = self.Txt_Title.get_width() > 420
        self.TxtPos_Title_ = 400 - self.Txt_Title.get_width()

        self.Txt_Artist = Styles.SANS_B3.render(ChairyData.CURRENT_MEDIA.Artist, 1, Styles.BLACK)
        
        self.Title()


    def Title(self):
        """ 타이틀 렌더링 """
        self.Surface_Bottom.fill((Styles.SPRLIGHTGRAY[0], Styles.SPRLIGHTGRAY[1], Styles.SPRLIGHTGRAY[2], 255))
        self.Surface_Bottom.blit(self.Txt_Album, (18, 0))
        self.Surface_Bottom.blit(self.Txt_Title, (self.TxtPos_Title + 18, 35))
        self.Surface_Bottom.blit(self.Txt_Artist, (18, 93))
        self.Surface_Bottom.blit(self.Mask_Title, (0, 0), special_flags=(BLEND_RGBA_MULT))
    

    
    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        return super().On_Init(DISPLAY)


    def On_Update(self, ANIMATION_OFFSET, TICK):

        if ChairyData.CURRENT_MEDIA.Updated and ChairyData.CURRENT_MEDIA.Playing:
            self.Render()
            Interface.OT_CurrentMedia.Render()

        if not ChairyData.CURRENT_MEDIA.Playing and self.InteractionStep < 3:
            self.InteractionStep = 3
        
        if self.InteractionStep == 0:

            self.ID_Group_Y = AnimateSpdUp(True, self.ID_Group_Y, 460, -216, 1.5, ANIMATION_OFFSET)
            Interface.OT_CurrentMedia.AnimateSpdUp_Y(False, 935, 1080, 2.25, ANIMATION_OFFSET)
            
            if self.ID_Group_Y == -216 and Interface.OT_CurrentMedia.Y == 1080:
                self.InteractionStep = 1

        elif self.InteractionStep == 1:

            self.Y = Animate(self.Y, 338, 1.0, ANIMATION_OFFSET)

            if self.Y < 400:
                Interface.MD_HideMediaBtn.Animate_Y(873, 1.0, ANIMATION_OFFSET)

            if self.Y == 338 and Interface.MD_HideMediaBtn.Y == 873:
                self.InteractionStep = 2

        elif self.InteractionStep == 2:

            if SceneManager.SCENE_TIME > 2000 and self.Scroll_Title:

                if self.ScrollDirection:
                    if self.TxtPos_Title != 0:
                        self.TxtPos_Title += TICK * 0.1
                        if self.TxtPos_Title > 0:
                            self.TxtPos_Title = 0
                            self.ScrollDirection = not self.ScrollDirection
                            SceneManager.SCENE_TIME = 0
                        self.Title()

                else:

                    if self.TxtPos_Title != self.TxtPos_Title_:
                        self.TxtPos_Title -= TICK * 0.1
                        if self.TxtPos_Title < self.TxtPos_Title_:
                            self.TxtPos_Title = self.TxtPos_Title_
                            self.ScrollDirection = not self.ScrollDirection
                            SceneManager.SCENE_TIME = 0
                        self.Title()

        elif self.InteractionStep == 3:

            if Interface.MD_HideMediaBtn.Y > 1000:
                self.Y = AnimateSpdUp(False, self.Y, 300, 1080, 1.5, ANIMATION_OFFSET)

            Interface.MD_HideMediaBtn.AnimateSpdUp_Y(False, 850, 1080, 2.25, ANIMATION_OFFSET)

            if self.Y == 1080 and Interface.MD_HideMediaBtn.Y == 1080:
                Interface.OT_CurrentMedia.Reset()
                self.InteractionStep = 4

        elif self.InteractionStep == 4:

            if Interface.OT_CurrentMedia.Init and ChairyData.CURRENT_MEDIA.Playing:
                Interface.OT_CurrentMedia.Animate_Y(955, 1.25, ANIMATION_OFFSET)

            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            if (Interface.OT_CurrentMedia.Y == 955 or not ChairyData.CURRENT_MEDIA.Playing) and self.ID_Group_Y == 432:
                SceneManager.CURRENT_SCENE = SceneManager.MainScene
                SceneManager.SCENE_TIME = 0
                SceneManager.MainScene.InteractionStep = 0


    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        
        # 화면 오른쪽 요소 렌더링
        if Interface.SD_DateTime.Update():
            RECTS.append(Interface.SD_DateTime.Frame(DISPLAY))

        if Interface.SD_DietAndSchedule.Update():
            RECTS.append(Interface.SD_DietAndSchedule.Frame(DISPLAY))

        if Interface.SD_SeatingStatus.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SD_SeatingStatus.Frame(DISPLAY))

        # 좌석표 렌더링
        if Interface.ST_SeatDisplay.Update(TICK):
            RECTS.append(Interface.ST_SeatDisplay.Frame(DISPLAY))

        # 자세한 미디어 정보
        elif self.InteractionStep in (1, 3, 4):

            if self.Y != self.Y_:
                d = self.Y - self.Y_
                if d < 0:
                    DISPLAY.fill(Styles.SPRLIGHTGRAY, Rect(51, self.Y, 438, - d + 405))
                    DISPLAY.blit(self.Surface_Top, (69, self.Y))
                    DISPLAY.blit(self.Surface_Bottom, (51, self.Y + 291))
                    self.Y_ = self.Y
                    RECTS.append(Rect(51, self.Y, 438, 405 - d))
                else:
                    DISPLAY.fill(Styles.SPRLIGHTGRAY, Rect(51, self.Y_ - 1, 438, d + 406))
                    DISPLAY.blit(self.Surface_Top, (69, self.Y))
                    DISPLAY.blit(self.Surface_Bottom, (51, self.Y + 291))
                    self.Y_ = self.Y
                    RECTS.append(Rect(51, self.Y_, 438, 404 + d))
            else:
                DISPLAY.fill(Styles.SPRLIGHTGRAY, Rect(51, 338, 438, 404))
                DISPLAY.blit(self.Surface_Top, (69, self.Y))
                DISPLAY.blit(self.Surface_Bottom, (51, self.Y + 291))
                RECTS.append(Rect(51, 338, 438, 404))

        elif self.InteractionStep == 2:
            DISPLAY.fill(Styles.SPRLIGHTGRAY, Rect(51, 338, 438, 404))
            DISPLAY.blit(self.Surface_Top, (69, self.Y))
            DISPLAY.blit(self.Surface_Bottom, (51, self.Y + 291))
            RECTS.append(Rect(51, 338, 438, 404))
        
        # 가리기 버튼
        if Interface.MD_HideMediaBtn.Update():
            RECTS.append(Interface.MD_HideMediaBtn.Frame(DISPLAY))

        # 학번 입력란 그룹 렌더링
        Interface.ID_InstructionText.Y = self.ID_Group_Y
        Interface.ID_KeyInstruction.Y = self.ID_Group_Y + 187
        Interface.ID_IdInputDialog.Y = self.ID_Group_Y + 60

        if Interface.ID_InstructionText.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.ID_InstructionText.Frame(DISPLAY))

        if Interface.ID_KeyInstruction.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.ID_KeyInstruction.Frame(DISPLAY))
        
        if Interface.ID_IdInputDialog.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.ID_IdInputDialog.Frame(DISPLAY))

        # 현재 미디어 업데이트
        if Interface.OT_CurrentMedia.Update():
            RECTS.append(Interface.OT_CurrentMedia.Frame(DISPLAY))


    def Draw(self, SURFACE):
        SURFACE.fill(Styles.SPRLIGHTGRAY)
        
        # 화면 오른쪽 요소 렌더링
        Interface.SD_DateTime.Frame(SURFACE)
        Interface.SD_DietAndSchedule.Frame(SURFACE)

        Interface.SD_SeatingStatus.Frame(SURFACE)

        # 좌석표 렌더링
        Interface.ST_SeatDisplay.Frame(SURFACE)

        # 자세한 미디어 정보
        SURFACE.blit(self.Surface_Top, (69, self.Y))
        SURFACE.blit(self.Surface_Bottom, (51, self.Y + 291))
        
        # 가리기 버튼
        Interface.MD_HideMediaBtn.Frame(SURFACE)

        # 학번 입력란
        Interface.ID_InstructionText.Frame(SURFACE)
        Interface.ID_KeyInstruction.Frame(SURFACE)        
        Interface.ID_IdInputDialog.Frame(SURFACE)

        # 현재 재생중
        Interface.OT_CurrentMedia.Frame(SURFACE)
                


    def Event_MouseMotion(self, POS):
        
        Interface.MD_HideMediaBtn.MouseMotion(POS)

        if self.InteractionStep == 4:
            Interface.OT_CurrentMedia.MouseMotion(POS)


    def Event_MouseButtonDown(self, POS, BUTTON):
        
        Interface.MD_HideMediaBtn.MouseButtonDown(POS, BUTTON)


    def Event_MouseButtonUp(self, POS, BUTTON):
        
        if Interface.MD_HideMediaBtn.MouseButtonUp(POS, BUTTON) and self.InteractionStep < 3:
            self.InteractionStep = 3