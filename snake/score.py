class Score:

    MAX_LENTH=8

    def __init__(self, score: int,name: str)-> None:
        self.score=score
        self.name=name[:MAX_LENTH]

    @property
    def Name(self) ->str:
        return self.name
    
    @property
    def Score(self) -> int:
        return self.score
    
    def __lt__(self, other: object)->bool:
        return isinstance(object,Score) and self.score < other.score
    
