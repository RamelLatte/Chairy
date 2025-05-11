
# 빌드 명령어: pyinstaller --noupx --onefile --icon=Installer.ico ChairyInstaller.pyw --add-data="InstallerAsset;InstallerAsset"

import pygame as pg
from concurrent.futures import Future, ThreadPoolExecutor
import sys, os
from datetime import datetime
import json, requests, logging


AUTH_INFO = ('RamelLatte', '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')


class Installer:
    """
    ### Chairy Installer
    
    Chairy의 설치, 업데이트, 재설치를 수행하는 프로그램
    """

    Executor: ThreadPoolExecutor
    Task    : Future

    TestEnvir: bool

    Clock: pg.time.Clock
    Tick : int

    Screen: pg.Surface

    ButtonEnd: list[pg.Surface]
    ButtonEndActive: bool
    ButtonEndBtn: int
    ButtonEndRect: pg.Rect

    ButtonProceed: list[pg.Surface]
    ButtonProceedActive: bool
    ButtonProceedBtn: int
    ButtonProceedRect: pg.Rect

    ButtonReinstall: list[pg.Surface]
    ButtonReinstallActive: bool
    ButtonReinstallBtn: int
    ButtonReinstallRect: pg.Rect

    Assets: list[pg.Surface]
    SERIF_H3: pg.font.Font
    SANS_B5: pg.font.Font

    CurrentVersion: str
    LatestVersion : str
    LatestReleaseDate: datetime

    MouseDown: bool

    CanQuit: bool

    DownloadURL: str

    Logger: logging.Logger


    # 초기화
    def __init__(self):
        pg.init()

        try:
            self.TestEnvir = not hasattr(sys, '_MEIPASS')
        except:
            self.TestEnvir = False

        self.Executor = ThreadPoolExecutor(max_workers=1)
        self.Task = None

        self.Clock = pg.time.Clock()
        self.Tick = self.Clock.tick(24)

        self.Screen = pg.display.set_mode((640, 400))

        pg.display.set_caption('Chairy 설치 마법사')
        pg.display.set_icon(pg.image.load(self.resource_path('./InstallerAsset/InstallerLogo.png')))

        self.ButtonEnd = [
            pg.image.load(self.resource_path('./InstallerAsset/end0.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/end1.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/end2.png')).convert()
        ]
        self.ButtonEndActive = False
        self.ButtonEndRect = pg.Rect(0, 0, 0, 0)
        self.ButtonEndBtn = 0

        self.ButtonProceed = [
            pg.image.load(self.resource_path('./InstallerAsset/proceed0.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/proceed1.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/proceed2.png')).convert()
        ]
        self.ButtonProceedActive = False
        self.ButtonProceedRect = pg.Rect(0, 0, 0, 0)
        self.ButtonProceedBtn = 0

        self.ButtonReinstall = [
            pg.image.load(self.resource_path('./InstallerAsset/reinstall0.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/reinstall1.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/reinstall2.png')).convert()
        ]
        self.ButtonReinstallActive = False
        self.ButtonReinstallRect = pg.Rect(0, 0, 0, 0)
        self.ButtonReinstallBtn = 0

        self.Assets = [
            pg.image.load(self.resource_path('./InstallerAsset/Download.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/Update.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/Latest.png')).convert(),
            pg.image.load(self.resource_path('./InstallerAsset/Installing.png')).convert()
        ]

        self.CanQuit = True

        self.SERIF_H3 = pg.font.Font(self.resource_path("./InstallerAsset/NotoSerif_Condensed-ExtraBold.ttf"), 36)
        self.SANS_B5 = pg.font.Font(self.resource_path("./InstallerAsset/Paperlogy-4Regular.ttf"), 12)

        self.MouseDown = False

        self.InitLogger()

        self.Step_gettingInfo()

        self.Executor.submit(self.getVersion())

        self.MainLoop()

        ### 종료 로직 ###

        self.Executor.shutdown(cancel_futures=True)

    

    def InitLogger(self):
        self.Logger = logging.getLogger()

        # 로그의 레벨
        self.Logger.setLevel(logging.INFO)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s >> %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.Logger.addHandler(stream_handler)

        # log를 파일에 출력
        file_handler = logging.FileHandler(self.file_path('./installer.log'))
        file_handler.setFormatter(formatter)
        self.Logger.addHandler(file_handler)



    # 리소스 경로 획득
    def resource_path(self, relative_path):
        """
        에셋 파일의 절대 경로를 반환해주는 함수.

        - **onefile 실행 시:** 임시 폴더 기준으로 반환
        - **onedir/테스트 실행 시:** 현재 파일(exe or py)이 있는 폴더 기준으로 반환

        * ChatGPT가 써준 코드를 약간 수정함.
        """
        if self.TestEnvir:
            # 개발 중 또는 onedir 실행
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            # pyinstaller --onefile로 실행 중
            base_path = sys._MEIPASS
        
        full_path = os.path.join(base_path, relative_path)
        return full_path
    

    # 실행 파일 기준 경로 획득
    def file_path(self, relative_path):
        if self.TestEnvir:
            return os.path.join(os.path.abspath(os.path.dirname(__file__)) + relative_path)
        else:
            return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), relative_path)

    

    # 메인 루프
    def MainLoop(self):
        
        while 1:
            self.Tick = self.Clock.tick(24)

            # 이벤트 처리
            for event in pg.event.get():

                if event.type == pg.QUIT and self.CanQuit:
                   pg.quit()
                   return 
                
                elif event.type == pg.MOUSEMOTION:

                    if self.ButtonEndActive and self.ButtonEndRect.collidepoint(event.pos):
                        if self.MouseDown:
                            self.ButtonEndBtn = 2
                        elif self.ButtonEndBtn != 2:
                            self.ButtonEndBtn = 1
                    else:
                        self.ButtonEndBtn = 0

                    if self.ButtonProceedActive and self.ButtonProceedRect.collidepoint(event.pos):
                        if self.MouseDown:
                            self.ButtonProceedBtn = 2
                        elif self.ButtonProceedBtn != 2:
                            self.ButtonProceedBtn = 1
                    else:
                        self.ButtonProceedBtn = 0

                    if self.ButtonReinstallActive and self.ButtonReinstallRect.collidepoint(event.pos):
                        if self.MouseDown:
                            self.ButtonReinstallBtn = 2
                        elif self.ButtonReinstallBtn != 2:
                            self.ButtonReinstallBtn = 1
                    else:
                        self.ButtonReinstallBtn = 0

                    self.Render_Buttons(True)

                elif event.type == pg.MOUSEBUTTONDOWN:

                    if not self.MouseDown:
                        self.MouseDown = True

                    if self.ButtonEndActive and self.ButtonEndRect.collidepoint(event.pos):
                        self.ButtonEndBtn = 2

                    if self.ButtonProceedActive and self.ButtonProceedRect.collidepoint(event.pos):
                        self.ButtonProceedBtn = 2

                    if self.ButtonReinstallActive and self.ButtonReinstallRect.collidepoint(event.pos):
                        self.ButtonReinstallBtn = 2

                    self.Render_Buttons(True)

                elif event.type == pg.MOUSEBUTTONUP:

                    if self.MouseDown:
                        self.MouseDown = False

                    if self.ButtonEndActive:
                        if self.ButtonEndRect.collidepoint(event.pos):
                            self.ButtonEndBtn = 1
                            if self.CanQuit:
                                pg.quit()
                                return
                        else:
                            self.ButtonEndBtn = 0

                    if self.ButtonProceedActive:
                        if self.ButtonProceedRect.collidepoint(event.pos):
                            self.ButtonProceedBtn = 1
                            self.CanQuit = False
                            self.Executor.submit(self.performDownload)
                            self.Step_downloading()
                            continue
                        else:
                            self.ButtonProceedBtn = 0

                    if self.ButtonReinstallActive:
                        if self.ButtonReinstallRect.collidepoint(event.pos):
                            self.ButtonReinstallBtn = 1
                            self.Step_download()
                            continue
                        else:
                            self.ButtonReinstallBtn = 0

                    self.Render_Buttons(True)

                


    # 버튼 렌더링
    def Render_Buttons(self, updatePartly: bool = False):

        if self.ButtonEndActive:
            self.Screen.blit(self.ButtonEnd[self.ButtonEndBtn], self.ButtonEndRect)
            if updatePartly:
                pg.display.update(self.ButtonEndRect)
        if self.ButtonProceedActive:
            self.Screen.blit(self.ButtonProceed[self.ButtonProceedBtn], self.ButtonProceedRect)
            if updatePartly:
                pg.display.update(self.ButtonProceedRect)
        if self.ButtonReinstallActive:
            self.Screen.blit(self.ButtonReinstall[self.ButtonReinstallBtn], self.ButtonReinstallRect)
            if updatePartly:
                pg.display.update(self.ButtonReinstallRect)



    # 정보 가져오는 중
    def Step_gettingInfo(self):
        self.Screen.fill((0xFB, 0xFB, 0xFB))
        txt = self.SANS_B5.render('정보를 가져오고 있습니다...', 1, (0x20, 0x21, 0x24), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=320, centery=200))

        pg.display.flip()


    # 종료 메시지
    def Step_finish(self, finish_msg: str = '정보를 가져올 수 없습니다. 잠시후 다시 시도해주세요.'):
        self.Screen.fill((0xFB, 0xFB, 0xFB))
        txt = self.SANS_B5.render(finish_msg, 1, (0x20, 0x21, 0x24), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=320, centery=200))

        self.CanQuit = True

        self.ButtonEndActive = True
        self.ButtonEndRect = pg.Rect(246, 331, 150, 40)
        self.ButtonProceedActive = False
        self.ButtonProceedRect = pg.Rect(0, 0, 0, 0)
        self.ButtonReinstallActive = False
        self.ButtonReinstallRect = pg.Rect(0, 0, 0, 0)

        self.Render_Buttons()

        pg.display.flip()

    
    # 내려받기
    def Step_download(self):
        self.Screen.blit(self.Assets[0], (0, 0))
        txt = self.SANS_B5.render(self.file_path(''), 1, (0x82, 0x85, 0x8D), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(left=37, centery=121))
        txt = self.SERIF_H3.render(self.LatestVersion, 1, (0x49, 0xB2, 0x60), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(centerx=320, centery=234))
        txt = self.SANS_B5.render(f'게시일: {self.LatestReleaseDate}', 1, (0x82, 0x85, 0x8D), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=320, centery=272))

        self.ButtonEndActive = True
        self.ButtonEndRect = pg.Rect(162, 331, 150, 40)
        self.ButtonProceedActive = True
        self.ButtonProceedRect = pg.Rect(328, 331, 150, 40)
        self.ButtonReinstallActive = False
        self.ButtonReinstallRect = pg.Rect(0, 0, 0, 0)

        self.Render_Buttons()

        pg.display.flip()


    # 업데이트
    def Step_update(self):
        self.Screen.blit(self.Assets[1], (0, 0))
        txt = self.SANS_B5.render(self.file_path(''), 1, (0x82, 0x85, 0x8D), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(left=37, centery=121))
        txt = self.SERIF_H3.render(self.CurrentVersion, 1, (0x82, 0x85, 0x8D), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(centerx=158, centery=216))
        txt = self.SERIF_H3.render(self.LatestVersion, 1, (0x49, 0xB2, 0x60), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(centerx=481, centery=216))
        txt = self.SANS_B5.render(f'게시일: {self.LatestReleaseDate}', 1, (0x82, 0x85, 0x8D), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=481, centery=255))
        
        self.ButtonEndActive = True
        self.ButtonEndRect = pg.Rect(162, 331, 150, 40)
        self.ButtonProceedActive = True
        self.ButtonProceedRect = pg.Rect(328, 331, 150, 40)
        self.ButtonReinstallActive = False
        self.ButtonReinstallRect = pg.Rect(0, 0, 0, 0)

        self.Render_Buttons()

        pg.display.flip()


    # 최신버전 이용 중
    def Step_latest(self):
        self.Screen.blit(self.Assets[2], (0, 0))
        txt = self.SANS_B5.render(self.file_path(''), 1, (0x82, 0x85, 0x8D), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(left=37, centery=121))
        txt = self.SERIF_H3.render(self.CurrentVersion, 1, (0x82, 0x85, 0x8D), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(centerx=158, centery=216))
        txt = self.SERIF_H3.render(self.LatestVersion, 1, (0x49, 0xB2, 0x60), (0xE2, 0xE6, 0xEA))
        self.Screen.blit(txt, txt.get_rect(centerx=481, centery=216))
        txt = self.SANS_B5.render(f'게시일: {self.LatestReleaseDate}', 1, (0x82, 0x85, 0x8D), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=481, centery=255))

        self.ButtonEndActive = True
        self.ButtonEndRect = pg.Rect(246, 331, 150, 40)
        self.ButtonProceedActive = False
        self.ButtonProceedRect = pg.Rect(0, 0, 0, 0)
        self.ButtonReinstallActive = True
        self.ButtonReinstallRect = pg.Rect(541, 336, 75, 30)

        self.Render_Buttons()

        pg.display.flip()


    # 다운로드 중
    def Step_downloading(self, message: str = '내려받기 준비중..', length: int = 0):
        self.Screen.blit(self.Assets[3], (0, 0))
        pg.draw.rect(self.Screen, (0x4B, 0x84, 0xC5), [35, 195, length, 5])

        txt = self.SANS_B5.render(message, 1, (0x20, 0x21, 0x24), (0xFB, 0xFB, 0xFB))
        self.Screen.blit(txt, txt.get_rect(centerx=320, centery=172))

        self.ButtonEndActive = False
        self.ButtonEndRect = pg.Rect(0, 0, 0, 0)
        self.ButtonProceedActive = False
        self.ButtonProceedRect = pg.Rect(0, 0, 0, 0)
        self.ButtonReinstallActive = False
        self.ButtonReinstallRect = pg.Rect(0, 0, 0, 0)

        self.Render_Buttons()

        pg.display.flip()
                    


    ##### ThreadPoolExecutor에  #####

    # 버전 가져오기
    def getVersion(self):

        self.Logger.info('버전 가져오는 중')

        # 내부 파일에서 이용중인 버전 가져오기
        try:
            with open(self.file_path('./ChairyApp/chairy.json'), 'r') as f:
                info = json.load(f)
                self.CurrentVersion = info['version']
        except:
            self.CurrentVersion = None

        self.Logger.info(f'이 컴퓨터에 설치된 Chairy 버전: {self.CurrentVersion}')

        # GitHub REST API에서 최신 버전 가져오기
        try:
            response = requests.get('https://api.github.com/repos/RamelLatte/Chairy/releases', auth=AUTH_INFO)

            if response.status_code == 200:
                latest = response.json()[0]
                self.LatestVersion = latest['tag_name']
                self.LatestReleaseDate = datetime.strptime(latest['published_at'], '%Y-%m-%dT%H:%M:%SZ')
                self.DownloadURL = latest['assets'][0]['url']
            else:
                self.LatestVersion = None
                self.LatestReleaseDate = None
        except Exception as exception:
            import traceback

            self.Logger.error('오류 발생: \n' + traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.LatestVersion = None
            self.LatestReleaseDate = None

        self.Logger.info(f'GitHub에 배포된 최신 릴리즈 버전: {self.LatestVersion}')
        self.Logger.info(f'GitHub에 배포된 최신 릴리즈 게시일: {self.LatestReleaseDate.strftime("%Y년 %m월 %d일 %H:%M:%S")}\n')

        if self.LatestVersion is None and self.CurrentVersion is None:
            self.Step_finish()
        elif self.CurrentVersion is None:
            self.Step_download()
        else:
            if self.CurrentVersion != self.LatestVersion:
                self.Step_update()
            else:
                self.Step_latest()



    # 다운로드 1
    def performDownload(self):
        try:
            self._performDownload()
        except Exception as exception:
            import traceback

            self.Logger.error('오류 발생: \n' + traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.Step_finish(f'오류가 발생했습니다. 잠시후 다시 시도해주십시오. 자세한 기록은 "installer.log"를 참고하십시오.')

    
    # 다운로드 2 (ChatGPT가 코드 보완함)
    # 참고 자료: https://velog.io/@kimjihong/auto-update-github-rest-api-1
    def _performDownload(self):
        import zipfile
        import shutil

        # 다운로드 로직
        self.Step_downloading('내려받는 중...')
        self.Logger.info('내려받는 중')
        
        response = requests.get(self.DownloadURL, headers={'Accept': 'application/octet-stream'}, stream=True, auth=AUTH_INFO)
        
        if response.status_code == 200:
            update_newFile = self.file_path('./temp.zip')

            total_length = response.headers.get('content-length')
            if total_length is None:
                total_length = 0
            else:
                total_length = int(total_length)

            downloaded = 0
            chunk_size = 512 * 1024  # 512KB

            with open(update_newFile, "wb") as update_file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        update_file.write(chunk)
                        downloaded += len(chunk)
                        if total_length > 0:
                            length = downloaded / total_length * 450
                            percent = downloaded / total_length * 100
                            self.Logger.info(f'진행 상황: {downloaded}/{total_length} - {percent:.0f}%')
                            self.Step_downloading(f'내려받는 중...{percent:.0f}%', length)

            # 압축 해제 로직
            self.Step_downloading('압축 해제 중...', 450)
            self.Logger.info('압축 해제 중\n')

            skip_dirs = ['RoomData', 'school_data', 'student_data', 'log']

            unzip_dir = self.file_path('./_unzipped')

            os.makedirs(unzip_dir, exist_ok=True)

            with zipfile.ZipFile(update_newFile, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)

            unzipped_root = os.path.join(unzip_dir, 'Chairy')  # 압축에 포함된 최상위 디렉토리

            # 파일 복사 로직
            self.Step_downloading('파일 복사 중...', 510)
            self.Logger.info('파일 복사 중')

            # 복사
            for root, dirs, files in os.walk(unzipped_root):
                rel_dir = os.path.relpath(root, unzipped_root)
                top_level = rel_dir.split(os.sep)[0]

                # 스킵 디렉토리면: 존재 안 하면 만들고 복사 허용, 존재하면 복사 금지
                if top_level in skip_dirs:
                    existing_path = self.file_path(f'./{top_level}')
                    if os.path.exists(existing_path):
                        continue  # 복사하지 않음

                # 모든 경우에 폴더는 생성
                target_folder = self.file_path(f'./{rel_dir}')
                os.makedirs(target_folder, exist_ok=True)

                # 파일 복사
                for file in files:
                    abs_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_file_path, unzipped_root)
                    target_path = self.file_path(f'./{rel_path}')

                    try:
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        shutil.copy2(abs_file_path, target_path)
                        self.Logger.info(f'파일 복사 완료: {abs_file_path} → {target_path}')
                    except Exception as e:
                        self.Logger.error(f'파일 복사 실패: {abs_file_path} → {target_path}:\n{e}')

            
            # 정리
            self.Step_downloading('설치 완료, 정리 중...', 570)
            self.Logger.info('정리 중')

            os.remove(update_newFile)
            shutil.rmtree(unzip_dir)

            # 완료
            self.Step_finish('설치를 완료하였습니다.')

        else:
            self.Step_finish('현재 내려받기를 할 수 없습니다. 잠시후 다시 시도해주십시오.')


if __name__ == '__main__':

    Installer()