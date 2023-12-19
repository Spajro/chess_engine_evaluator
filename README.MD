## Chess Engine Evaluator

### Setup

Set stockfish path:

`` py config.py set_stock STOCKFISH_PATH``

Set uci engine path:

``py config.py set_uci ENGINE_NAME ENGINE_PATH``

### Usage

Play a match between two uci engines

``py play.py ENGINE1 ENGINE2 GAMES_PER_COLOR SECONDS_PER_GAME``

Play a match between uci engine and stockfish of elo

``py play_stockfish.py ENGINE STOCKFISH_ELO GAMES_PER_COLOR SECONDS_PER_GAME``

### Debug
Display uci messages: ``--verbose=uci``

Display board and clock: ``--verbose=board``

All of above: ``--verbose=full``