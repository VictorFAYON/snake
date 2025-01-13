from .score import Score
import typing

class Scores:
    def __init__(self, max_scores:int,scores:list[Score])->None:
        self._max_scores=max_scores
        self._scores=scores[:self._max_scores]
    
    @classmethod
    def default(cls,max_scores:int) ->"Scores":
        return cls(max_scores, [Score(100,"Joe"),Score(80,"Jack"),Score(60,"William"),Score(40,"Averell")])
    
    def __iter__(self) -> typing.Iterator[Score]:
        return iter(self._scores)

