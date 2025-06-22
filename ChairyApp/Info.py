
import json


class ChairyInfo:
    """ ### Chairy 정보 """

    Version     : str = None
    """ 소프트웨어 버전 """

    LatestVersion: str = None

    @staticmethod
    def Load(DIR: str):

        with open(DIR + '/ChairyApp/chairy.json', 'r') as f:
            info = json.load(f)
            ChairyInfo.Version = info['version']


    @staticmethod
    def getLatestVersion():

        try:
            import requests

            response = requests.get('https://api.github.com/repos/RamelLatte/Chairy/releases', timeout=10)#, auth=AUTH_INFO)

            if response.status_code == 200:
                latest = response.json()[0]
                ChairyInfo.LatestVersion = latest['tag_name']

            return (ChairyInfo.LatestVersion is None) or (ChairyInfo.LatestVersion == ChairyInfo.Version)
        
        except:
            
            return False