class Encounter:
    def __init__(self, name: str, create_fn):
        self.name = name
        self._create_fn = create_fn

    def create_enemies(self, ascension: int, act: int) -> list:
        return self._create_fn(ascension, act)
