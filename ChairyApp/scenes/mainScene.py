
from ..interface import Interface, Scene, SceneManager, Styles, SeatsDataVerifyError
from ..chairyData import ChairyData
from pygame import constants
from ..Logging import LoggingManager as logging

from ..optimization.animation import Animate



class MainScene(Scene):
    """
    ### MainScene
    
    가장 주요한 장면이며, 학번 입력과 입퇴실 및 이동 과정을 관장하는 장면.
    """

    InteractionStep : int = 0 # Static
    # 0 ~ 3: 학번 입력
    # 4: StudentInfo 확인
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


    @staticmethod
    def Init():
        SceneManager.MainScene = MainScene()



    def __init__(self):
        self.ID_Group_Y = 432

    
    def On_Init(self, DISPLAY):
        DISPLAY.fill(Styles.SPRLIGHTGRAY)
        self.ID_Group_Y = 432

        Interface.SD_DateTime.Reset()
        Interface.SD_DietAndSchedule.Reset()
        Interface.SD_SeatingStatus.Reset()

        Interface.ID_InstructionText.Reset(300, Styles.SANS_H4, "학번을 입력합니다", Styles.BLACK)
        Interface.ID_IdInputDialog.Reset()
        Interface.ID_KeyInstruction.Reset()

        Interface.ST_SeatDisplay.Reset()
        Interface.ST_StudentInfo.Reset()

        Interface.BTN_Cancel.Reset()
        Interface.BTN_Checkout.Reset()
        Interface.BTN_Move.Reset()

        Interface.OT_CurrentMedia.Reset()



    def On_Render(self, ANIMATION_OFFSET, TICK, DISPLAY, RECTS):
        
        # 화면 오른쪽 요소 렌더링
        if Interface.SD_DateTime.Update():
            RECTS.append(Interface.SD_DateTime.Frame(DISPLAY))

        if Interface.SD_DietAndSchedule.Update():
            RECTS.append(Interface.SD_DietAndSchedule.Frame(DISPLAY))

        if Interface.SD_SeatingStatus.Update(ANIMATION_OFFSET):
            RECTS.append(Interface.SD_SeatingStatus.Frame(DISPLAY))

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
        if Interface.BTN_Cancel.Update():
            RECTS.append(Interface.BTN_Cancel.Frame(DISPLAY))

        if Interface.BTN_Move.Update(TICK):
            RECTS.append(Interface.BTN_Move.Frame(DISPLAY))

        if Interface.BTN_Checkout.Update(TICK):
            RECTS.append(Interface.BTN_Checkout.Frame(DISPLAY))

        # 현재 미디어 업데이트
        if Interface.OT_CurrentMedia.Update():
            RECTS.append(Interface.OT_CurrentMedia.Frame(DISPLAY))



    # 전체 그림
    def Draw(self, SURFACE):

        SURFACE.fill(Styles.SPRLIGHTGRAY)

        # 화면 오른쪽 요소 렌더링
        Interface.SD_DateTime.Frame(SURFACE)
        Interface.SD_DietAndSchedule.Frame(SURFACE)

        Interface.SD_SeatingStatus.Frame(SURFACE)

        #Interface.SD_QR.Frame(SURFACE)

        # 좌석표 렌더더링
        Interface.ST_SeatDisplay.Frame(SURFACE)

        # 학번 입력란 그룹 렌더링
        Interface.ID_InstructionText.Frame(SURFACE)

        Interface.ID_KeyInstruction.Frame(SURFACE)
            
        Interface.ID_IdInputDialog.Frame(SURFACE)
        
        # StudentInfo
        Interface.ST_StudentInfo.Frame(SURFACE)

        # 버튼 렌더링
        Interface.BTN_Cancel.Frame(SURFACE)

        Interface.BTN_Move.Frame(SURFACE)

        Interface.BTN_Checkout.Frame(SURFACE)

        # 현재 미디어 업데이트
        Interface.OT_CurrentMedia.Frame(SURFACE)


    
    def UpdateSeats(self):
        """ 좌석 데이터/인터페이스 처리 """
        try:
            Interface.ST_SeatDisplay.updateSeatSurf()
        except SeatsDataVerifyError as e:
            logging.error(e, "좌석 데이터를 처리하는 도중 오류가 발생하였습니다.", True)



    def On_Update(self, ANIMATION_OFFSET, TICK):
        
        ## 미등록 이용자 단계 타이밍 계산 ##
        if MainScene.InteractionStep == 5:
            
            if SceneManager.SCENE_TIME > 1000:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                MainScene.InteractionStep = 0
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
        if MainScene.InteractionStep == 0 and ChairyData.CURRENT_MEDIA.Playing:
            if ChairyData.CURRENT_MEDIA.Updated:
                Interface.OT_CurrentMedia.Render()

            if Interface.OT_CurrentMedia.Init and Interface.OT_CurrentMedia.Y != 955:
                Interface.OT_CurrentMedia.Animate_Y(955, 1.25, ANIMATION_OFFSET)
        
        ## 미디어 숨기기 ##
        else:
            if Interface.OT_CurrentMedia.Y != 1080:
                Interface.OT_CurrentMedia.AnimateSpdUp_Y(False, 940, 1080, 2.25, ANIMATION_OFFSET)


        ## 이외의 애니메이션 연산 ##

        # 학번 입력 + 미등록 이용자 단계
        if MainScene.InteractionStep < 6:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
                
        # 자리 선택 단계
        elif MainScene.InteractionStep == 6:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 150, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME < 250:
                if SceneManager.SCENE_TIME > 100 and Interface.ID_KeyInstruction._Use != 0:
                    Interface.ID_InstructionText.set("좌석을 선택합니다", Styles.BLACK)
                    Interface.ID_KeyInstruction.useMouse()

            else:
                Interface.BTN_Cancel.Animate_Y(970, 1.0, ANIMATION_OFFSET)

        # 단일 지우기 애니메이션
        elif MainScene.InteractionStep == 7:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 430, 1.0, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, ANIMATION_OFFSET)

            if self.ID_Group_Y > 400:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                Interface.ID_KeyInstruction.useKeypad()
                MainScene.InteractionStep = 3

        # 전체 지우기 애니메이션
        elif MainScene.InteractionStep == 8:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                MainScene.InteractionStep = 0
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
        elif MainScene.InteractionStep == 9:
            if Interface.ST_StudentInfo.Y > 450:
                self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            Interface.BTN_Cancel.AnimateSpdUp_Y(True, 970, 1080, 4.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 1300:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                MainScene.InteractionStep = 0
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
        elif MainScene.InteractionStep == 10:
            self.ID_Group_Y = Animate(self.ID_Group_Y, 150, 1.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 2000:
                Interface.ST_StudentInfo.hide()
                MainScene.InteractionStep = 11
                SceneManager.SCENE_TIME = 0

        # 지정석 이용자 입실 완료 2
        elif MainScene.InteractionStep == 11:

            if SceneManager.SCENE_TIME > 200 and Interface.ST_StudentInfo.Y > 450:
                if self.ID_Group_Y != 432:
                    self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)
                else:
                    MainScene.InteractionStep = 12
                    SceneManager.SCENE_TIME = 0

        # 지정석 이용자 입실 완료 3
        elif MainScene.InteractionStep == 12:

            if SceneManager.SCENE_TIME > 200:
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                Interface.ST_SeatDisplay.hide()
                MainScene.InteractionStep = 0
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
        elif MainScene.InteractionStep == 13:
            
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

        # 퇴실/이동 취소
        elif MainScene.InteractionStep in (14, 15):

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 704, 1080, 2.0, ANIMATION_OFFSET)

            if SceneManager.SCENE_TIME > 30:
                Interface.BTN_Move.AnimateSpdUp_Y(False, 629, 1080, 2.0, ANIMATION_OFFSET)
            
            if SceneManager.SCENE_TIME > 60:
                Interface.BTN_Checkout.AnimateSpdUp_Y(False, 554, 1080, 2.0, ANIMATION_OFFSET)

            if MainScene.InteractionStep == 14:
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

                if MainScene.InteractionStep == 14:
                    MainScene.InteractionStep = 0

                elif MainScene.InteractionStep == 15:
                    MainScene.InteractionStep = 3

        # 퇴실 완료
        elif MainScene.InteractionStep == 16:

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
                MainScene.InteractionStep = 0

        # 이동 단계 진입 애니메이션
        elif MainScene.InteractionStep == 17:

            if Interface.BTN_Checkout.Alpha == 0. and Interface.BTN_Move.Alpha == 0.:
                Interface.ID_InstructionText.set("이동할 좌석을 선택합니다.", Styles.YELLOW)
                MainScene.InteractionStep = 18

        # 자리 이동 단계
        elif MainScene.InteractionStep == 18:
            
            self.ID_Group_Y = Animate(self.ID_Group_Y, 388, 1.0, ANIMATION_OFFSET)
            Interface.BTN_Cancel.Animate_Y(631, 1.0, ANIMATION_OFFSET)

        # 이동 단계 취소
        elif MainScene.InteractionStep == 19:
            
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
                MainScene.InteractionStep = 0

        # 이동 단계 학번 단일 지우기
        elif MainScene.InteractionStep == 20:
            
            self.ID_Group_Y = Animate(self.ID_Group_Y, 432, 1.0, ANIMATION_OFFSET)

            if Interface.BTN_Cancel.Y != 1080:
                Interface.BTN_Cancel.AnimateSpdUp_Y(False, 600, 1080, 2.0, ANIMATION_OFFSET)
            else:
                Interface.BTN_Cancel.Y = 1080
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                Interface.ID_InstructionText.set("학번을 입력합니다", Styles.BLACK)
                Interface.ID_KeyInstruction.useKeypad()
                MainScene.InteractionStep = 3

        # 이동 완료
        elif MainScene.InteractionStep == 21:

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
                MainScene.InteractionStep = 0
    


    def Event_KeyDown(self, KEY):

        if KEY == constants.K_F9 and MainScene.InteractionStep == 0:
            Interface.SC_TopBar.Reset()
            from .transition import Transition
            Transition(SceneManager.ExportDaily)
        
        if MainScene.InteractionStep < 4:

            if KEY in (constants.K_KP0, constants.K_0):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '0'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP1, constants.K_1):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '1'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP2, constants.K_2):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '2'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP3, constants.K_3):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '3'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP4, constants.K_4):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '4'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP5, constants.K_5):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '5'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP6, constants.K_6):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '6'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP7, constants.K_7):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '7'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP8, constants.K_8):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '8'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY in (constants.K_KP9, constants.K_9):
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = '9'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
                MainScene.InteractionStep += 1
            elif KEY == constants.K_BACKSPACE and MainScene.InteractionStep > 0:
                Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep - 1] = '-'
                Interface.ID_IdInputDialog.text(MainScene.InteractionStep - 1)
                MainScene.InteractionStep -= 1
            elif KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                if MainScene.InteractionStep > 0:
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
                    MainScene.InteractionStep = 0
            elif ChairyData.CONFIGURATION.Alphabet:
                self.AlphabetInput(KEY)


            if MainScene.InteractionStep == 4: # 학번 입력 및 InteractionStep 전환

                id = ""
                for i in Interface.ID_IdInputDialog.StudentId:
                    id += i
                
                if id in ChairyData.STUDENTS: # 학번이 등록된 경우

                    ChairyData.CURRENT_STUDENT = ChairyData.STUDENTS[id]

                    # 이용중
                    if ChairyData.CURRENT_STUDENT.CurrentSeat != None:
                        MainScene.InteractionStep = 13
                        Interface.ID_InstructionText.set("퇴실하시겠습니까?", Styles.BLACK)
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
                        MainScene.InteractionStep = 10
                        Interface.ID_InstructionText.set("지정석 입실 완료!", Styles.BLUE)
                        Interface.ID_KeyInstruction.wait()

                        ChairyData.ROOMDATA.CheckInReserved(ChairyData.CURRENT_STUDENT)
                        logging.info("지정석 입실 처리 -> " + ChairyData.CURRENT_STUDENT.StudentID + " : " 
                                                + ChairyData.CURRENT_STUDENT.Name + " -> " + ChairyData.STUDENTS[id].ReservedSeat)
                        self.UpdateSeats()
                        Interface.SD_SeatingStatus.RoomUpdated()
                        ChairyData.CURRENT_STUDENT.save()
                        ChairyData.CURRENT_STUDENT = None

                    # 일반 입실
                    else:
                        MainScene.InteractionStep = 6

                    SceneManager.SCENE_TIME = 0
                    Interface.ST_SeatDisplay.mySeat(None)
                    Interface.ST_SeatDisplay.show()

                else:
                    Interface.ID_InstructionText.set("미등록된 학번입니다.", Styles.RED)
                    MainScene.InteractionStep = 5
                    SceneManager.SCENE_TIME = 0
        
        # 좌석 선택
        elif MainScene.InteractionStep == 6:
            if KEY == constants.K_BACKSPACE:
                MainScene.InteractionStep = 7
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
            elif KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                SceneManager.SCENE_TIME = 0
                MainScene.InteractionStep = 8
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()

        # 퇴실/이동 선택
        elif MainScene.InteractionStep == 13:
            if KEY in (constants.K_KP_PERIOD, constants.K_ESCAPE):
                MainScene.InteractionStep = 14
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                SceneManager.SCENE_TIME = 0
            elif KEY == constants.K_BACKSPACE:
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text4()
                MainScene.InteractionStep = 15
                SceneManager.SCENE_TIME = 0 
            elif KEY in (constants.K_KP_ENTER, constants.K_RETURN):
                ChairyData.ROOMDATA.CheckOut(ChairyData.CURRENT_STUDENT)
                logging.info("퇴실 처리 -> " + ChairyData.CURRENT_STUDENT.StudentID + " : " + ChairyData.CURRENT_STUDENT.Name)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_InstructionText.set("퇴실 완료!", Styles.RED)
                Interface.ID_KeyInstruction.wait()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                MainScene.InteractionStep = 16
            elif KEY in (constants.K_MINUS, constants.K_KP_MINUS):
                if not ChairyData.CURRENT_STUDENT.SeatReserved:
                    self.UpdateSeats()
                    Interface.BTN_Move.hide()
                    Interface.BTN_Checkout.hide()
                    SceneManager.SCENE_TIME = 0
                    
                    MainScene.InteractionStep = 17

        # 자리 이동 단계
        elif MainScene.InteractionStep == 18:

            if KEY in (constants.K_ESCAPE, constants.K_KP_PERIOD):
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                MainScene.InteractionStep = 19
                Interface.ST_SeatDisplay.hide()

            elif KEY == constants.K_BACKSPACE:
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                MainScene.InteractionStep = 20
                Interface.ST_SeatDisplay.hide()


    def Event_MouseButtonDown(self, POS, BUTTON):

        # 자리 선택 단계
        if MainScene.InteractionStep == 6:
            Interface.ST_SeatDisplay.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)

        # 퇴실/이동 선택 단계
        elif MainScene.InteractionStep == 13:
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Checkout.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Move.MouseButtonDown(POS, BUTTON)

        # 이동할 자리 선택 단계
        elif MainScene.InteractionStep == 18:
            Interface.ST_SeatDisplay.MouseButtonDown(POS, BUTTON)
            Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)


    def Event_MouseButtonUp(self, POS, BUTTON):

        # 미디어
        if MainScene.InteractionStep == 0:
            
            if Interface.OT_CurrentMedia.MouseButtonUp(POS, BUTTON):
                from .media import Media
                SceneManager.CURRENT_SCENE = Media()
                SceneManager.SCENE_TIME = 0

        # 좌석 선택 단계
        elif MainScene.InteractionStep == 6:

            # 취소 버튼을 눌렀을 시
            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                SceneManager.SCENE_TIME = 0
                MainScene.InteractionStep = 8           
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
            
            # 좌석 선택 시
            SeatIndex = Interface.ST_SeatDisplay.MouseButtonUp(POS, BUTTON)

            if SeatIndex != -1:
                s = ChairyData.ROOMDATA.Arrangement[SeatIndex][0]
                ChairyData.ROOMDATA.CheckIn(ChairyData.CURRENT_STUDENT, s)
                logging.info("입실 처리 -> " + ChairyData.CURRENT_STUDENT.StudentID + " : " + ChairyData.CURRENT_STUDENT.Name + " -> "
                "" + ChairyData.ROOMDATA.Arrangement[SeatIndex][0])
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ID_InstructionText.set("입실 완료!", Styles.BLUE)
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                Interface.ST_StudentInfo.hide()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                MainScene.InteractionStep = 9


        # 퇴실/이동 선택 단계
        elif MainScene.InteractionStep == 13:
            
            # 취소 버튼
            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                MainScene.InteractionStep = 14
                SceneManager.SCENE_TIME = 0

            # 퇴실 버튼
            elif Interface.BTN_Checkout.MouseButtonUp(POS, BUTTON):
                ChairyData.ROOMDATA.CheckOut(ChairyData.CURRENT_STUDENT)
                logging.info("퇴실 처리 -> " + ChairyData.CURRENT_STUDENT.StudentID + " : " + ChairyData.CURRENT_STUDENT.Name)
                self.UpdateSeats()
                Interface.SD_SeatingStatus.RoomUpdated()
                Interface.ST_SeatDisplay.hide()
                Interface.ID_InstructionText.set("퇴실 완료!", Styles.RED)
                Interface.ID_KeyInstruction.wait()
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None
                
                MainScene.InteractionStep = 16

            # 좌석 이동
            elif Interface.BTN_Move.MouseButtonUp(POS, BUTTON):
                self.UpdateSeats()
                Interface.BTN_Move.hide()
                Interface.BTN_Checkout.hide()
                SceneManager.SCENE_TIME = 0
                
                MainScene.InteractionStep = 17

        # 이동할 자리 선택 단계
        elif MainScene.InteractionStep == 18:

            if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):
                SceneManager.SCENE_TIME = 0
                ChairyData.CURRENT_STUDENT.save()
                ChairyData.CURRENT_STUDENT = None

                MainScene.InteractionStep = 19
                Interface.ST_SeatDisplay.hide()

            SeatIndex = Interface.ST_SeatDisplay.MouseButtonUp(POS, BUTTON)

            if SeatIndex != -1:
                s = ChairyData.ROOMDATA.Arrangement[SeatIndex][0]
                logging.info("자리 이동 처리 -> " + ChairyData.CURRENT_STUDENT.StudentID + " : " + ChairyData.CURRENT_STUDENT.Name + " -> "
                " [" + ChairyData.CURRENT_STUDENT.CurrentSeat + "]번에서 [" + ChairyData.ROOMDATA.Arrangement[SeatIndex][0] + "]번으로 이동")
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
                
                MainScene.InteractionStep = 21


    def Event_MouseMotion(self, POS):

        # 미디어
        if MainScene.InteractionStep == 0:
            Interface.OT_CurrentMedia.MouseMotion(POS)

        # 자리 선택 단계
        elif MainScene.InteractionStep == 6:
            Interface.BTN_Cancel.MouseMotion(POS)

        # 퇴실/이동 선택 단계
        elif MainScene.InteractionStep == 13:
            Interface.BTN_Cancel.MouseMotion(POS)
            Interface.BTN_Checkout.MouseMotion(POS)
            Interface.BTN_Move.MouseMotion(POS)

        # 자리 이동 단계
        elif MainScene.InteractionStep == 18:
            Interface.BTN_Cancel.MouseMotion(POS)
    
    

    def AlphabetInput(self, KEY: constants):
        """ 알파벳 입력 처리, **매개변수로 입력된 키 값을 받음.** """    

        def input(a: str):
            Interface.ID_IdInputDialog.StudentId[MainScene.InteractionStep] = a
            Interface.ID_IdInputDialog.text(MainScene.InteractionStep)
            MainScene.InteractionStep += 1

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