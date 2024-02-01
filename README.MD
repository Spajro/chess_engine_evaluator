## Chess Engine Evaluator

### Setup

Set stockfish path:

`` py setup.py stockfihs STOCKFISH_PATH``

Set uci engine path:

``py setup.py uci ENGINE_NAME ENGINE_PATH``

### Usage

Evaluate uci engine

``py evaluate.py ENGINE``

Play a match between two uci engines

``py play.py ENGINE1 ENGINE2 GAMES_PER_COLOR SECONDS_PER_GAME``

Play a match between uci engine and stockfish of elo

``py play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR SECONDS_PER_GAME``

### Debug

Display uci messages: ``--verbose=uci``

Display board and clock: ``--verbose=board``

All of above: ``--verbose=full``

### Threading

Enable threading and set number of threads by flags:

``--threads=2``

``--threads=5``

``--threads=10``

### Evaluation length
Set number of games played in evaluation:

``"--length=short"``

``"--length=medium"``

``"--length=long"``