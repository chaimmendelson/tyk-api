from src.api import TykApi

class TykRepository:

    def __init__(self, api: TykApi):
        self.api = api