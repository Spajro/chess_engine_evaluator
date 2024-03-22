from src.puzzle.puzzle import Puzzle


class LengthStats:
    def __init__(self):
        self.length_wins = dict()
        self.length_loses = dict()
        self.lengths = set()

    def __str__(self):
        result = ""
        for length in self.lengths:
            result += (str(length) + " " + str(self.length_wins[length]) + " / " +
                       str(self.length_wins[length] + self.length_loses[length]) + "\n")
        return result

    def add_puzzle(self, success: bool, puzzle: Puzzle):
        length = len(puzzle.moves) - 1
        self.lengths.add(length)
        if length not in self.length_wins:
            self.length_wins[length] = 0
        if length not in self.length_loses:
            self.length_loses[length] = 0
        if success:
            self.length_wins[length] += 1
        else:
            self.length_loses[length] += 1
