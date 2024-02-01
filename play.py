import sys

from src.core import play_match
from src.templates import UciEngineTemplate

if len(sys.argv) < 5:
    print("SYNTAX: play.py ENGINE1 ENGINE2 GAMES_PER_COLOR SECONDS_PER_GAME")
    exit(200)

win, draw, lose = play_match(UciEngineTemplate(sys.argv[1]),
                             UciEngineTemplate(sys.argv[2]),
                             int(sys.argv[3]),
                             int(sys.argv[4]) * 1000)

print("Result:", win, '-', draw, '-', lose)
