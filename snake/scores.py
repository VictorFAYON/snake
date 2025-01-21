import logging
import typing
import yaml
import schema


from .score import Score
from pathlib import Path

logger = logging.getLogger("snake")

SCORE_FILE_SCHEMA = schema.Schema([
    {"name":str,
     "score":int}
])

class Scores :
    """Contains instances of scores."""

    def __init__(self, max_scores : int, scores : list[Score]) -> None :
        """Define the scores."""
        self._max_scores=max_scores
        self._scores=sorted(scores, reverse = True)[:max_scores]

    @classmethod
    def default(cls, max_scores : int ) -> "Scores" :
        """Classmethod."""
        logger.info("Default high scores loaded.")
        return cls(max_scores, [Score (score=-1, name="Joe"), Score(score=8, name="Jack"), Score(score=0,name="Averell"), Score(score=6, name="William")])

    def __iter__(self) -> typing.Iterator[Score]:
        """Iterate on the list of scores."""
        return iter(self._scores)


    def is_highscore(self, score_player : int) -> bool :
        """Define the case highscore."""
        return len(self._scores)<self._max_scores or self._scores[-1].score < score_player

    def add_score(self, score_player: Score) -> None:
        """Add a score and sort the list."""
        if self.is_highscore(score_player.score):
            if len(self._scores)>=self._max_scores :
                self._scores.pop()
                logger.info("New highest score found.")
            self._scores.append(score_player)
            self._scores.sort(reverse=True)

    def saving_hs(self,hs_file:Path)->None:
        """Saves high score in the file."""
        high_scores=[{"name":s.name,"score":s.score} for s in self]
        with hs_file.open("w") as fd:
            yaml.safe_dump(high_scores,fd)

    def loading_hs(self,scores_file:Path) -> None:
        """Loads high scores from the file."""
        with open(scores_file, "r") as f:
            hs = yaml.load(f, Loader=yaml.Loader)
        SCORE_FILE_SCHEMA.validate(hs)
        self._scores=[]
        for sc in hs:
            self._scores.append(Score(sc["score"],sc["name"]))
        self._scores=sorted(self._scores, reverse = True)[:self._max_scores]
        logger.info("High scores displayed.")















