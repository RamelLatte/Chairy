
import json, datetime


class ChairyInfo:
    """ ### Chairy 정보 """

    Version     : str
    """ 소프트웨어 버전 """

    @staticmethod
    def Load(DIR: str):

        with open(DIR + '/ChairyApp/chairy.json', 'r') as f:
            info = json.load(f)
            ChairyInfo.Version = info['version']