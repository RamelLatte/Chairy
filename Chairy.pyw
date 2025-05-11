
if __name__ == '__main__':

    from ChairyApp.ChairyApp import ChairyApp
    from os import path

    ChairyApp.Init(path.dirname(path.abspath(path.dirname(__file__))))