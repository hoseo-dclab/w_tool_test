import os
import sys

class CustomException(Exception):

    def __init__(self, msg):
        self.msg = msg
        print(self.msg + "\n--------------종료--------------")
        exit()


def raise_exception(msg):
    raise CustomException(msg)


def check_input(argv):
    try:
        if len(argv) != 3:
            raise raise_exception("디렉토리명과 접속 할 address를 정확히 입력해 주세요.")

        if argv[1][0:2] != "./":
            raise raise_exception("\"./폴더명\" 으로 입력해 주세요.")

        if not os.path.exists(argv[1]):
            raise raise_exception(argv[1][2:] + "은 존재하지 않는 디렉토리 입니다.")

        if not os.path.isdir(argv[1]):
            raise raise_exception(argv[1][2:] + "은 디렉토리가 아닙니다.")

    except CustomException:
        print("비정상 종료")
        exit()
