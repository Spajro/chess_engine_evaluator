import subprocess

from stockfish import Stockfish

from src import config
from src.flags import get_uci_debug

uci_debug = get_uci_debug()


class Engine:
    def update(self, moves: [str]):
        pass

    def update_fen(self, fen: str, moves: [str]):
        pass

    def make_move(self, wtime: int, btime: int) -> str:
        pass

    def make_move_time(self, move_time: int) -> str:
        pass

    def restart(self):
        pass

    def quit(self):
        pass

    def name(self) -> str:
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
        self.engine_name = engine_name

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

    def update(self, moves: [str]):
        self.__send("position startpos " + " ".join(moves) + "\n")

    def update_fen(self, fen: str, moves: [str]):
        self.__send("position " + fen + " " + " ".join(moves) + "\n")

    def make_move(self, wtime: int, btime: int) -> str:
        msg = "go wtime " + str(wtime) + " btime " + str(btime) + "\n"
        self.__send(msg)
        tokens = ["null"]
        while tokens[0] != "bestmove":
            result = self.__read()
            tokens = result.split(' ')
        return tokens[1].strip()

    def make_move_time(self, move_time: int) -> str:
        msg = "go movetime " + str(move_time) + "\n"
        self.__send(msg)
        tokens = ["null"]
        while tokens[0] != "bestmove":
            result = self.__read()
            tokens = result.split(' ')
        return tokens[1].strip()

    def restart(self):
        self.__send("ucinewgame")

    def quit(self):
        self.__send("quit")

    def name(self) -> str:
        return self.engine_name


class StockfishEngine(Engine):
    def __init__(self, elo):
        engine_path = config.get_path(config.STOCKFISH)
        if engine_path is None:
            print("Not configured Stockfish")
            exit(101)
        self.stock = Stockfish(engine_path)
        self.stock.set_elo_rating(elo)

    def update(self, moves: [str]):
        self.stock.make_moves_from_current_position(moves)

    def update_fen(self, fen: str, moves: [str]):
        self.stock.set_fen_position(fen, False)
        self.stock.make_moves_from_current_position(moves)

    def make_move(self, wtime: int, btime: int):
        result = self.stock.get_best_move(wtime, btime)
        if result is None:
            print(self.stock.get_board_visual())
        self.update([result])
        return result

    def make_move_time(self, move_time: int) -> str:
        result = self.stock.get_best_move_time(move_time)
        if result is None:
            print(self.stock.get_board_visual())
        self.update([result])
        return result

    def restart(self):
        self.stock.set_position()

    def quit(self):
        pass

    def name(self) -> str:
        return "stockfish"
