import math
import subprocess
import sys
import time

import chess
from stockfish import Stockfish

import config

uci_debug = "--verbose=uci" in sys.argv or "--verbose=full" in sys.argv
board_debug = "--verbose=board" in sys.argv or "--verbose=full" in sys.argv


class Engine:
    def update(self, move: str):
        pass

    def make_move(self, wtime: int, btime: int) -> str:
        pass

    def restart(self):
        pass


class UciEngine(Engine):

    def __log_out(self, txt: str):
        if uci_debug and len(txt) > 0:
            print("-> " + txt)

    def __log_in(self, txt: str):
        if uci_debug and len(txt) > 0:
            print("<- " + txt.rstrip())

    def __send(self, msg: str):
        self.proc.stdin.write(msg + "\n")
        self.proc.stdin.flush()
        self.__log_out(msg)

    def __read(self) -> str:
        msg = self.proc.stdout.readline()
        self.__log_in(msg)
        return msg

    def __init__(self, engine_name: str):
        engine_path = config.get_path(engine_name)
        if engine_path is None:
            print("Unknown engine")
            exit(100)
        self.proc = subprocess.Popen(engine_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     text=True)

        self.__send("uci")
        name = self.__read()
        uci = self.__read()
        self.__send("isready")
        readyok = self.__read()
        self.__send("ucinewgame")

    def update(self, move: str):
        self.__send("position " + move + "\n")

    def make_move(self, wtime: int, btime: int) -> str:
        msg = "go wtime " + str(wtime) + " btime " + str(btime) + "\n"
        self.__send(msg)
        tokens = ["null"]
        while tokens[0] != "bestmove":
            result = self.__read()
            tokens = result.split(' ')
        return tokens[1]

    def restart(self):
        self.__send("ucinewgame")


class StockfishEngine(Engine):
    def __init__(self, elo):
        engine_path = config.get_path(config.STOCKFISH)
        if engine_path is None:
            print("Not configured Stockfish")
            exit(101)
        self.stock = Stockfish(engine_path)
        self.stock.set_elo_rating(elo)

    def update(self, move: str):
        self.stock.make_moves_from_current_position([move])

    def make_move(self, wtime: int, btime: int):
        result = self.stock.get_best_move(wtime, btime)
        if result is None:
            print(self.stock.get_board_visual())
        self.update(result)
        return result

    def restart(self):
        self.stock.set_position()


def play_game(white: Engine, black: Engine, game_time: int) -> int:
    white.restart()
    black.restart()
    wtime = game_time
    btime = game_time
    white_move = True
    board = chess.Board()
    while True and wtime > 0 and btime > 0:
        if board_debug:
            print("CLOCK: w=", wtime, "|b=", btime)
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

    if wtime <= 0:
        if board_debug:
            print("Black win time")
        return -1
    if btime <= 0:
        if board_debug:
            print("White win time")
        return 1
    return 0


def play_match(engine1: Engine, engine2: Engine, games_per_color: int, game_time: int) -> tuple[int, int, int]:
    wr = [play_game(engine1, engine2, game_time) for _ in range(games_per_color)]
    br = [play_game(engine2, engine1, game_time) for _ in range(games_per_color)]
    win = wr.count(1) + br.count(-1)
    draw = wr.count(0) + br.count(0)
    lose = wr.count(-1) + br.count(1)
    return win, draw, lose
