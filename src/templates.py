from src.engines import Engine, UciEngine, StockfishEngine


class EngineTemplate:
    def get_instance(self) -> Engine:
        pass


class UciEngineTemplate(EngineTemplate):
    def __init__(self, name: str):
        self.name = name

    def get_instance(self) -> UciEngine:
        return UciEngine(self.name)


class StockfishEngineTemplate(EngineTemplate):
    def __init__(self, elo: int):
        self.elo = elo

    def get_instance(self) -> StockfishEngine:
        return StockfishEngine(self.elo)
