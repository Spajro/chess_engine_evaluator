import concurrent.futures

import chess
import chess.pgn

from src.clock import Clock
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
    clock = Clock()
    white_move = True
    board = chess.Board()
    while True and not clock.white.is_out_of_time() and not clock.black.is_out_of_time():
        if board_debug:
            print(clock)
            print(board)

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
        outcome = board.outcome()
        if outcome is not None:
            white.quit()
            black.quit()
            if board_debug:
                print("FINAL:")
                print(clock)
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
        print(clock)
        print(board)
    if clock.white.is_out_of_time():
        if result_debug:
            log_result(BLACK_WIN, white, black, board.ply(), True)
        return -1
    if clock.black.is_out_of_time():
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
