
from pygame import Surface, Rect



class oldComponent:
    """
    ### 화면 상 구성 요소(Component)

    특정한 정보를 표시하거나 사용자와의 상호작용을 통해 특정한 기능을 수행함.
    """

    X: int
    Y: int

    def __init__(self):
        ...


    def Reset(self, x: int, y: int):
        """ 원래 초기 상태로 초기화함. **경우에 따라 매개변수로 초기 위치를 지정함.** """
        pass
    def Update(self, A_OFFSET: float) -> bool:
        """ Component 내의 데이터를 저장하고 계산 작업을 수행함. **Component의 생김새가 바뀌면 True를 반환함.** """
        return False
    def Frame(self, DISP: Surface) -> Rect:
        """ Component를 지정된 Surface에 그림. **일반적으로 Update()를 호출하고, True일 때 Frame()을 호출하는 형태임.** """
        pass
    
    def MouseMotion(self, POS: tuple[int]):
        """ 마우스를 움직였을 경우, 매개변수로 위치가 주어짐. """
        pass
    def MouseButtonDown(self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 누르거나 스크롤한 경우, 매개변수로 위치와 버튼이 주어짐. """
        pass
    def MouseButtonUp(self, POS: tuple[int], BUTTON: int):
        """ 마우스 버튼을 뗀 경우, 매개변수로 위치와 버튼이 주어짐. """
        pass