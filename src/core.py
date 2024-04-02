import concurrent.futures
import math
import time

import chess
import chess.pgn

from src.engines import Engine
from src.flags import get_threads, get_board_debug, get_time_control, get_result_debug
from src.templates import EngineTemplate

board_debug = get_board_debug()
result_debug = get_result_debug()
threads = get_threads()
game_time = get_time_control()

WHITE_WIN = "1-0"
BLACK_WIN = "0-1"
DRAW = "1/2-1/2"


def log_result(result: str, white: Engine, black: Engine, ply: int, on_time=False):
    msg = white.name() + " " + result + " " + black.name() + " in " + str(ply) + " moves"
    if on_time:
        msg += " (lost on time)"
    print(msg)


def play_game(white_template: EngineTemplate, black_template: EngineTemplate) -> int:
    white = white_template.get_instance()
    black = black_template.get_instance()
    wtime = game_time
    btime = game_time
    white_move = True
    board = chess.Board()
    while True and wtime > 0 and btime > 0:
        if board_debug:
            print("CLOCK: w=", wtime, "b=", btime)
            print(board)

        move = None
        if white_move:
            stime = time.time() * 1000
            move = white.make_move(wtime, btime).rstrip()
            ftime = math.ceil(time.time() * 1000 - stime)
            wtime -= ftime
            black.update([move])

        if not white_move:
            stime = time.time() * 1000
            move = black.make_move(wtime, btime).rstrip()
            ftime = math.ceil(time.time() * 1000 - stime)
            btime -= ftime
            white.update([move])

        white_move = not white_move
        board.push_uci(move)
        outcome = board.outcome()
        if outcome is not None:
            white.quit()
            black.quit()
            if board_debug:
                print("FINAL:")
                print("CLOCK: w=", wtime, "b=", btime)
                print(board)
            if outcome.winner == chess.WHITE:
                if result_debug:
                    log_result(WHITE_WIN, white, black, board.ply())
                return 1
            if outcome.winner == chess.BLACK:
                if result_debug:
                    log_result(BLACK_WIN, white, black, board.ply())
                return -1
            if result_debug:
                log_result(DRAW, white, black, board.ply())
            return 0
    white.quit()
    black.quit()
    if board_debug:
        print("FINAL:")
        print("CLOCK: w=", wtime, "b=", btime)
        print(board)
    if wtime <= 0:
        if result_debug:
            log_result(BLACK_WIN, white, black, board.ply(), True)
        return -1
    if btime <= 0:
        if result_debug:
            log_result(WHITE_WIN, white, black, board.ply(), True)
        return 1
    print("[ERROR] game result unknown")
    return 0


def play_match(engine1: EngineTemplate,
               engine2: EngineTemplate,
               games_per_color: int,
               ) -> tuple[int, int, int]:
    we = [(engine1, engine2, lambda x: x) for _ in range(games_per_color)]
    be = [(engine2, engine1, lambda x: -1 * x) for _ in range(games_per_color)]
    data = we + be

    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        futures = [(executor.submit(play_game, e1, e2), l) for e1, e2, l in data]
    results = [l(f.result()) for f, l in futures]

    win = results.count(1)
    draw = results.count(0)
    lose = results.count(-1)
    return win, draw, lose
