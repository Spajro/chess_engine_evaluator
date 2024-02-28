import concurrent.futures
import math
import time

import chess
import chess.pgn

from src.engines import Engine
from src.flags import get_threads, get_board_debug, get_time_control
from src.templates import EngineTemplate

board_debug = get_board_debug()
threads = get_threads()
game_time = get_time_control()


def play_game(white: Engine, black: Engine) -> int:
    white.restart()
    black.restart()
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
            black.update(move)

        if not white_move:
            stime = time.time() * 1000
            move = black.make_move(wtime, btime).rstrip()
            ftime = math.ceil(time.time() * 1000 - stime)
            btime -= ftime
            white.update(move)

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
                if board_debug:
                    print("White win outcome")
                return 1
            if outcome.winner == chess.BLACK:
                if board_debug:
                    print("Black win outcome")
                return -1
            if board_debug:
                print("Draw")
            return 0
    white.quit()
    black.quit()
    if board_debug:
        print("FINAL:")
        print("CLOCK: w=", wtime, "b=", btime)
        print(board)
    if wtime <= 0:
        if board_debug:
            print("Black win time")
        return -1
    if btime <= 0:
        if board_debug:
            print("White win time")
        return 1
    return 0


def play_match(engine1: EngineTemplate,
               engine2: EngineTemplate,
               games_per_color: int,
               ) -> tuple[int, int, int]:
    if threads == 1:
        return __play_match(engine1, engine2, games_per_color)
    else:
        return __play_match_threaded(engine1, engine2, games_per_color)


def __play_match(engine1: EngineTemplate,
                 engine2: EngineTemplate,
                 games_per_color: int,
                 ) -> tuple[int, int, int]:
    wr = [play_game(engine1.get_instance(), engine2.get_instance()) for _ in range(games_per_color)]
    br = [play_game(engine2.get_instance(), engine1.get_instance()) for _ in range(games_per_color)]
    win = wr.count(1) + br.count(-1)
    draw = wr.count(0) + br.count(0)
    lose = wr.count(-1) + br.count(1)
    return win, draw, lose


def __play_match_threaded(engine1: EngineTemplate,
                          engine2: EngineTemplate,
                          games_per_color: int,
                          ) -> tuple[int, int, int]:
    we = [(engine1.get_instance(), engine2.get_instance()) for _ in range(games_per_color)]
    be = [(engine2.get_instance(), engine1.get_instance()) for _ in range(games_per_color)]
    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        futures = [executor.submit(play_game, e1, e2) for e1, e2 in we]
    wr = [f.result() for f in futures]
    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        futures = [executor.submit(play_game, e1, e2) for e1, e2 in be]
    br = [f.result() for f in futures]

    win = wr.count(1) + br.count(-1)
    draw = wr.count(0) + br.count(0)
    lose = wr.count(-1) + br.count(1)
    return win, draw, lose
