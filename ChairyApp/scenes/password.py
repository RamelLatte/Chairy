
from ..interface import Scene, SceneManager, Styles, Interface, ShrinkFadeAnimation, PasswordDialog, DeletePasswordButton
from ..chairyData import StudentData, ChairyData
from pygame import constants

from ..Logging import LoggingManager as logging
from ..optimization.animation import Animate



class Password(Scene):

    Delay: int

    New: bool
    CurrentPassword: str

    InteractionStep: int
    AnimationStep: int

    ID_Group_Y: int

    Student: StudentData

    SFA: ShrinkFadeAnimation
    PWD: PasswordDialog
    DPB: DeletePasswordButton


    def __init__(self, interactionStep: int, id_group_y: int, student: StudentData):
        """
        ### InteractionStep
        - **0:** 자리 선택 단계에서 비밀번호 설정 버튼을 눌렀을 경우
        - **1:** 비밀번호가 있는 학번이 입력된 경우
        - **2:** 퇴실 선택 단계에서 비밀번호 설정 버튼을 눌렀을 경우
        
        """
        logging.info(f'{student.StudentID} >> 비밀번호 입력 중')

        self.Identifier = 'Password'
        self.Delay = 0
        self.CurrentPassword = ''

        self.New = not student.hasPassword()

        self.Student = student

        self.InteractionStep = interactionStep
        self.Step = 0

        self.ID_Group_Y = id_group_y

        self.DPB = DeletePasswordButton()
        self.DPB.hide()

        self.SFA = None

        if interactionStep == 0:
            self.SFA = ShrinkFadeAnimation(Interface.ST_StudentInfo.X, Interface.ST_StudentInfo.Y, 
                                           Interface.ST_StudentInfo.getSurface(), 0.9, 1.25, Styles.SPRLIGHTGRAY)
            self.SFA.perform()
            if self.New:
                self.PWD = PasswordDialog(120, 525, '새로운 비밀번호 입력', True)
            else:
                self.PWD = PasswordDialog(120, 525, '기존 비밀번호 입력', False)

        elif interactionStep == 1:
            self.PWD = PasswordDialog(120, 525, '비밀번호 입력', False)

        elif interactionStep == 2:
            
            Interface.BTN_Move.Reset(123, 631)
            Interface.BTN_Checkout.Reset(123, 556)

            Interface.BTN_Move.hide()
            Interface.BTN_Checkout.hide()
            Interface.ID_PasswordButton.hide()

            if self.New:
                self.PWD = PasswordDialog(120, 525, '새로운 비밀번호 입력', True)
            else:
                self.PWD = PasswordDialog(120, 525, '기존 비밀번호 입력', False)

        Interface.ST_StudentInfo.Reset()
        Interface.ID_InstructionText.set('비밀번호 입력 중...', Styles.ORANGE)
        Interface.ID_KeyInstruction.useKeypad()

        self.PWD.freeze()
        Interface.ID_PasswordButton.hide()

        SceneManager.setSceneRaw(self)


    def On_Init(self, DISPLAY):
        ...

    
    def On_Layer(self, ANIMATION_OFFSET, TICK, LAYER, RECTS):
        if Interface.LY_Notice.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.LY_Notice.Frame(LAYER))


    def On_Update(self, ANIMATION_OFFSET, TICK):

        # 딜레이
        if self.Delay > 0:
            self.Delay -= TICK
            if self.Delay < 0:
                self.Delay = 0

        # 유휴 상태
        if SceneManager.SCENE_TIME > 30000:
            
            if not Interface.LY_Notice.Show:
                Interface.LY_Notice.show_Idle1()

            if Interface.LY_Notice.Idle_Reset:
                SceneManager.SCENE_TIME = 0
                Interface.LY_Notice.hide()
                self.Close()
        
        # 미디어
        if Interface.OT_CurrentMedia.Y != 1080:
            Interface.OT_CurrentMedia.AnimateSpdUp_Y(False, 940, 1080, 2.25, ANIMATION_OFFSET)

        # 자리 선택 단계에서 비밀번호 설정을 누른 경우
        if self.InteractionStep == 0:
            self.Animation_Step0(ANIMATION_OFFSET, TICK)

        # 비밀번호가 있는 학번이 입력된 경우
        elif self.InteractionStep == 1:
            self.Animation_Step1(ANIMATION_OFFSET, TICK)

        # 퇴실 선택 단계에서 비밀번호 설정을 누른 경우
        elif self.InteractionStep == 2:
            self.Animation_Step2(ANIMATION_OFFSET, TICK)


    def On_Layer(self, ANIMATION_OFFSET, TICK, LAYER, RECTS):

        if Interface.LY_Notice.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(Interface.LY_Notice.Frame(LAYER))


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

        # 미디어
        if Interface.OT_CurrentMedia.Update():
            RECTS.append(Interface.OT_CurrentMedia.Frame(DISPLAY))
        
        # StudentInfo
        #if Interface.ST_StudentInfo.Update(ANIMATION_OFFSET, TICK):
        #    RECTS.append(Interface.ST_StudentInfo.Frame(DISPLAY))

        # 비번 입력란 렌더링
        if self.PWD.Update(TICK):
            RECTS.append(self.PWD.Frame(DISPLAY))

        # 애니메이션 렌더링
        if self.SFA is not None and self.SFA.Update(ANIMATION_OFFSET, TICK):
            RECTS.append(self.SFA.Frame(DISPLAY))

        # 버튼 렌더링
        if Interface.ID_PasswordButton.Update(TICK):
            RECTS.append(Interface.ID_PasswordButton.Frame(DISPLAY))

        if self.DPB.Update(TICK):
            RECTS.append(self.DPB.Frame(DISPLAY))

        if Interface.BTN_Checkout.Update(TICK):
            RECTS.append(Interface.BTN_Checkout.Frame(DISPLAY))

        if Interface.BTN_Move.Update(TICK):
            RECTS.append(Interface.BTN_Move.Frame(DISPLAY))

        if Interface.BTN_Cancel.Update():
            RECTS.append(Interface.BTN_Cancel.Frame(DISPLAY))


    def Event_MouseMotion(self, POS):

        self.NotIdle()
        
        Interface.BTN_Cancel.MouseMotion(POS)
        self.DPB.MouseMotion(POS)


    def Event_MouseButtonDown(self, POS, BUTTON):

        self.NotIdle()
        
        Interface.BTN_Cancel.MouseButtonDown(POS, BUTTON)
        self.DPB.MouseButtonDown(POS, BUTTON)


    def Event_MouseButtonUp(self, POS, BUTTON):

        self.NotIdle()
        
        if Interface.BTN_Cancel.MouseButtonUp(POS, BUTTON):

            self.Close()

        if self.DPB.MouseButtonUp(POS, BUTTON):
            
            self.Student.removePassword()
            self.PWD.hideInstantly()
            self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
            self.SFA.perform()
            self.DPB.hide()
            self.Step = 1


    def Event_KeyDown(self, KEY):

        self.NotIdle()
        
        if KEY in (constants.K_ESCAPE, constants.K_KP_PERIOD):

            if self.InteractionStep == 0:

                if self.Step != 0 and self.PWD.Alpha == 255. and self.SFA.Done:
                    self.PWD.hideInstantly()
                    self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                    self.SFA.perform()
                    self.DPB.hide()
                    self.Step = 1

            elif self.InteractionStep == 1:

                if self.Step != 1:
                    self.PWD.hideInstantly()
                    self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                    self.SFA.perform()
                    self.DPB.hide()
                    self.Step = 1

            elif self.InteractionStep == 2:

                if self.Step > 1:
                    self.PWD.hideInstantly()
                    self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                    self.SFA.perform()
                    self.DPB.hide()
                    self.Step = 1

        elif KEY in (constants.K_0, constants.K_KP0):

            self.PWD.append(0)

        elif KEY in (constants.K_1, constants.K_KP1):

            self.PWD.append(1)

        elif KEY in (constants.K_2, constants.K_KP2):

            self.PWD.append(2)

        elif KEY in (constants.K_3, constants.K_KP3):

            self.PWD.append(3)

        elif KEY in (constants.K_4, constants.K_KP4):

            self.PWD.append(4)

        elif KEY in (constants.K_5, constants.K_KP5):

            self.PWD.append(5)

        elif KEY in (constants.K_6, constants.K_KP6):

            self.PWD.append(6)

        elif KEY in (constants.K_7, constants.K_KP7):

            self.PWD.append(7)

        elif KEY in (constants.K_8, constants.K_KP8):

            self.PWD.append(8)

        elif KEY in (constants.K_9, constants.K_KP9):

            self.PWD.append(9)

        elif KEY == constants.K_BACKSPACE:

            self.PWD.delete()


    # Scene 빠져나감
    def Close(self):
        if self.InteractionStep == 0:

            if self.Step != 0 and self.PWD.Alpha == 255. and self.SFA.Done:
                self.PWD.hideInstantly()
                self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                self.SFA.perform()
                self.DPB.hide()
                self.Step = 1

        elif self.InteractionStep == 1:

            if self.Step != 0 and self.PWD.Alpha == 255.:
                self.PWD.hideInstantly()
                self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                self.SFA.perform()
                self.DPB.hide()
                self.Step = 1

        elif self.InteractionStep == 2:

            if self.Step > 1:
                self.PWD.hideInstantly()
                self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                self.SFA.perform()
                self.DPB.hide()
                self.Step = 1


    # 유휴 상태 빠져나감
    def NotIdle(self):
        SceneManager.SCENE_TIME = 0
        if Interface.LY_Notice.Show:
            Interface.LY_Notice.hide()


    # 자리 선택 단계에서 비밀번호 설정을 누른 경우
    def Animation_Step0(self, A_OFFSET: float, TICK: int):

        # 애니메이션
        if self.Step in (2, 3):

            self.ID_Group_Y = Animate(self.ID_Group_Y, 238, 1.0, A_OFFSET)

            if not self.PWD.Show:
                self.PWD.show()

            if self.PWD.Y != 498:
                self.PWD.Animate_Y(498, 0.9, A_OFFSET)
                self.PWD.Updated = True

            if Interface.BTN_Cancel.Y != 970:
                Interface.BTN_Cancel.Animate_Y(970, 1.0, A_OFFSET)


        # 등장 애니메이션
        if self.Step == 0:
            if self.SFA.CurrentAlpha < 200.:
            
                self.ID_Group_Y = Animate(self.ID_Group_Y, 238, 1.0, A_OFFSET)

            if Interface.BTN_Cancel.Y != 970:
                Interface.BTN_Cancel.Animate_Y(970, 1.0, A_OFFSET)

            if self.SFA.Done:
                if self.New:
                    self.Step = 3
                else:
                    self.Step = 2
                self.PWD.unfreeze()

        # 전환 애니메이션
        elif self.Step == 1:

            if Interface.BTN_Cancel.Y == 1080 and self.SFA.Done:
                Interface.ID_PasswordButton.Reset()
                Interface.ID_InstructionText.set('학번을 입력합니다', Styles.BLACK)
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text1()
                Interface.ID_IdInputDialog.text2()
                Interface.ID_IdInputDialog.text3()
                Interface.ID_IdInputDialog.text4()
                Interface.ID_KeyInstruction.useKeypad()
                Interface.ST_SeatDisplay.hide()
                SceneManager.Scenes['MainScene'].ID_Group_Y = self.ID_Group_Y
                SceneManager.Scenes['MainScene'].InteractionStep = 0
                SceneManager.setScene('MainScene', False)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)

        # 기존 비밀번호 입력
        elif self.Step == 2:

            if self.PWD.done():
                self.PWD.freeze()

                if self.Student.matchPassword(self.PWD.getPassword()):
                    self.PWD.step('새로운 비밀번호 입력', True, Styles.BLACK)
                    self.PWD.clear()
                    self.CurrentPassword = ''
                    self.PWD.unfreeze()
                    self.DPB.show()
                    self.Step = 3
                else:
                    self.PWD.step('비밀번호가 일치하지 않습니다.', False, Styles.RED)
                    self.Delay = 1500
                    self.Step = 7

        # 새로운 비밀번호 입력
        elif self.Step == 3:

            if self.PWD.done():
                self.Step = 4
                self.CurrentPassword = self.PWD.getPassword()
                self.PWD.clear()
                self.PWD.step('비밀번호 다시 입력', True)

        # 새로운 비밀번호 다시 입력
        elif self.Step == 4:

            if self.PWD.done():
                self.PWD.freeze()
                self.DPB.hide()

                if self.PWD.getPassword() == self.CurrentPassword:
                    self.Student.setPassword(self.CurrentPassword)
                    ChairyData.ROOMDATA.SetPassword(self.Student)
                    self.PWD.step('설정 완료!', True, Styles.BLUE)
                    self.Delay = 1500
                    self.Step = 6
                else:
                    self.PWD.step('비밀번호가 일치하지 않습니다.', True, Styles.RED)
                    self.Delay = 1500
                    self.Step = 5
                
        # 비밀번호 설정 - 일치하지 않는 비밀번호
        elif self.Step == 5:
            
            if self.Delay == 0:
                self.PWD.step('새로운 비밀번호 입력', True, Styles.BLACK)
                self.PWD.clear()
                self.CurrentPassword = ''
                self.PWD.unfreeze()
                self.Step = 3

                if not self.New:
                    self.DPB.show()                    

        # 비밀번호 설정 - 설정 완료
        elif self.Step == 6:

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)
            
            if self.Delay == 0:
                self.PWD.hideInstantly()
                self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                self.SFA.perform()
                self.DPB.hide()
                self.Step = 1

        # 기존 비밀번호 입력 - 일치하지 않는 비밀번호
        elif self.Step == 7:
            
            if self.Delay == 0:
                self.PWD.step('기존 비밀번호 입력', False, Styles.BLACK)
                self.PWD.clear()
                self.CurrentPassword = ''
                self.PWD.unfreeze()
                self.Step = 2


    # 비밀번호가 있는 학번이 입력된 경우
    def Animation_Step1(self, A_OFFSET: float, TICK: int):

        # 등장 애니메이션
        if self.Step == 0:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 238, 1.0, A_OFFSET)

            if self.ID_Group_Y < 280:
                self.Step = 2
                self.PWD.show()
                self.PWD.unfreeze()

        # 취소 애니메이션
        elif self.Step == 1:

            if Interface.BTN_Cancel.Y == 1080 and self.SFA.Done:
                Interface.ID_PasswordButton.Reset()
                Interface.ID_InstructionText.set('학번을 입력합니다', Styles.BLACK)
                Interface.ID_IdInputDialog.StudentId[0] = '-'
                Interface.ID_IdInputDialog.StudentId[1] = '-'
                Interface.ID_IdInputDialog.StudentId[2] = '-'
                Interface.ID_IdInputDialog.StudentId[3] = '-'
                Interface.ID_IdInputDialog.text1()
                Interface.ID_IdInputDialog.text2()
                Interface.ID_IdInputDialog.text3()
                Interface.ID_IdInputDialog.text4()
                Interface.ID_KeyInstruction.useKeypad()
                Interface.ST_SeatDisplay.hide()
                SceneManager.Scenes['MainScene'].ID_Group_Y = self.ID_Group_Y
                SceneManager.Scenes['MainScene'].InteractionStep = 0
                SceneManager.setScene('MainScene', False)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)

        # 추가 애니메이션 및 기존 비밀번호 입력
        elif self.Step == 2:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 238, 1.0, A_OFFSET)

            if Interface.BTN_Cancel.Y != 970:
                Interface.BTN_Cancel.Animate_Y(970, 1.0, A_OFFSET)

            if self.PWD.Y != 498:
                self.PWD.Animate_Y(498, 0.9, A_OFFSET)
                self.PWD.Updated = True
            elif self.PWD.Freeze:
                self.PWD.unfreeze()

            if self.PWD.done():
                self.PWD.freeze()

                if self.Student.matchPassword(self.PWD.getPassword()):
                    self.Step = 4
                else:
                    self.PWD.step('비밀번호가 일치하지 않습니다.', False, Styles.RED)
                    self.Delay = 1500
                    self.Step = 3

        # 일치하지 않는 비밀번호
        elif self.Step == 3:
            
            if self.Delay == 0:
                self.PWD.step('비밀번호 입력', False, Styles.BLACK)
                self.PWD.clear()
                self.CurrentPassword = ''
                self.PWD.unfreeze()
                self.Step = 2

        # 두 프레임 넘김
        elif self.Step == 4:
            self.Step = 5

        elif self.Step == 5:
            self.PWD.hideInstantly()
            self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
            self.SFA.perform()
            self.Step = 6

        # 좌석 선택 애니메이션 1
        elif self.Step == 6:

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)

            if self.PWD.Alpha == 0. and Interface.BTN_Cancel.Y == 1080:
                self.Step = 7
                self.Delay = 100


        # 좌석 선택 애니메이션 2
        elif self.Step == 7:

            if self.Delay == 0 and self.PWD.Alpha == 0.:
                Interface.ID_PasswordButton.Reset()
                SceneManager.Scenes['MainScene'].ID_Group_Y = self.ID_Group_Y
                SceneManager.Scenes['MainScene'].StudentInfo(self.Student.StudentID)
                SceneManager.setScene('MainScene', False)


    # 퇴실 선택 단계에서 비밀번호 설정을 누른 경우
    def Animation_Step2(self, A_OFFSET: float, TICK: int):

        # 기존 요소 사라짐
        if self.Step == 0:

            self.ID_Group_Y = Animate(self.ID_Group_Y, 238, 1.0, A_OFFSET)
            Interface.BTN_Cancel.Animate_Y(970, 1.0, A_OFFSET)

            if self.ID_Group_Y == 238 and Interface.BTN_Cancel.Y == 970 and Interface.BTN_Checkout.Alpha == 0 and Interface.BTN_Move.Alpha == 0:
                self.PWD.show()
                self.PWD.unfreeze()
                if self.New:
                    self.Step = 3
                else:
                    self.Step = 2

        # 취소 애니메이션
        elif self.Step == 1:

            if Interface.BTN_Cancel.Y == 1080 and self.SFA.Done:
                Interface.ID_PasswordButton.Reset()
                Interface.LY_StudentInfo.hide()
                Interface.ID_KeyInstruction.wait()
                Interface.ST_SeatDisplay.hide()
                SceneManager.Scenes['MainScene'].ID_Group_Y = self.ID_Group_Y
                SceneManager.Scenes['MainScene'].InteractionStep = 14
                SceneManager.setScene('MainScene', False)

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)

        # 기존 비밀번호 입력
        elif self.Step == 2:

            if self.PWD.Alpha != 255. or self.PWD.Y != 498:
                self.PWD.Animate_Y(498, 0.9, A_OFFSET)
                self.PWD.Updated = True

            if self.PWD.done():
                self.PWD.freeze()
                
                if self.Student.matchPassword(self.PWD.getPassword()):
                    self.PWD.step('새로운 비밀번호 입력', True, Styles.BLACK)
                    self.PWD.clear()
                    self.CurrentPassword = ''
                    self.PWD.unfreeze()
                    self.DPB.show()
                    self.Step = 3
                else:
                    self.PWD.step('비밀번호가 일치하지 않습니다.', False, Styles.RED)
                    self.Delay = 1500
                    self.Step = 7

        # 새로운 비밀번호 입력
        elif self.Step == 3:

            if self.PWD.Alpha != 255. or self.PWD.Y != 498:
                self.PWD.Animate_Y(498, 0.9, A_OFFSET)
                self.PWD.Updated = True

            if self.PWD.done():
                self.Step = 4
                self.CurrentPassword = self.PWD.getPassword()
                self.PWD.clear()
                self.PWD.step('비밀번호 다시 입력', True)

        # 새로운 비밀번호 다시 입력
        elif self.Step == 4:

            if self.PWD.done():
                self.PWD.freeze()
                self.DPB.hide()

                if self.PWD.getPassword() == self.CurrentPassword:
                    self.Student.setPassword(self.CurrentPassword)
                    ChairyData.ROOMDATA.SetPassword(self.Student)
                    self.PWD.step('설정 완료!', True, Styles.BLUE)
                    self.Delay = 1500
                    self.Step = 6
                else:
                    self.PWD.step('비밀번호가 일치하지 않습니다.', True, Styles.RED)
                    self.Delay = 1500
                    self.Step = 5
                
        # 비밀번호 설정 - 일치하지 않는 비밀번호
        elif self.Step == 5:
            
            if self.Delay == 0:
                self.PWD.step('새로운 비밀번호 입력', True, Styles.BLACK)
                self.PWD.clear()
                self.CurrentPassword = ''
                self.PWD.unfreeze()
                self.Step = 3

                if not self.New:
                    self.DPB.show()                    

        # 비밀번호 설정 - 설정 완료
        elif self.Step == 6:

            Interface.BTN_Cancel.AnimateSpdUp_Y(False, 970, 1080, 4.0, A_OFFSET)
            
            if self.Delay == 0:
                self.PWD.hideInstantly()
                self.SFA = ShrinkFadeAnimation(120, 498, self.PWD.SURFACE, 0.9, 1.25, Styles.SPRLIGHTGRAY)
                self.SFA.perform()
                self.DPB.hide()
                self.Step = 1

        # 기존 비밀번호 입력 - 일치하지 않는 비밀번호
        elif self.Step == 7:
            
            if self.Delay == 0:
                self.PWD.step('기존 비밀번호 입력', False, Styles.BLACK)
                self.PWD.clear()
                self.CurrentPassword = ''
                self.PWD.unfreeze()
                self.Step = 2