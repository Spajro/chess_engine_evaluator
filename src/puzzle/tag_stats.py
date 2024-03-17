from src.puzzle.puzzle import Puzzle


class TagStats:
    def __init__(self):
        self.tag_wins = dict()
        self.tag_loses = dict()
        self.tags = set()

    def __str__(self):
        result = ""
        for tag in self.tags:
            result += tag + " " + str(self.tag_wins[tag]) + " / " + str(self.tag_wins[tag] + self.tag_loses[tag]) + "\n"
        return result

    def add_puzzle(self, success: bool, puzzle: Puzzle):
        for tag in puzzle.tags:
            self.tags.add(tag)
            if tag not in self.tag_wins:
                self.tag_wins[tag] = 0
            if tag not in self.tag_loses:
                self.tag_loses[tag] = 0
            if success:
                self.tag_wins[tag] += 1
            else:
                self.tag_loses[tag] += 1
