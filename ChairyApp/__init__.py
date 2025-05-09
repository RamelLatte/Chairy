
"""
# ChairyApp



"""


from .ChairyApp import ChairyApp

__all__ = ['ChairyApp']

from .interface import SceneManager
from .scenes.start import StartScene

SceneManager.setScene(StartScene())