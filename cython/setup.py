
# 명령어: python setup.py build_ext --build-lib build

from setuptools import setup
from Cython.Build import cythonize
import sys

setup(
    name='optimization',
    ext_modules=cythonize(
        [
            'optimization/**/*.pyx'
        ],
        compiler_directives={
            'language_level': sys.version_info[0],  # Python 3.x 맞추기
            'boundscheck': False,                   # 배열 경계 검사 끄기 (성능↑)
            'wraparound': False,                   # 음수 인덱스 비활성화 (성능↑)
            'cdivision': True                      # C 언어식 나눗셈 사용 (성능↑, 주의!)
        },
    ),
    zip_safe=False,
)