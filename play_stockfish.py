import sys

import core

if len(sys.argv) < 5:
    print("SYNTAX: play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR SECONDS_PER_GAME")
    exit(200)

wr, br = core.play_match(core.UciEngine(sys.argv[1]),
                         core.StockfishEngine(int(sys.argv[2])),
                         int(sys.argv[3]),
                         int(sys.argv[4])* 1000)

win = wr.count(1) + br.count(-1)
draw = wr.count(0) + br.count(0)
lose = wr.count(-1) + br.count(1)

print("Result:", win, '-', draw, '-', lose)
