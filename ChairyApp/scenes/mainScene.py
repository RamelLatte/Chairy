
from ..interface import Interface, Scene, SceneManager, Styles, SeatsDataVerifyError
from ..chairyData import ChairyData, StudentData
from pygame import constants, Surface
from ..Logging import LoggingManager as logging
from .password import Password

from ..optimization.animation import Animate, AnimateSpdUp
from ..optimization.positioning import collidepoint



class MainScene(Scene):
    """
    ### MainScene
    
    가장 주요한 장면이며, 학번 입력과 입퇴실 및 이동 과정을 관장하는 장면.
    """

    InteractionStep : float
    # 0 ~ 3: 학번 입력
    # 4: 비밀번호 확인
    # 4.5: StudentInfo 확인
    # 5: 미등록 학번
    # 6: 좌석 선택
    # 7: 단일 지우기 애니메이션
    # 8: 취소 애니메이션
    # 9: 입실 완료
    # 10: 지정석 입실 완료 1
    # 11: 지정석 입실 완료 2
    # 12: 지정석 입실 완료 3
    # 13: 퇴실/이동 선택
    # 14: 퇴실/이동 취소
    # 15: 퇴실/이동 단일 지우기
    # 16: 퇴실 완료
    # 17: 이동 단계 진입
    # 18: 이동할 자리 선택
    # 19: 이동 단계 취소
    # 20: 이동 단계 학번 단일 지우기
    # 21: 이동 완료

    ID_Group_Y: int

    StudentHoverID: str

    Init: bool = False
    LogoImage: Surface

    IdleTime: int = 0


    def __init__(self):
        self.Identifier = 'MainScene'

        self.ID_Group_Y = 432
        self.InteractionStep = 0
        
        MainScene.Init = False
        MainScene.StudentHoverID = None

        MainScene.LogoImage = SceneManager.loadAsset('/ChairyApp/assets/components/BottomLogo.png').convert()

    
    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)

        # 로고
        DISPLAY.blit(MainScene.LogoImage, (1644, 985))

        self.ID_Group_Y = 432

        Interface.SD_SeatingStatus.RoomUpdated()

        Interface.SD_DateTime.Reset()
        Interface.SD_DietAndSchedule.Reset()
        Interface.SD_SeatingStatus.Reset()
        Interface.SD_QuickAccess.Reset()

        Interface.ID_InstructionText.Reset(300, Styles.SANS_H4, "학번을 입력합니다", Styles.BLACK)
        Interface.ID_IdInputDialog.Reset()
        Interface.ID_KeyInstruction.Reset()

        Interface.ST_SeatDisplay.Reset()
        Interface.ST_StudentInfo.Reset()

        Interface.BTN_Cancel.Reset()
        Interface.BTN_Checkout.Reset()
        Interface.BTN_Move.Reset()

        Interface.OT_CurrentMedia.Reset()

        self.Draw(DISPLAY)

        if not MainScene.Init:
            MainScene.Init = True
            if ChairyData.LATEST_VERSION:
                Interface.LY_Notice.show_LatestVersion()
            else:
                Interface.LY_Notice.show_Update()



    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        
        # 화면 오른쪽 요소 렌더링
        if Interface.SD_DateTime.Update():
            RECTS.append(Interface.SD_DateTime.Frame(DISPLAY))

        if Interface.SD_DietAndSchedule.Update():
            RECTS.append(Interface.SD_DietAndSchedule.Frame(DISPLAY))

        if Interface.SD_SeatingStatus.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SD_SeatingStatus.Frame(DISPLAY))

        if Interface.SD_QuickAccess.Update():
            RECTS.append(Interface.SD_QuickAccess.Frame(DISPLAY))

        #if Interface.SD_QR.Update():
        #    RECTS.append(Interface.SD_QR.Frame(DISPLAY))

        # 좌석표 렌더링
        if Interface.ST_SeatDisplay.Update(TICK):
            RECTS.append(Interface.ST_SeatDisplay.Frame(DISPLAY))

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
        
        # StudentInfo
        if Interface.ST_StudentInfo.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.ST_StudentInfo.Frame(DISPLAY))

        # 버튼 렌더링
        if Interface.ID_PasswordButton.Update(TICK):
            RECTS.append(Interface.ID_PasswordButton.Frame(DISPLAY))

        if Interface.BTN_Cancel.Update():
            RECTS.append(Interface.BTN_Cancel.Frame(DISPLAY))

        if Interface.BTN_Move.Update(TICK):
            RECTS.append(Interface.BTN_Move.Frame(DISPLAY))

        if Interface.BTN_Checkout.Update(TICK):
            RECTS.append(Interface.BTN_Checkout.Frame(DISPLAY))

        # 현재 미디어 업데이트
        if Interface.OT_CurrentMedia.Update():
            RECTS.append(Interface.OT_CurrentMedia.Frame(DISPLAY))


    
    def On_Layer(self, ANIMATION_OFFSET, TICK, LAYER, RECTS):
        
        if Interface.LY_StudentInfo.Update():
            RECTS.append(Interface.LY_StudentInfo.Frame(LAYER))

        if Interface.LY_Notice.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.LY_Notice.Frame(LAYER))



    # 전체 그림
    def Draw(self, SURFACE):

        SURFACE.fill(Styles.SPRLIGHTGRAY)

        # 화면 오른쪽 요소 렌더링
        Interface.SD_DateTime.Frame(SURFACE)
        Interface.SD_DietAndSchedule.Frame(SURFACE)
        Interface.SD_SeatingStatus.Frame(SURFACE)
        Interface.SD_QuickAccess.Frame(SURFACE)

        #Interface.SD_QR.Frame(SURFACE)

        # 좌석표 렌더링
        Interface.ST_SeatDisplay.Frame(SURFACE)

        # 학번 입력란 그룹 렌더링
        Interface.ID_InstructionText.Frame(SURFACE)

        Interface.ID_KeyInstruction.Frame(SURFACE)
            
        Interface.ID_IdInputDialog.Frame(SURFACE)
        
        # StudentInfo
        Interface.ST_StudentInfo.Frame(SURFACE)

        # 버튼 렌더링
        Interface.ID_PasswordButton.Frame(SURFACE)

        Interface.BTN_Cancel.Frame(SURFACE)

        Interface.BTN_Move.Frame(SURFACE)

        Interface.BTN_Checkout.Frame(SURFACE)

        # 현재 미디어 업데이트
        Interface.OT_CurrentMedia.Frame(SURFACE)

        # 로고
        SURFACE.blit(MainScene.LogoImage, (1644, 985))


    
    def UpdateSeats(self):
        """ 좌석 데이터/인터페이스 처리 """
        try:
            Interface.ST_SeatDisplay.updateSeatSurf()
        except SeatsDataVerifyError as e:
            logging.error(e, "좌석 데이터를 처리하는 도중 오류가 발생하였습니다.", True)



    def On_Update(self, ANIMATION_OFFSET, TICK):
        
        ## 미등록 이용자 단계 타이밍 계산 ##
        if self.InteractionStep == 5:
            
            if SceneManager.SCENE_TIME > 1000:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                self.InteractionStep = 0
                SceneManager.SCENE_TIME = 0

            if SceneManager.SCENE_TIME > 800 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 850 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 900 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 950 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

        ## 미디어 표시 ##
        if self.InteractionStep == 0 and ChairyData.CURRENT_MEDIA.Playing:
            if ChairyData.CURRENT_MEDIA.Updated:
                Interface.OT_CurrentMedia.Render()

            if Interface.OT_CurrentMedia.Init and Interface.OT_CurrentMedia.Y != 955:
                Interface.OT_CurrentMedia.Animate_Y(955, 1.25, ANIMATION_OFFSET)
        
        ## 미디어 숨기기 ##
        else:
            if Interface.OT_CurrentMedia.Y != 1080:
                Interface.OT_CurrentMedia.AnimateSpdUp_Y(False, 940, 1080, 2.25, ANIMATION_OFFSET)

        ## 빠른 접근 버튼 ##
        if self.InteractionStep != 0 and Interface.SD_QuickAccess.Enabled:
            Interface.SD_QuickAccess.disable()

        if self.InteractionStep == 0 and not Interface.SD_QuickAccess.Enabled:
            Interface.SD_QuickAccess.enable()

        ## 유휴 상태 ##
        if self.InteractionStep in (1, 2, 3, 4, 6, 13, 18):
            MainScene.IdleTime += TICK

            if MainScene.IdleTime > 30000:

                # 경고 메시지 표시
                if not Interface.LY_Notice.Show:
                    Interface.LY_Notice.show_Idle1()

                # 유휴 초기화
                if Interface.LY_Notice.Idle_Reset:
                    Interface.LY_Notice.hide()
                    self.NotIdle()

                    if self.InteractionStep <= 4:
                        Interface.ID_IdInputDialog.StudentId[0] = '-'
                        Interface.ID_IdInputDialog.text1()
                        if Interface.ID_IdInputDialog.StudentId[1] != '-':
                            Interface.ID_IdInputDialog.StudentId[1] = '-'
                            Interface.ID_IdInputDialog.text2()
                        if Interface.ID_IdInputDialog.StudentId[2] != '-':
                            Interface.ID_IdInputDialog.StudentId[2] = '-'
                            Interface.ID_IdInputDialog.text3()
                        if Interface.ID_IdInputDialog.StudentId[3] != '-':
                            Interface.ID_IdInputDialog.StudentId[3] = '-'
                            Interface.ID_IdInputDialog.text4()
                        self.InteractionStep = 0

                    elif self.InteractionStep == 6:
                        SceneManager.SCENE_TIME = 0
                        self.InteractionStep = 8
                        Interface.LY_StudentInfo.hide()
                        Interface.ST_SeatDisplay.hide()
                        Interface.ST_StudentInfo.hide()

                    elif self.InteractionStep == 13:
                        self.InteractionStep = 14
                        Interface.LY_StudentInfo.hide()
                        Interface.ID_KeyInstruction.wait()
                        Interface.ST_SeatDisplay.hide()
                        SceneManager.SCENE_TIME = 0

                    elif self.InteractionStep == 18:
                        SceneManager.SCENE_TIME = 0
                        ChairyData.CURRENT_STUDENT.save()
                        ChairyData.CURRENT_STUDENT = None
                        self.InteractionStep = 19
                        Interface.LY_StudentInfo.hide()
                        Interface.ST_SeatDisplay.hide()


        ## 이외의 애니메이션 연산 ##

        # 학번 입력 + 미등록 이용자 단계
        if self.InteractionStep < 6:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
                
        # 자리 선택 단계
        elif self.InteractionStep == 6:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 118, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME < 250:
                if SceneManager.SCENE_TIME > 100 and Interface.ID_KeyInstruction._Use != 0:
                    Interface.ID_InstructionText.set("좌석을 선택합니다", Styles.BLACK)
                    Interface.ID_KeyInstruction.useMouse()

            else:
                Interface.ID_PasswordButton.Animate_Y(877, 1.0, ANIMATION_OFFSET)

                if Interface.ID_PasswordButton.Y < 980:
                    Interface.BTN_Cancel.Animate_Y(970, 1.0, ANIMATION_OFFSET)

        # 단일 지우기 애니메이션
        elif self.InteractionStep == 7:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 430, 1.0, ANIMATION_OFFSET)
            else:
                self.ID_Group_Y = AnimateSpdUp(False, self.ID_Group_Y, 116, 432, 2.3, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, ANIMATION_OFFSET)
            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)

            if self.ID_Group_Y > 400:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                Interface.ID_KeyInstruction.useKeypad()
                self.InteractionStep = 3

        # 전체 지우기 애니메이션
        elif self.InteractionStep == 8:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
            else:
                self.ID_Group_Y = AnimateSpdUp(False, self.ID_Group_Y, 116, 432, 2.3, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, ANIMATION_OFFSET)
            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                self.InteractionStep = 0
                SceneManager.SCENE_TIME = 0

            if SceneManager.SCENE_TIME > 0 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 50 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 100 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 150 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

        # 일반 이용자 입실 완료
        elif self.InteractionStep == 9:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
            else:
                self.ID_Group_Y = AnimateSpdUp(False, self.ID_Group_Y, 116, 432, 2.3, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(True, 970, 1080, 4.0, ANIMATION_OFFSET)
            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 1300:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                self.InteractionStep = 0
                SceneManager.SCENE_TIME = 0

            if SceneManager.SCENE_TIME > 1100 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 1150 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 1200 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 1250 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

        # 지정석 이용자 입실 완료 1
        elif self.InteractionStep == 10:
            self.ID_Group_Y = Animate(self.ID_Group_Y, 118, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 2000:
                Interface.ST_StudentInfo.hide()
                self.InteractionStep = 11
                SceneManager.SCENE_TIME = 0
                Interface.LY_StudentInfo.hide()

        # 지정석 이용자 입실 완료 2
        elif self.InteractionStep == 11:

            if SceneManager.SCENE_TIME > 200 and Interface.ST_StudentInfo.Y > 450:
                if self.ID_Group_Y != 432:
                    self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
                else:
                    self.InteractionStep = 12
                    SceneManager.SCENE_TIME = 0
                    Interface.LY_StudentInfo.hide()

        # 지정석 이용자 입실 완료 3
        elif self.InteractionStep == 12:

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                Interface.ST_SeatDisplay.hide()
                self.InteractionStep = 0
                SceneManager.SCENE_TIME = 0

            if SceneManager.SCENE_TIME > 0 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 50 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 100 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 150 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

        # 퇴실/이동 선택
        elif self.InteractionStep == 13:
            
            if self.ID_Group_Y != 313:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 313, 1.0, ANIMATION_OFFSET)
            else:
                Interface.ID_KeyInstruction.useMouse()

            if SceneManager.SCENE_TIME > 0:
                Interface.BTN_Checkout.Animate_Y(556, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 80:
                Interface.BTN_Move.Animate_Y(631, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 160:
                Interface.BTN_Cancel.Animate_Y(706, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_PasswordButton.Animate_Y(877, 1.0, ANIMATION_OFFSET)

        # 퇴실/이동 취소
        elif self.InteractionStep in (14, 15):

            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)
            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 704, 1080, 2.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 30:
                Interface.BTN_Move.AnimateSpdUp_Y(False, 629, 1080, 2.0, ANIMATION_OFFSET)
            
            if SceneManager.SCENE_TIME > 60:
                Interface.BTN_Checkout.AnimateSpdUp_Y(False, 554, 1080, 2.0, ANIMATION_OFFSET)

            if self.InteractionStep == 14:
                if SceneManager.SCENE_TIME > 110 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                    Interface.ID_IdInputDialog.StudentId[0] = '-'
                    Interface.ID_IdInputDialog.text1()

                if SceneManager.SCENE_TIME > 160 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                    Interface.ID_IdInputDialog.StudentId[1] = '-'
                    Interface.ID_IdInputDialog.text2()

                if SceneManager.SCENE_TIME > 210 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                    Interface.ID_IdInputDialog.StudentId[2] = '-'
                    Interface.ID_IdInputDialog.text3()

                if SceneManager.SCENE_TIME > 260 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                    Interface.ID_IdInputDialog.StudentId[3] = '-'
                    Interface.ID_IdInputDialog.text4()

            if Interface.BTN_Checkout.Y == 1080 and Interface.ID_IdInputDialog.StudentId[3] == '-':
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                SceneManager.SCENE_TIME = 0

                if self.InteractionStep == 14:
                    self.InteractionStep = 0

                elif self.InteractionStep == 15:
                    self.InteractionStep = 3

        # 퇴실 완료
        elif self.InteractionStep == 16:

            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)
            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 704, 1080, 2.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 30:
                Interface.BTN_Move.AnimateSpdUp_Y(False, 629, 1080, 2.0, ANIMATION_OFFSET)
            
            if SceneManager.SCENE_TIME > 60:
                Interface.BTN_Checkout.AnimateSpdUp_Y(False, 554, 1080, 2.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 200:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 110 and Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 160 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 210 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 260 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

            if SceneManager.SCENE_TIME > 1200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                SceneManager.SCENE_TIME = 0
                self.InteractionStep = 0

        # 이동 단계 진입 애니메이션
        elif self.InteractionStep == 17:

            Interface.ID_PasswordButton.AnimateSpdUp_Y(False, 876, 1080, 4.0, ANIMATION_OFFSET)

            if Interface.BTN_Checkout.Alpha == 0. and Interface.BTN_Move.Alpha == 0. and Interface.ID_PasswordButton.Y >= 1080:
                Interface.ID_InstructionText.set("이동할 좌석을 선택합니다.", Styles.YELLOW)
                self.InteractionStep = 18
                Interface.LY_StudentInfo.hide()

        # 자리 이동 단계
        elif self.InteractionStep == 18:
            
            self.ID_Group_Y = Animate(self.ID_Group_Y, 388, 1.0, ANIMATION_OFFSET)
            Interface.BTN_Cancel.Animate_Y(631, 1.0, ANIMATION_OFFSET)

        # 이동 단계 취소
        elif self.InteractionStep == 19:
            
            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 600, 1080, 2.0, ANIMATION_OFFSET)

            Interface.BTN_Checkout.Reset()
            Interface.BTN_Move.Reset()

            if Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 50 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 100 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 150 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                SceneManager.SCENE_TIME = 0
                self.InteractionStep = 0

        # 이동 단계 학번 단일 지우기
        elif self.InteractionStep == 20:
            
            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            if Interface.BTN_Cancel.Y != 1080:
                Interface.BTN_Cancel.AnimateSpdUp_Y(False, 600, 1080, 2.0, ANIMATION_OFFSET)
            else:
                Interface.BTN_Cancel.Y = 1080
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                self.InteractionStep = 3

        # 이동 완료
        elif self.InteractionStep == 21:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 600, 1080, 2.0, ANIMATION_OFFSET)

            if Interface.ID_IdInputDialog.StudentId[0] != '-':
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.text1()

            if SceneManager.SCENE_TIME > 50 and Interface.ID_IdInputDialog.StudentId[1] != '-':
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.text2()

            if SceneManager.SCENE_TIME > 100 and Interface.ID_IdInputDialog.StudentId[2] != '-':
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.text3()

            if SceneManager.SCENE_TIME > 150 and Interface.ID_IdInputDialog.StudentId[3] != '-':
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()

            if SceneManager.SCENE_TIME > 1200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                SceneManager.SCENE_TIME = 0
                self.InteractionStep = 0
    


    def Event_KeyDown(self, KEY):

        self.NotIdle()

        if KEY == constants.K_F9 and self.InteractionStep == 0:
            Interface.SC_TopBar.Reset()
            from .transition import Transition
            Transition(SceneManager.Scenes['ExportDaily'])

        if KEY == constants.K_F12 and self.InteractionStep == 0:
            SceneManager.RESET = True
        
        if self.InteractionStep < 4:

            if KEY in (constants.K_KP0, constants.K_0):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '0'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP1, constants.K_1):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '1'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP2, constants.K_2):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '2'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP3, constants.K_3):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '3'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP4, constants.K_4):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '4'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP5, constants.K_5):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '5'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP6, constants.K_6):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '6'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP7, constants.K_7):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '7'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP8, constants.K_8):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '8'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY in (constants.K_KP9, constants.K_9):
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = '9'
                Interface.ID_IdInputDialog.text(self.InteractionStep)
                self.InteractionStep += 1
            elif KEY == constants.K_BACKSPACE and self.InteractionStep > 0:
                Interface.ID_IdInputDialog.StudentId[self.InteractionStep - 1] = '-'
                Interface.ID_IdInputDialog.text(self.InteractionStep - 1)
                self.InteractionStep -= 1
            elif KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                if self.InteractionStep > 0:
                    Interface.ID_IdInputDialog.StudentId[0] = '-'
                    Interface.ID_IdInputDialog.text1()
                    if Interface.ID_IdInputDialog.StudentId[1] != '-':
                        Interface.ID_IdInputDialog.StudentId[1] = '-'
                        Interface.ID_IdInputDialog.text2()
                    if Interface.ID_IdInputDialog.StudentId[2] != '-':
                        Interface.ID_IdInputDialog.StudentId[2] = '-'
                        Interface.ID_IdInputDialog.text3()
                    if Interface.ID_IdInputDialog.StudentId[3] != '-':
                        Interface.ID_IdInputDialog.StudentId[3] = '-'
                        Interface.ID_IdInputDialog.text4()
                    self.InteractionStep = 0
            elif ChairyData.CONFIGURATION.Alphabet:
                self.AlphabetInput(KEY)


            if self.InteractionStep == 4: # 학번 확인 및 비밀번호 확인

                id = ""
                for i in Interface.ID_IdInputDialog.StudentId:
                    id += i

                if id in ChairyData.STUDENTS: # 학번이 등록된 경우

                    ChairyData.CURRENT_STUDENT = ChairyData.STUDENTS[id]

                    # 비밀번호 확인
                    if ChairyData.CURRENT_STUDENT.hasPassword():
                        Password(1, self.ID_Group_Y, ChairyData.CURRENT_STUDENT)
                    
                    else:
                        self.InteractionStep = 4.5

                else:
                    Interface.ID_InstructionText.set("미등록된 학번입니다.", Styles.RED)
                    self.InteractionStep = 5
                    SceneManager.SCENE_TIME = 0
                    Interface.LY_StudentInfo.hide()


            if self.InteractionStep == 4.5: # InteractionStep 전환
                self.StudentInfo(ChairyData.CURRENT_STUDENT.StudentID)
        

        # 좌석 선택
        elif self.InteractionStep == 6:
            if KEY == constants.K_BACKSPACE:
                self.InteractionStep = 7
                Interface.LY_StudentInfo.hide()
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
            elif KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                SceneManager.SCENE_TIME = 0
                self.InteractionStep = 8
                Interface.LY_StudentInfo.hide()
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()

        # 퇴실/이동 선택
        elif self.InteractionStep == 13:
            if KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                self.InteractionStep = 14
                Interface.LY_StudentInfo.hide()
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                SceneManager.SCENE_TIME = 0
            elif KEY == constants.K_BACKSPACE:
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                self.InteractionStep = 15
                Interface.LY_StudentInfo.hide()
                SceneManager.SCENE_TIME = 0 
            elif KEY in (constants.K_KP_ENTER, constants.K_RETURN):
                ChairyData.ROOMDATA.CheckOut(ChairyData.CURRENT_STUDENT)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_InstructionText.set("퇴실 완료!", Styles.RED)
                Interface.ID_KeyInstruction.wait()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                self.InteractionStep = 16
                Interface.LY_StudentInfo.hide()
            elif KEY in (constants.K_MINUS, constants.K_KP_MINUS):
                if not ChairyData.CURRENT_STUDENT.SeatReserved:
                    self.UpdateSeats()
                    Interface.BTN_Move.hide()
                    Interface.BTN_Checkout.hide()
                    SceneManager.SCENE_TIME = 0
                    
                    self.InteractionStep = 17
                    Interface.LY_StudentInfo.hide()

        # 자리 이동 단계
        elif self.InteractionStep == 18:

            if KEY in (constants.K_ESCAPE, constants.K_KP_PERIOD):
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                self.InteractionStep = 19
                Interface.LY_StudentInfo.hide()
                Interface.ST_SeatDisplay.hide()

            elif KEY == constants.K_BACKSPACE:
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                self.InteractionStep = 20
                Interface.LY_StudentInfo.hide()
                Interface.ST_SeatDisplay.hide()


    def Event_MouseButtonDown(self, POS, BUTTON):

        if BUTTON != 1:
            return

        self.NotIdle()

        # 빠른 접근 버튼
        if self.InteractionStep == 0:
            Interface.SD_QuickAccess.MouseButtonDown(POS, BUTTON)

        # 자리 선택 단계
        elif self.InteractionStep == 6:
            Interface.ST_SeatDisplay.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)
            Interface.ID_PasswordButton.MouseButtonDown(POS, BUTTON)
            Interface.SD_QuickAccess.MouseButtonDown(POS, BUTTON)

        # 퇴실/이동 선택 단계
        elif self.InteractionStep == 13:
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Checkout.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Move.MouseButtonDown(POS, BUTTON)
            Interface.ID_PasswordButton.MouseButtonDown(POS, BUTTON)

        # 이동할 자리 선택 단계
        elif self.InteractionStep == 18:
            Interface.ST_SeatDisplay.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)


    def Event_MouseButtonUp(self, POS, BUTTON):

        if BUTTON != 1:
            return

        self.NotIdle()

        # 미디어 및 학번 일괄 채움, 빠른 접근 버튼
        if self.InteractionStep == 0:
            
            # 미디어
            if Interface.OT_CurrentMedia.MouseButtonUp(POS, BUTTON):
                Interface.SD_QuickAccess.disable()
                from .media import Media
                SceneManager.setSceneRaw(Media(), False)

            # 학번 일괄 채움
            id = Interface.ST_SeatDisplay.MouseMotion(POS)

            if id is not None:
                s = ChairyData.ROOMDATA.getStudent(id)

                if s is not None:
                    Interface.ID_IdInputDialog.StudentId[0] = s[0]
                    Interface.ID_IdInputDialog.text1()
                    Interface.ID_IdInputDialog.StudentId[1] = s[1]
                    Interface.ID_IdInputDialog.text2()
                    Interface.ID_IdInputDialog.StudentId[2] = s[2]
                    Interface.ID_IdInputDialog.text3()
                    Interface.ID_IdInputDialog.StudentId[3] = s[3]
                    Interface.ID_IdInputDialog.text4()
                    Interface.LY_StudentInfo.hide()
                    
                    if s in ChairyData.STUDENTS: # 학번이 등록된 경우

                        ChairyData.CURRENT_STUDENT = ChairyData.STUDENTS[s]

                        # 비밀번호 확인
                        if ChairyData.CURRENT_STUDENT.hasPassword():
                            Password(1, self.ID_Group_Y, ChairyData.CURRENT_STUDENT)
                        
                        else:

                            # 이용중
                            if ChairyData.CURRENT_STUDENT.CurrentSeat != None:
                                self.InteractionStep = 13
                                Interface.ID_InstructionText.set("퇴실하시겠습니까?", Styles.BLACK)
                                
                                Interface.LY_StudentInfo.hide()
                                if ChairyData.CURRENT_STUDENT.SeatReserved:
                                    Interface.BTN_Move.disable()
                                else:
                                    Interface.BTN_Move.enable()

                                Interface.ST_SeatDisplay.mySeat(ChairyData.CURRENT_STUDENT.CurrentSeat)
                                self.UpdateSeats()
                                Interface.ST_SeatDisplay.show()

                                Interface.BTN_Cancel.reset()
                                Interface.BTN_Move.reset()
                                Interface.BTN_Checkout.reset()

                                SceneManager.SCENE_TIME = 0

                            else:
                                Interface.ID_IdInputDialog.StudentId[0] = '-'
                                Interface.ID_IdInputDialog.text1()
                                Interface.ID_IdInputDialog.StudentId[1] = '-'
                                Interface.ID_IdInputDialog.text2()
                                Interface.ID_IdInputDialog.StudentId[2] = '-'
                                Interface.ID_IdInputDialog.text3()
                                Interface.ID_IdInputDialog.StudentId[3] = '-'
                                Interface.ID_IdInputDialog.text4()
                                self.InteractionStep = 0

                    else:
                        Interface.ID_IdInputDialog.StudentId[0] = '-'
                        Interface.ID_IdInputDialog.text1()
                        Interface.ID_IdInputDialog.StudentId[1] = '-'
                        Interface.ID_IdInputDialog.text2()
                        Interface.ID_IdInputDialog.StudentId[2] = '-'
                        Interface.ID_IdInputDialog.text3()
                        Interface.ID_IdInputDialog.StudentId[3] = '-'
                        Interface.ID_IdInputDialog.text4()
                        self.InteractionStep = 0

                # 학번 기입 안내
                elif collidepoint(POS[0], POS[1], 1002, 1045, POS):
                    Interface.LY_Notice.show_IdFirst()

            # 빠른 접근 버튼
            qab = Interface.SD_QuickAccess.MouseButtonUp(POS, BUTTON)

            if qab == 0:
                Interface.SC_TopBar.Reset()
                from .transition import Transition
                Transition(SceneManager.Scenes['ExportDaily'])
            
            elif qab == 1:
                Interface.LY_Notice.show_Developing()

            elif qab == 2:
                SceneManager.setScene('RoomdataLog')

            elif qab == 3:
                SceneManager.Restart()


        # 좌석 선택 단계
        elif self.InteractionStep == 6:

            # 취소 버튼을 눌렀을 시
            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                SceneManager.SCENE_TIME = 0
                self.InteractionStep = 8      
                Interface.LY_StudentInfo.hide()     
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
            
            # 비밀번호 설정
            if Interface.ID_PasswordButton.MouseButtonUp(POS, BUTTON):
                Password(0, self.ID_Group_Y, ChairyData.CURRENT_STUDENT)
            
            # 좌석 선택 시
            SeatIndex = Interface.ST_SeatDisplay.MouseButtonUp(POS, BUTTON)

            if SeatIndex != -1:
                s = ChairyData.ROOMDATA.Arrangement[SeatIndex][0] # 좌석 번호
                ChairyData.ROOMDATA.CheckIn(ChairyData.CURRENT_STUDENT, s)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ID_InstructionText.set("입실 완료!", Styles.BLUE)
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                self.InteractionStep = 9
                Interface.LY_StudentInfo.hide()


        # 퇴실/이동 선택 단계
        elif self.InteractionStep == 13:

            # 비밀번호 설정
            if Interface.ID_PasswordButton.MouseButtonUp(POS, BUTTON):
                Password(2, self.ID_Group_Y, ChairyData.CURRENT_STUDENT)
            
            # 취소 버튼
            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                self.InteractionStep = 14
                Interface.LY_StudentInfo.hide()
                SceneManager.SCENE_TIME = 0

            # 퇴실 버튼
            elif Interface.BTN_Checkout.MouseButtonUp(POS, BUTTON):
                ChairyData.ROOMDATA.CheckOut(ChairyData.CURRENT_STUDENT)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_InstructionText.set("퇴실 완료!", Styles.RED)
                Interface.ID_KeyInstruction.wait()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                self.InteractionStep = 16
                Interface.LY_StudentInfo.hide()

            # 좌석 이동
            elif Interface.BTN_Move.MouseButtonUp(POS, BUTTON):
                self.UpdateSeats()
                Interface.BTN_Move.hide()
                Interface.BTN_Checkout.hide()
                SceneManager.SCENE_TIME = 0
                
                self.InteractionStep = 17
                Interface.LY_StudentInfo.hide()

        # 이동할 자리 선택 단계
        elif self.InteractionStep == 18:

            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None

                self.InteractionStep = 19
                Interface.LY_StudentInfo.hide()
                Interface.ST_SeatDisplay.hide()

            SeatIndex = Interface.ST_SeatDisplay.MouseButtonUp(POS, BUTTON)

            if SeatIndex != -1:
                s = ChairyData.ROOMDATA.Arrangement[SeatIndex][0]
                ChairyData.ROOMDATA.Move(ChairyData.CURRENT_STUDENT, s)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ID_InstructionText.set("이동 완료!", Styles.BLUE)
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                self.InteractionStep = 21
                Interface.LY_StudentInfo.hide()


    def Event_MouseMotion(self, POS):

        self.NotIdle()

        # 미디어 및 빠른 접근 버튼
        if self.InteractionStep == 0:
            Interface.SD_QuickAccess.MouseMotion(POS)
            Interface.OT_CurrentMedia.MouseMotion(POS)

        # 자리 선택 단계
        elif self.InteractionStep == 6:
            Interface.BTN_Cancel.MouseMotion(POS)
            Interface.ID_PasswordButton.MouseMotion(POS)

        # 퇴실/이동 선택 단계
        elif self.InteractionStep == 13:
            Interface.BTN_Cancel.MouseMotion(POS)
            Interface.BTN_Checkout.MouseMotion(POS)
            Interface.BTN_Move.MouseMotion(POS)
            Interface.ID_PasswordButton.MouseMotion(POS)

        # 자리 이동 단계
        elif self.InteractionStep == 18:
            Interface.BTN_Cancel.MouseMotion(POS)

        # 마우스 호버
        if self.InteractionStep in (0, 1, 2, 3):
            Interface.LY_StudentInfo.MouseMotion(POS)
            id = Interface.ST_SeatDisplay.MouseMotion(POS)

            if id != MainScene.StudentHoverID:

                if id is None:
                    Interface.LY_StudentInfo.hide()

                else:
                    s: StudentData = ChairyData.STUDENTS.get(ChairyData.ROOMDATA.getStudent(id), None)

                    if s is not None:
                        Interface.LY_StudentInfo.render(s.StudentID, s.Name, s.LastChkIn)
                        Interface.LY_StudentInfo.show()

                MainScene.StudentHoverID = id
    

    def AlphabetInput(self, KEY: constants):
        """ 알파벳 입력 처리, **매개변수로 입력된 키 값을 받음.** """    

        def input(a: str):
            Interface.ID_IdInputDialog.StudentId[self.InteractionStep] = a
            Interface.ID_IdInputDialog.text(self.InteractionStep)
            self.InteractionStep += 1

        if KEY == constants.K_a:
            input('A')
        elif KEY == constants.K_b:
            input('B')
        elif KEY == constants.K_c:
            input('C')
        elif KEY == constants.K_d:
            input('D')
        elif KEY == constants.K_e:
            input('E')
        elif KEY == constants.K_f:
            input('F')
        elif KEY == constants.K_g:
            input('G')
        elif KEY == constants.K_h:
            input('H')
        elif KEY == constants.K_i:
            input('I')
        elif KEY == constants.K_j:
            input('J')
        elif KEY == constants.K_k:
            input('K')
        elif KEY == constants.K_l:
            input('L')
        elif KEY == constants.K_m:
            input('M')
        elif KEY == constants.K_n:
            input('N')
        elif KEY == constants.K_o:
            input('O')
        elif KEY == constants.K_p:
            input('P')
        elif KEY == constants.K_q:
            input('Q')
        elif KEY == constants.K_r:
            input('R')
        elif KEY == constants.K_s:
            input('S')
        elif KEY == constants.K_t:
            input('T')
        elif KEY == constants.K_u:
            input('U')
        elif KEY == constants.K_v:
            input('V')
        elif KEY == constants.K_w:
            input('W')
        elif KEY == constants.K_x:
            input('X')
        elif KEY == constants.K_y:
            input('Y')
        elif KEY == constants.K_z:
            input('Z')
        elif KEY == constants.K_SPACE:
            input('_')


    def NotIdle(self):
        if Interface.LY_Notice.Index in (0, 1, 3) and Interface.LY_Notice.Show:
            Interface.LY_Notice.hide()
        MainScene.IdleTime = 0


    def StudentInfo(self, id: str):
        # 이용중
        if ChairyData.CURRENT_STUDENT.CurrentSeat != None:
            self.InteractionStep = 13
            Interface.ID_InstructionText.set("퇴실하시겠습니까?", Styles.BLACK)
            
            Interface.LY_StudentInfo.hide()
            if ChairyData.CURRENT_STUDENT.SeatReserved:
                Interface.BTN_Move.disable()
            else:
                Interface.BTN_Move.enable()

            Interface.ST_SeatDisplay.mySeat(ChairyData.CURRENT_STUDENT.CurrentSeat)
            self.UpdateSeats()
            Interface.ST_SeatDisplay.show()

            Interface.BTN_Cancel.reset()
            Interface.BTN_Move.reset()
            Interface.BTN_Checkout.reset()

            SceneManager.SCENE_TIME = 0
            return

        ## 입실
        Interface.ST_StudentInfo.info(id)
        Interface.ST_StudentInfo.show()

        # 지정석 입실
        if ChairyData.CURRENT_STUDENT.SeatReserved:
            self.InteractionStep = 10
            Interface.ID_InstructionText.set("지정석 입실 완료!", Styles.BLUE)
            Interface.ID_KeyInstruction.wait()
            
            Interface.LY_StudentInfo.hide()

            ChairyData.ROOMDATA.CheckInReserved(ChairyData.CURRENT_STUDENT)
            self.UpdateSeats()
            Interface.SD_SeatingStatus.RoomUpdated()
            ChairyData.CURRENT_STUDENT.save()
            ChairyData.CURRENT_STUDENT = None

        # 일반 입실
        else:
            self.InteractionStep = 6
            
            Interface.LY_StudentInfo.hide()

        SceneManager.SCENE_TIME = 0
        Interface.ST_SeatDisplay.mySeat(None)
        Interface.ST_SeatDisplay.show()