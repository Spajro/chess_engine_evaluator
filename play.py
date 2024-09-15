import sys

from src.flags import summarize
from src.core import play_match
from src.templates import UciEngineTemplate

print(summarize())
if len(sys.argv) < 4:
    print("SYNTAX: py play.py ENGINE1 ENGINE2 GAMES_PER_COLOR")
    exit(200)

win, draw, lose = play_match(UciEngineTemplate(sys.argv[1]),
                             UciEngineTemplate(sys.argv[2]),
                             int(sys.argv[3]))

print("Result:", win, '-', draw, '-', lose)
