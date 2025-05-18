
from pygame import constants, Surface, Rect, image
from os.path import exists

class SceneWarning(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class Scene:
    """
    ### 장면

    다양한 Component들을 처리하고 화면 상에 렌더링하며,
    키 입력과 마우스 입력 등의 사용자 상호작용을 처리,
    **프로그램에서 기능별로 그 로직을 구분하고 기능 간 꼬임을 방지하는 기능을 하는 클래스.**
    """

    INIT     : bool = False # 초기화해야하는지 여부
    Identifier: str = '' # 구분자. 사실상 ErrorDialog 말고는 쓰지 않음.

    def On_Init  (self, DISPLAY: Surface):
        """
        ChiaryApp에서 경우에 따라 호출되는 초기화 함수.
        초기 화면을 그리고 Scene의 데이터를 초기 상태로 되돌림.

        이 때 화면 전체가 갱신되고, 이후로 호출되는 **On_Render()** 메서드를 통해 부분적으로 화면을 업데이트함.
        - - -
        #### 매개변수:
        - **DISPLAY:** 렌더링할 화면, **1920x1080** 크기임.
        """
    def On_Update(self, ANIMATION_OFFSET: float, TICK: int) -> bool:
        """
        ChiaryApp에서 매 프레임마다 호출되는 계산 및 갱신 함수.
        Scene 내의 데이터를 갱신하고 수학적 연산을 주로 수행함.
        - - -
        #### 매개변수:
        - **ANIMATION_OFFSET:** 프레임레이트에 따라 변화하는 값이며, 프레임레이트의 변동에 따라 애니메이션 위치 변화를 보정하는데 사용됨.
        - **TICK:** 프레임레이트에 따라 변화하는 값이며, 프레임레이트의 변동에 따라 특정한 Surface의 Alpha 값 변화를 보정하는데 사용됨.
        """
    def On_Render(self, ANIMATION_OFFSET: float, TICK: int, DISPLAY: Surface, RECTS: list[Rect]):
        """
        ChiaryApp에서 매 프레임마다 호출되는 화면 렌더링 함수.
        On_Update() 메서드 이후로 호출되며, 화면 렌더링의 목적임.
        - - -
        #### 매개변수:
        - **ANIMATION_OFFSET:** 프레임레이트에 따라 변화하는 값이며, 프레임레이트의 변동에 따라 애니메이션 위치 변화를 보정하는데 사용됨.
        - **TICK:** 프레임레이트에 따라 변화하는 값이며, 프레임레이트의 변동에 따라 특정한 Surface의 Alpha 값 변화를 보정하는데 사용됨.
        - **DISPLAY:** 렌더링할 화면, **1920x1080** 크기임.
        - **RECTS:** 화면 상에서 업데이트 된 영역, list 유형이며, Rect를 추가하여 화면에서 어디를 업데이트해야하는지 결정함.
        """
        ...

    def Draw(self, SURFACE: Surface):
        """
        현재 표시되는 화면을 DISPLAY가 아닌 다른 Pygame Surface에 그림.
        - - -
        #### 매개변수:
        - **SURFACE:** 렌더링할 Surface, **1920x1080** 크기임.
        """
    
    def Call_Quit(self):
        """ 프로그램을 종료하도록 호출함. """
        SceneManager.Quit()

    def Event_Quit              (self):
        """ 종료 시 호출되는 이벤트 """
        ...
    def Event_MouseButtonDown   (self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 눌렀을 시 호출되는 이벤트 """
        ...
    def Event_MouseButtonUp     (self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 뗐을 시 호출되는 이벤트 """
        ...
    def Event_MouseMotion       (self, POS: tuple[int]             ):
        """ 마우스를 움직였을 시 호출되는 이벤트 """
        ...
    def Event_KeyDown           (self, KEY: constants              ):
        """ 키보드 키을 눌렀을 시 호출되는 이벤트 """
        ...
    def Event_KeyUp             (self, KEY: constants              ):
        """ 키보드 키를 뗐을 시 호출되는 이벤트 """
        ...


class SceneManager:
    """
    ### 장면 관리자

    다수의 Scene을 저장하고 재사용하며, ChairyApp에서 Scene에 접근하고 관리할 수 있도록 하는 클래스.

    추가적으로 에셋을 불러오는 기능도 수행함.
    """

    DIRECTORY       : str
    CURRENT_SCENE   : Scene

    SCENE_TIME: int  = 0
    
    QUIT    : bool = False
    RESET   : bool = False

    ## Scene들은 순환 Import 문제로 인해 SceneManager 클래스에서 Static으로 저장함. ##

    MainScene      : Scene

    ExportDaily     : Scene
    ExportMonthly   : Scene
    ExportPeriod    : Scene
    ExportSeats     : Scene
    
    ####

    @staticmethod
    def directory(dir: str):
        """ 디렉토리 지정 """
        SceneManager.DIRECTORY = dir


    @staticmethod
    def loadAsset(pathToAsset: str) -> Surface:
        """
        이미지 에셋을 불러옴.
        - - -
        #### 매개변수:
        - **pathToAsset:** 에셋의 경로, 기본 경로는 '.../ChairyApp/'이며 그 뒤로 **pathToAsset**을 뒤에 붙여 경로를 완성함.
        """
        return image.load(SceneManager.DIRECTORY + pathToAsset)
    

    @staticmethod
    def exists(path: str) -> bool:
        """
        파일이 존재하는지 확인함.
        - - -
        #### 매개변수:
        - **pathToAsset:** 에셋의 경로, 기본 경로는 '.../ChairyApp/'이며 그 뒤로 **pathToAsset**을 뒤에 붙여 경로를 완성함.
        """
        return exists(SceneManager.DIRECTORY + path)

    
    @staticmethod
    def setScene(scene: Scene):
        """
        Scene을 지정함. 장면 전환 이후 **On_Init()** 메서드가 호출됨.
        - - -
        #### 매개변수:
        - **scene:** 전환할 장면
        """
        SceneManager.CURRENT_SCENE  = scene
        scene.INIT                  = True
        SceneManager.SCENE_TIME     = 0


    @staticmethod
    def SceneTime(tick: int):
        """ 내부 사용 용도. ChairyApp에서만 사용함. """
        if SceneManager.SCENE_TIME < 100000:
            SceneManager.SCENE_TIME += tick


    @staticmethod
    def Quit():
        """ 종료 호출 """
        SceneManager.QUIT = True


    @staticmethod
    def Restart():
        """ 데이터 재설정 호출 """
        SceneManager.RESET = True