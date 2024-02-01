import sys

from src import core

if len(sys.argv) < 5:
    print("SYNTAX: play.py ENGINE1 ENGINE2 GAMES_PER_COLOR SECONDS_PER_GAME")
    exit(200)

win, draw, lose = core.play_match(core.UciEngine(sys.argv[1]),
                                  core.UciEngine(sys.argv[2]),
                                  int(sys.argv[3]),
                                  int(sys.argv[4]) * 1000)

print("Result:", win, '-', draw, '-', lose)
