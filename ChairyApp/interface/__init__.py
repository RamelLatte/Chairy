
from .Scene import Scene, SceneManager, SceneWarning
from .Styles import Styles


from .sideDisplays      import DateTimeDisplay, DietAndScheduleDisplay, SeatingStatus, QuickAccessButtons
from .keyInstruction    import KeyInstructionDisplay
from .idInputDialog     import IdInputDialog
from .scrollingTextbox  import ScrollingTextbox
from .seatDisplay       import SeatsDisplay, SeatsDataVerifyError
from .infoBox           import StudentInfoBox
from .buttons           import CancelButton, CheckoutButton, MoveButton, StatisticsExitButton, StatisticsExportButton, HideMediaButton
from .statistics        import TopBar
from .dateSelection     import DateSelection, MonthSelection
from .currentMedia      import CurrentMedia
from .layerComponents   import StudentHoverInfo, Notice
from .password          import SetPasswordButton, PasswordDialog, DeletePasswordButton
from .shrinkfade        import ShrinkFadeAnimation



__all__ = ['Scene', 'SceneManager', 'SceneWarning', 'ComponentWarning', 'Interface', 'Styles',
           'DateTimeDisplay', 'DietAndScheduleDisplay', 'SeatingStatus', 'QuickAccessButtons',
           'KeyInstructionDisplay',
           'IdInputDialog',
           'ScrollingTextbox',
           'SeatsDisplay', 'SeatsDataVerifyError',
           'StudentInfoBox',
           'CancelButton', 'CheckoutButton', 'MoveButton', 'StatisticsExitButton', 'StatisticsExportButton',
           'CurrentMedia', 'HideMediaButton',
           'StudentHoverInfo', 'Notice',
           'SetPasswordButton', 'PasswordDialog', 'DeletePasswordButton',
           'ShrinkFadeAnimation'
        ]


from ..Logging import LoggingManager as logging
from pygame import Surface


class ComponentWarning(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class Interface:
    """
    ### Interface

    다양한 화면 상의 구성 요소(Component)를 관리함.
    """


    # 준비 여부
    Ready: bool = False
    
    # SD: Side Display
    SD_DateTime        : DateTimeDisplay       
    SD_DietAndSchedule : DietAndScheduleDisplay
    SD_SeatingStatus   : SeatingStatus         
    SD_QuickAccess     : QuickAccessButtons

    # ID: student ID
    ID_InstructionText : ScrollingTextbox     
    ID_IdInputDialog   : IdInputDialog        
    ID_KeyInstruction  : KeyInstructionDisplay

    ID_PasswordButton  : SetPasswordButton

    # ST: SeaTing
    ST_SeatDisplay     : SeatsDisplay
    ST_StudentInfo     : StudentInfoBox

    # BTN: BuTtoN
    BTN_Cancel      : CancelButton  
    BTN_Checkout    : CheckoutButton
    BTN_Move        : MoveButton    

    # SC: StatiCs
    SC_TopBar       : TopBar
    SC_QuitButton   : StatisticsExitButton
    SC_ExportButton : StatisticsExportButton
    SC_DateSelection : DateSelection
    SC_MonthSelection: MonthSelection

    # OT: OThers
    OT_CurrentMedia : CurrentMedia

    # MD: MeDia
    MD_HideMediaBtn : HideMediaButton

    # LY: LaYer
    LY_StudentInfo  : StudentHoverInfo
    LY_Notice       : Notice


    @staticmethod
    def Init(Layer0: Surface, Layer1: Surface):
        try:
            Interface._Init(Layer0, Layer1)
        except Exception as e:
            logging.error('인터페이스를 불러오는 중 오류가 발생하였습니다.', e, True, True)


    @staticmethod
    def _Init(Layer0: Surface, Layer1: Surface):
        """ Interface 초기화 함수 """

        Interface.SD_DateTime        = DateTimeDisplay()
        Interface.SD_DietAndSchedule = DietAndScheduleDisplay()
        Interface.SD_SeatingStatus   = SeatingStatus()
        Interface.SD_QuickAccess     = QuickAccessButtons()

        Interface.ID_PasswordButton  = SetPasswordButton()

        Interface.ID_InstructionText = ScrollingTextbox(300, Styles.SANS_H4, "학번을 입력합니다", Styles.BLACK)
        Interface.ID_IdInputDialog   = IdInputDialog()
        Interface.ID_KeyInstruction  = KeyInstructionDisplay()

        Interface.ST_SeatDisplay     = SeatsDisplay()
        Interface.ST_StudentInfo     = StudentInfoBox()

        Interface.BTN_Cancel    = CancelButton()
        Interface.BTN_Checkout  = CheckoutButton()
        Interface.BTN_Move      = MoveButton()

        # 통계 화면
        Interface.SC_TopBar     = TopBar()
        Interface.SC_QuitButton = StatisticsExitButton()
        Interface.SC_ExportButton = StatisticsExportButton(130, 940)
        Interface.SC_DateSelection = DateSelection()
        Interface.SC_MonthSelection = MonthSelection()

        # 기타 요소
        Interface.OT_CurrentMedia = CurrentMedia()

        # 미디어
        Interface.MD_HideMediaBtn = HideMediaButton()

        # 레이어
        Interface.LY_StudentInfo = StudentHoverInfo(Layer1)
        Interface.LY_Notice = Notice(Layer1)

        # 준비 완료
        Interface.Ready = True