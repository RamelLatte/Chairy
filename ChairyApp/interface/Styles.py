
from pygame.font import Font
from pygame.font import init
from dataclasses import dataclass


@dataclass(slots=True)
class Styles:
    """
    ### 스타일

    색깔 및 폰트를 미리 지정, 불러옴.
    """


    # Colors

    BLACK       = (0x20, 0x21, 0x24)
    DARKGRAY    = (0x82, 0x85, 0x8D)
    GRAY        = (0xB4, 0xB9, 0xBF)
    LIGHTGRAY   = (0xE2, 0xE6, 0xEA)
    SPRLIGHTGRAY= (0xF1, 0xF3, 0xF7)
    WHITE       = (0xFB, 0xFB, 0xFB)

    RED         = (0xE8, 0x40, 0x29)
    ORANGE      = (0xFF, 0x6A, 0x1A)
    YELLOW      = (0xFF, 0xB3, 0x0E)
    GREEN       = (0x1A, 0xB5, 0x3C)
    BLUE        = (0x4B, 0x84, 0xC5)
    PURPLE      = (0x9B, 0x43, 0xC3)
    PINK        = (0xFA, 0x5E, 0xBB)

    LIGHTRED    = (0xE8, 0x6F, 0x5F)
    LIGHTORANGE = (0xFF, 0x7F, 0x48)
    LIGHTYELLOW = (0xFF, 0xC5, 0x47)
    LIGHTGREEN  = (0x7C, 0xB7, 0x89)
    LIGHTBLUE   = (0x68, 0x9B, 0xE0)
    LIGHTPURPLE = (0xB2, 0x75, 0xCE)
    LIGHTPINK   = (0xFB, 0x86, 0xCC)

    # Fonts

    SANS_H1: Font
    """페이퍼로지 ExtraBold, 64pt"""
    SANS_H2: Font
    """페이퍼로지 ExtraBold, 48pt"""
    SANS_H3: Font
    """페이퍼로지 ExtraBold, 36pt"""
    SANS_H4: Font
    """페이퍼로지 ExtraBold, 28pt"""
    SANS_H5: Font
    """페이퍼로지 ExtraBold, 18pt"""
    SANS_H6: Font
    """페이퍼로지 ExtraBold, 12pt"""

    SANS_B1: Font
    """페이퍼로지 Regular, 42pt"""
    SANS_B2: Font
    """페이퍼로지 Regular, 30pt"""
    SANS_B3: Font
    """페이퍼로지 Regular, 18pt"""
    SANS_B4: Font
    """페이퍼로지 Regular, 16pt"""
    SANS_B5: Font
    """페이퍼로지 Regular, 12pt"""

    SERIF_H1: Font
    """Noto Serif Condensed ExtraBold, 64pt"""
    SERIF_H2: Font
    """Noto Serif Condensed ExtraBold, 48pt"""
    SERIF_H3: Font
    """Noto Serif Condensed ExtraBold, 36pt"""
    SERIF_H4: Font
    """Noto Serif Condensed ExtraBold, 24pt"""
    SERIF_H5: Font
    """Noto Serif Condensed ExtraBold, 18pt"""

    SERIF_B1: Font
    """Noto Serif Condensed Regular, 42pt"""
    SERIF_B2: Font
    """Noto Serif Condensed Regular, 30pt"""
    SERIF_B3: Font
    """Noto Serif Condensed Regular, 18pt"""
    SERIF_B4: Font
    """Noto Serif Condensed Regular, 12pt"""

    ANTON_H2: Font
    """Anton, 36pt"""
    ANTON_H3: Font
    """Anton, 32pt"""
    ANTON_H4: Font
    """Anton, 24pt"""
    ANTON_H5: Font
    """Anton, 18pt"""


    @staticmethod
    def initStyles(DIR: str):
        """ Styles 클래스를 초기화함. **매개변수로 실행 파일이 있는 디렉토리 위치를 투입하면 됨.** """

        init()
        #Styles.SANS_H1 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 64)
        Styles.SANS_H2 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 48)
        Styles.SANS_H3 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 36)
        Styles.SANS_H4 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 28)
        Styles.SANS_H5 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 18)
        Styles.SANS_H6 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-8ExtraBold.ttf", 12)

        #Styles.SANS_B1 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-4Regular.ttf", 42)
        #Styles.SANS_B2 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-4Regular.ttf", 30)
        Styles.SANS_B3 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-4Regular.ttf", 18)
        Styles.SANS_B4 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-4Regular.ttf", 16)
        Styles.SANS_B5 = Font(DIR + "/ChairyApp/assets/fonts/Paperlogy-4Regular.ttf", 12)

        Styles.SERIF_H1 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-ExtraBold.ttf", 64)
        #Styles.SERIF_H2 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-ExtraBold.ttf", 48)
        #Styles.SERIF_H3 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-ExtraBold.ttf", 36)
        #Styles.SERIF_H4 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-ExtraBold.ttf", 24)
        #Styles.SERIF_H5 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-ExtraBold.ttf", 18)

        #Styles.SERIF_B1 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-Regular.ttf", 42)
        #Styles.SERIF_B2 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-Regular.ttf", 30)
        #Styles.SERIF_B3 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-Regular.ttf", 18)
        #Styles.SERIF_B4 = Font(DIR + "/ChairyApp/assets/fonts/NotoSerif_Condensed-Regular.ttf", 12)

        Styles.ANTON_H2 = Font(DIR + "/ChairyApp/assets/fonts/Anton-Regular.ttf", 36)
        Styles.ANTON_H3 = Font(DIR + "/ChairyApp/assets/fonts/Anton-Regular.ttf", 32)
        Styles.ANTON_H4 = Font(DIR + "/ChairyApp/assets/fonts/Anton-Regular.ttf", 24)
        Styles.ANTON_H5 = Font(DIR + "/ChairyApp/assets/fonts/Anton-Regular.ttf", 18)