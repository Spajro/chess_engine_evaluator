import sys

from src.core import play_match
from src.templates import StockfishEngineTemplate, UciEngineTemplate

if len(sys.argv) < 4:
    print("SYNTAX: play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR")
    exit(200)

win, draw, lose = play_match(UciEngineTemplate(sys.argv[1]),
                             StockfishEngineTemplate(int(sys.argv[2])),
                             int(sys.argv[3]))

print("Result:", win, '-', draw, '-', lose)
