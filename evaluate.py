import sys

from src.flags import summarize
from src.core import play_match
from src.flags import get_eval_length
from src.templates import UciEngineTemplate, StockfishEngineTemplate

print(summarize())
if len(sys.argv) < 2:
    print("SYNTAX: py evaluate.py ENGINE_NAME")
    exit(200)

elo = 1500
max_elo = 3000
min_elo = 0
for ed in [500, 400, 300, 200, 100]:
    win, draw, lose = play_match(UciEngineTemplate(sys.argv[1]),
                                 StockfishEngineTemplate(elo),
                                 get_eval_length())

    rating_change = ed * (win - lose) / 10

    print("Result: ", win, '-', draw, '-', lose, " vs elo:", elo, " rating change: ", rating_change)

    elo += rating_change

    if rating_change > 0 and elo > min_elo:
        min_elo = elo
    if rating_change < 0 and elo < max_elo:
        max_elo = elo

print("Evaluated elo: ", elo, " min win: ", min_elo, " max lose: ", max_elo)
