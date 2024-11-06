import json
import os.path

STOCKFISH = "stockfish"


def get_path(engine_name: str) -> str | None:
    config = load_config()
    return config[engine_name]["path"]


def load_config() -> dict:
    if not os.path.exists("config.json"):
        return dict()
    f = open("config.json", "r")
    json_config = f.read()
    f.close()
    return json.loads(json_config)
