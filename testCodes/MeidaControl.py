
### 참고자료: https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python

from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
import asyncio

# 저거 위에 '\'는 무슨 의미가 있다라기보다는 한 줄로 쓰기에 코드나 너무 길어서 줄 구분할려고 마지막에 쓰는거
# (파이썬 문법임)


# StackOverFlow에 올라와있던 예제
async def get_media_info():
    sessions = await MediaManager.request_async()

    ### 원래 설명

    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    ### 해석본 (내가 해석한거임)
    
    # source_app_user_model_id 확인하는거랑 if 선언문은 선택사항임.
    # 특정 재생기나 프로그램의 미디어 정보만 얻고 싶다면 쓰면 됨.
    # (예를 들면, 오로지 'chrome.exe' 프로그램의 미디어 정보만 얻고 싶을 때)

    # ID 알고 싶으면, breakpoint() 함수를 써서 sessions.get_current_session() 돌리면 됨
    # 미디어 정보를 얻고 싶다면 일단 뭘 재생해야함.
    # 그리고 나오는 TARGET_ID를 쓰면 됨.

    current_session = sessions.get_current_session()

    if current_session:  # there needs to be a media session running
        if current_session.source_app_user_model_id == 'SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify': # 'SpotifyAB' 이건 내가 친거임. 안 치면 실행 자체가 안됨.
            info = await current_session.try_get_media_properties_async()

            # song_attr[0] != '_' ignores system attributes
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])

            return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    raise Exception('TARGET_PROGRAM is not the current media session')


if __name__ == '__main__':
    current_media_info = asyncio.run(get_media_info())

    print(current_media_info)