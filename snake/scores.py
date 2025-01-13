import typing
import yaml

from .score import Score


class Scores:
    def __init__(self, max_scores: int, scores: list[Score],high_scores_file:str) -> None:
        self._max_scores = max_scores
        scores.sort(reverse = True)
        self._scores = scores[:self._max_scores]
        self._high_scores_file=high_scores_file

    @classmethod
    def default(cls, max_scores: int, high_scores_file:str) -> "Scores":
        high_scores_file
        with open(high_scores_file, "r") as f:
            scores = yaml.load(f, Loader=yaml.Loader)
        return cls(max_scores,scores,high_scores_file)

    def __iter__(self) -> typing.Iterator[Score]:
        return iter(self._scores)

    def save_scores(self)-> None:
        with open(self._high_scores_file, "w") as f:
            yaml.dump(self._scores, f)
    
    def is_high_score(self,score:Score)->bool:
        return len(self._scores)<self._max_scores + self._scores[-1].score<score.score

