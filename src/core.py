import concurrent.futures
from typing import Tuple

import chess
import chess.pgn

from src.clock import Clock
from src.engines import Engine
from src.flags import get_threads, get_board_debug, get_time_control, get_result_debug, get_moves_debug
from src.templates import EngineTemplate

board_debug = get_board_debug()
result_debug = get_result_debug()
moves_debug = get_moves_debug()
threads = get_threads()
game_time = get_time_control()

WHITE_WIN = "1-0"
BLACK_WIN = "0-1"
DRAW = "1/2-1/2"


def log_game_end(result: str, white: Engine, black: Engine, board: chess.Board, on_time=False):
    if not result_debug:
        return

    msg = white.name() + " " + result + " " + black.name() + " in " + str(board.ply()) + " moves"

    if on_time:
        msg += " (lost on time)"

    if moves_debug:
        msg += "\n"
        msg += str([move.uci() for move in board.move_stack])

    print(msg)


def log_state(board: chess.Board, clock: Clock):
    if not board_debug:
        return
    print(board)
    print(clock)


def is_game_end(board: chess.Board, clock: Clock) -> bool:
    return board.outcome() is not None or clock.out_of_time()


def get_result(board: chess.Board, clock: Clock) -> Tuple[int, str, bool]:
    outcome = board.outcome()

    if outcome is not None:
        if outcome.winner == chess.WHITE:
            return 1, WHITE_WIN, False
        if outcome.winner == chess.BLACK:
            return -1, BLACK_WIN, False
        return 0, DRAW, False
    if clock.white.out_of_time():
        return -1, BLACK_WIN, True
    if clock.black.out_of_time():
        return 1, WHITE_WIN, True

    print("[ERROR] game result unknown")
    return 0, DRAW, True


def play_game(white_template: EngineTemplate, black_template: EngineTemplate) -> int:
    white = white_template.get_instance()
    black = black_template.get_instance()
    clock = Clock()
    white_move = True
    board = chess.Board()
    while True and not clock.white.out_of_time() and not clock.black.out_of_time():
        log_state(board, clock)

        move = None
        if white_move:
            clock.white.start()
            move = white.make_move(clock.white.time_left, clock.black.time_left).rstrip()
            clock.white.stop()
            black.update([move])

        if not white_move:
            clock.black.start()
            move = black.make_move(clock.white.time_left, clock.black.time_left).rstrip()
            clock.black.stop()
            white.update([move])

        white_move = not white_move
        board.push_uci(move)

        if is_game_end(board, clock):
            white.quit()
            black.quit()
            log_state(board, clock)

            result, code, on_time = get_result(board, clock)
            log_game_end(code, white, black, board, on_time)
            return result

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
