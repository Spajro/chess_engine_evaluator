import math
import sys
import time

import chess
import chess.pgn
from threading import Thread

from src.engines import Engine
from src.templates import EngineTemplate


def __load_threads_from_flag():
    if "--threads=2" in sys.argv:
        return 2
    if "--threads=5" in sys.argv:
        return 5
    if "--threads=10" in sys.argv:
        return 10
    return 1


board_debug = "--verbose=board" in sys.argv or "--verbose=full" in sys.argv
threads = __load_threads_from_flag()


def play_game(white: Engine, black: Engine, game_time: int) -> int:
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
               game_time: int
               ) -> tuple[int, int, int]:
    if threads == 1:
        return __play_match(engine1.get_instance(), engine2.get_instance(), games_per_color, game_time)
    else:
        return __play_match_threaded(engine1, engine2, games_per_color, game_time)


def __play_match(engine1: Engine,
                 engine2: Engine,
                 games_per_color: int,
                 game_time: int
                 ) -> tuple[int, int, int]:
    wr = [play_game(engine1, engine2, game_time) for _ in range(games_per_color)]
    br = [play_game(engine2, engine1, game_time) for _ in range(games_per_color)]
    win = wr.count(1) + br.count(-1)
    draw = wr.count(0) + br.count(0)
    lose = wr.count(-1) + br.count(1)
    return win, draw, lose


def __play_match_threaded(engine1: EngineTemplate,
                          engine2: EngineTemplate,
                          games_per_color: int,
                          game_time: int
                          ) -> tuple[int, int, int]:
    wr = []
    br = []
    we = [(engine1.get_instance(), engine2.get_instance()) for _ in range(games_per_color)]
    be = [(engine2.get_instance(), engine1.get_instance()) for _ in range(games_per_color)]
    wt = [Thread(target=play_game, args=(e1, e2, game_time)) for (e1, e2) in we]
    bt = [Thread(target=play_game, args=(e2, e1, game_time)) for (e1, e2) in be]
    for i in range(int(games_per_color / threads)):
        for t in wt[i:i + threads]:
            t.start()
        wr += [t.join() for t in wt[i:i + threads - 1]]

    for i in range(int(games_per_color / threads)):
        for t in bt[i:i + threads - 1]:
            t.start()
        br += [t.join() for t in bt[i:i + threads - 1]]

    win = wr.count(1) + br.count(-1)
    draw = wr.count(0) + br.count(0)
    lose = wr.count(-1) + br.count(1)
    return win, draw, lose
