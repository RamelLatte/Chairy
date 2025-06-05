
import pygame as pg
from .Logging import LoggingManager
from .chairyData import *
from .UpdateExecutor import UpdateExecutor
from .interface import *
from ctypes import windll
from .Info import ChairyInfo
from .scenes.restart import RestartScene

from .scenes.errorDialog import ErrorDialog
from .optimization.rects import DirtyRectsManager


class ChairyApp:
    """
    ### ChairyApp
    
    Chairy 소프트웨어를 실행하는 클래스.
    """

    DIRECTORY   : str               = ""

    RUNNING     : bool  = True
    DISPLAY     : pg.Surface
    RECTS       : list[pg.Rect] = []

    CLOCK   : pg.time.Clock = pg.time.Clock()
    ANIMATION_OFFSET: float = 0.136
    TICK            : int   = 17

    UPDATER: UpdateExecutor = None

    LAYER0: pg.Surface
    LAYER0_RECTS: DirtyRectsManager = DirtyRectsManager()
    LAYER1: pg.Surface
    LAYER1_RECTS: DirtyRectsManager = DirtyRectsManager()


    @staticmethod
    def InitStyles():
        """ Styles 초기화 """

        from .interface.Styles import Styles
        Styles.initStyles(ChairyApp.DIRECTORY)


    @staticmethod
    def Init(directory: str):
        """ ChairyApp 초기화 """

        # DPI 스케일링 무시 설정
        windll.shcore.SetProcessDpiAwareness(1)

        # 로거 시작
        LoggingManager.Init(directory)

        # 버전 정보 불러옴
        ChairyInfo.Load(directory)
        LoggingManager.info(f'Chairy 버전: {ChairyInfo.Version}')

        # Pygame 시작
        pg.init()

        # 디렉토리 지정
        ChairyApp.DIRECTORY = directory
        ChairyData._Dir = directory
        SceneManager.directory(directory)

        # 화면 조정
        ChairyApp.DISPLAY = pg.display.set_mode((1920, 1080), (pg.FULLSCREEN | pg.SCALED))

        # 레이어 설정
        ChairyApp.LAYER0 = pg.Surface((1920, 1080))
        ChairyApp.LAYER0.fill(Styles.SPRLIGHTGRAY)
        ChairyApp.LAYER1 = pg.Surface((1920, 1080), (pg.SRCALPHA))
        ChairyApp.LAYER1.fill((0, 0, 0, 0))

        # 상단 아이콘 및 캡션 설정
        pg.display.set_caption("마산고등학교 학습 관리 시스템", "Chairy")
        pg.display.set_icon(pg.image.load(ChairyApp.DIRECTORY + "/ChairyApp/assets/ChairySquareBlack.png"))

        # Styles 초기화
        ChairyApp.InitStyles()

        # 화면이 준비될 때까지 기다림
        while 1:
            ChairyApp.TICK = ChairyApp.CLOCK.tick(60)
            pg.event.pump()  # 이벤트 큐 업데이트
            surface = pg.display.get_surface()
            if surface is not None:
                try:
                    surface.get_locked()  # 표면 접근 시도 (에러 안 나면 준비됨)
                    break
                except pg.error:
                    pass
            pg.display.flip()  # 화면을 강제로 업데이트

        # 메인 루프
        ChairyApp.MainLoop()

        # 종료
        pg.quit()
        return

    
    @staticmethod
    def MainLoop():
        """ 화면 렌더링 및 이벤트 처리를 위한 메인 루프 """
        
        while 1:

            ## Tick 및 Animation_Offset 계산
            ChairyApp.TICK          = ChairyApp.CLOCK.tick(60)

            ChairyApp.ANIMATION_OFFSET = ChairyApp.TICK * 0.008

            SceneManager.SceneTime(ChairyApp.TICK)

            # 오류 확인
            if LoggingManager.hasProblem() and SceneManager.CURRENT_SCENE.Identifier != 'ErrorDialog':
                problem = LoggingManager.popProblem()
                ErrorDialog(problem[0], problem[1], problem[2], problem[3], LoggingManager.LOG_FILE_NM)

            # 리셋 확인
            if SceneManager.RESET:
                SceneManager.RESET = False
                SceneManager.setScene(RestartScene())

            ## 이벤트 처리
            for event in pg.event.get():

                # 종료
                if event.type == pg.QUIT:
                    ChairyApp.RUNNING = False
                    break

                # 마우스 버튼 누름
                elif event.type == pg.MOUSEBUTTONDOWN:
                    SceneManager.CURRENT_SCENE.Event_MouseButtonDown(event.pos, event.button)

                # 마우스 버튼 놓음
                elif event.type == pg.MOUSEBUTTONUP:
                    SceneManager.CURRENT_SCENE.Event_MouseButtonUp(event.pos, event.button)

                # 마우스 움직임
                elif event.type == pg.MOUSEMOTION:
                    SceneManager.CURRENT_SCENE.Event_MouseMotion(event.pos)
                
                # 키보드 키 누름
                elif event.type == pg.KEYDOWN:
                    SceneManager.CURRENT_SCENE.Event_KeyDown(event.key)

                    if event.key == pg.K_F12 and SceneManager.CURRENT_SCENE.Identifier == '':
                        SceneManager.Restart()

                # 키보드 키 놓음
                elif event.type == pg.KEYUP:
                    SceneManager.CURRENT_SCENE.Event_KeyUp(event.key)


            ## 종료 확인
            if not ChairyApp.RUNNING or SceneManager.QUIT:

                # 화면 어두워짐
                disp = ChairyApp.DISPLAY.copy()
                disp.set_alpha(128)
                ChairyApp.DISPLAY.fill((0, 0, 0))
                ChairyApp.DISPLAY.blit(disp, (0, 0))
                txt = Styles.SANS_B4.render('종료 중...', 1, Styles.WHITE)
                ChairyApp.DISPLAY.blit(txt, txt.get_rect(centerx=960, centery=540))
                pg.display.flip()

                # 종료 로직
                LoggingManager.info('종료 중...')
                SceneManager.CURRENT_SCENE.Event_Quit()
                ChairyApp.UPDATER.stop()

                if SceneManager.CURRENT_SCENE.Identifier != 'start':
                    LoggingManager.info("입실 데이터를 저장합니다...")
                    ChairyData.ROOMDATA.Save()
                return

            ## 화면 업데이트
            if SceneManager.CURRENT_SCENE.INIT:
                SceneManager.CURRENT_SCENE.INIT = False
                SceneManager.CURRENT_SCENE.On_Init(ChairyApp.LAYER0)
                ChairyApp.DISPLAY.blit(ChairyApp.LAYER0, (0, 0))
                ChairyApp.LAYER1.fill((0, 0, 0, 0))
                pg.display.flip()

            SceneManager.CURRENT_SCENE.On_Update(ChairyApp.ANIMATION_OFFSET, ChairyApp.TICK)
            SceneManager.CURRENT_SCENE.On_Render(ChairyApp.ANIMATION_OFFSET, ChairyApp.TICK, ChairyApp.LAYER0, ChairyApp.LAYER0_RECTS)
            SceneManager.CURRENT_SCENE.On_Layer (ChairyApp.ANIMATION_OFFSET, ChairyApp.TICK, ChairyApp.LAYER1, ChairyApp.LAYER1_RECTS)

            ## 프레임 모니터링하고 싶다면 주석 해제
            #ChairyApp.RECTS.append(ChairyApp.DISPLAY.blit(Styles.SANS_H4.render(str(int(ChairyApp.CLOCK.get_fps())), 1, Styles.BLACK, Styles.SPRLIGHTGRAY), (0, 0))

            # 메인 레이어 처리
            if ChairyApp.LAYER0_RECTS.Full:
                ChairyApp.DISPLAY.blit(ChairyApp.LAYER0, (0, 0))
            elif not ChairyApp.LAYER0_RECTS.empty():

                ChairyApp.LAYER0_RECTS.calculate()

                for r in ChairyApp.LAYER0_RECTS.iter():
                    ChairyApp.DISPLAY.blit(ChairyApp.LAYER0, (r[0], r[1]), r)

            
            # 서브 레이어 처리    
            if ChairyApp.LAYER1_RECTS.Full:
                ChairyApp.DISPLAY.blit(ChairyApp.LAYER1, (0, 0))
            elif not ChairyApp.LAYER1_RECTS.empty():

                ChairyApp.LAYER1_RECTS.calculate()

                for r in ChairyApp.LAYER1_RECTS.iter():
                    ChairyApp.DISPLAY.blit(ChairyApp.LAYER1, (r[0], r[1]), r)
                    ChairyApp.LAYER0_RECTS.append(r)


            # 마무리 렌더링
            if ChairyApp.LAYER0_RECTS.Full:
                pg.display.update()
            else:
                ChairyApp.LAYER0_RECTS.calculate()

                if not ChairyApp.LAYER0_RECTS.empty():
                    pg.display.update(ChairyApp.LAYER0_RECTS.get())

                    
            # 정리
            ChairyApp.LAYER0_RECTS.clear()
            ChairyApp.LAYER1_RECTS.clear()



    @staticmethod
    def Init_UpdateExecutor():
        """ ChairyData가 준비되면 호출하는 메서드. 백그라운드에서 데이터를 업데이트하는 UpdateExecutor를 준비시킨다. """
        try:
            ChairyApp.UPDATER = UpdateExecutor()
        except Exception as e:
            LoggingManager.error("Updater 준비 도중 오류가 발생하였습니다.", e, True)