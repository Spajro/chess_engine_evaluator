import sys


def get_eval_length() -> int:
    if "--length=short" in sys.argv:
        return 5
    if "--length=medium" in sys.argv:
        return 10
    if "--length=long" in sys.argv:
        return 25
    return 5


def get_threads() -> int:
    if "--threads=2" in sys.argv:
        return 2
    if "--threads=5" in sys.argv:
        return 5
    if "--threads=10" in sys.argv:
        return 10
    if "--threads=20" in sys.argv:
        return 20
    return 1


def get_time_control() -> int:
    if "--time=bullet" in sys.argv:
        return 60*1000
    if "--time=blitz" in sys.argv:
        return 5*60*1000
    if "--time=rapid" in sys.argv:
        return 10*60*1000
    return 5*60*1000


def get_board_debug() -> bool:
    return "--verbose=board" in sys.argv or "--verbose=full" in sys.argv


def get_uci_debug() -> bool:
    return "--verbose=uci" in sys.argv or "--verbose=full" in sys.argv
