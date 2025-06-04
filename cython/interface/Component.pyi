
from pygame import Surface, Rect
from array import array


class Component:
    """
    ### 화면 상 구성 요소(Component)

    특정한 정보를 표시하거나 사용자와의 상호작용을 통해 특정한 기능을 수행함.
    
    **Cython으로 컴파일하였으며, 애니메이션 관련 연산에 최적화됨.**
    """

    X : float
    Y : float
    _X : float
    _Y : float

    W: int
    H: int


    def __init__(self, x: int, y: int, w: int, h: int):
        ...


    def newMouseFields(self, size: int):
        """ 마우스 버튼 인식 구역을 만듦. """
        ...

    def setMouseField(self, Index: int, X: int, Y: int, W: int, H: int):
        """
        마우스 버튼 인식 구역을 지정함.
        
        - - -

        **매개변수로 지정하는 X, Y 값은 Component의 위치를 기준으로 한 상댓값을 기준으로 함.**
        """
        ...

    def setMouseField_DisplayPos(self, Index: int, X: int, Y: int, W: int, H: int):
        """
        화면 상 절대적인 위치값을 기준으로 마우스 버튼 인식 구역을 지정함.
        
        - - -

        **매개변수로 지정하는 X, Y 값은 화면 상의 위치를 기준으로 함.**
        """
        ...

    def collidepoint(self, index: int, point: tuple[int]) -> bool:
        """
        지정된 마우스 버튼 인식 구역에 점이 위치해 있는지 판단함.

        **인덱스가 잘못 지정이 된 경우 무조건 False를 반환함.**
        """


    def MoveTo(self, X: float, Y: float) -> Rect:
        """ 즉시 지정한 위치로 움직임. """
        ...


    def Animate_X(self, Target: float, Speed: float, AO: float): ...
    def Animate_Y(self, Target: float, Speed: float, AO: float): ...
    def AnimateSpdUp_X(self, Negative: bool, Start: float, Target: float, Speed: float, AO: float): ...
    def AnimateSpdUp_Y(self, Negative: bool, Start: float, Target: float, Speed: float, AO: float): ...


    def calculateRect(self) -> array:
        """ 애니메이션으로 인한 위치 변화를 고려해 최적의 화면 업데이트 영역을 반환함. """
        ...


    def convertRect(self, Rect: Rect) -> array:
        """ Pygame Rect를 DirtyRectsManager가 쓸 수 있는 array로 변환함. """
        ...


    def calculateTrailRect_X(self) -> Rect:
        """ 애니메이션로 인해 생기는 흔적에 대한 영역을 반환함. """
        ...

    def calculateTrailRect_Y(self) -> Rect:
        """ 애니메이션로 인해 생기는 흔적에 대한 영역을 반환함. """
        ...


    def Reset(self, x: int, y: int):
        """ 원래 초기 상태로 초기화함. **경우에 따라 매개변수로 초기 위치를 지정함.** """
        ...
    def Update(self, A_OFFSET: float) -> bool:
        """ Component 내의 데이터를 저장하고 계산 작업을 수행함. **Component의 생김새가 바뀌면 True를 반환함.** """
        return False
    def Frame(self, DISP: Surface) -> array:
        """ Component를 지정된 Surface에 그림. **일반적으로 Update()를 호출하고, True일 때 Frame()을 호출하는 형태임.** """
        ...
    
    def MouseMotion(self, POS: tuple[int]):
        """ 마우스를 움직였을 경우, 매개변수로 위치가 주어짐. """
        ...
    def MouseButtonDown(self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 누르거나 스크롤한 경우, 매개변수로 위치와 버튼이 주어짐. """
        ...
    def MouseButtonUp(self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 뗀 경우, 매개변수로 위치와 버튼이 주어짐. """
        ...