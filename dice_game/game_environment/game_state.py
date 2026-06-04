from dataclasses import dataclass
from enum import StrEnum, auto

class GameMode(StrEnum):
    CLASSIC = auto()


@dataclass
class RoundState:
    """
    Stores the state of a round
    """
    round_score: int
    dice_values: list[int]
    has_scored: bool
    hot_dice: int
    busted: bool
    terminal: bool
    

    @property
    def dice_remaining(self):
        return len(self.dice_values)
 

@dataclass
class GameState:
    """
    Stores the state of a entire game
    """
    # Round number 0 indexed
    rounds: list[RoundState]
    game_over: bool
    mode: GameMode = GameMode.CLASSIC

    @property
    def round_number(self):
        return len(self.rounds)
    
    @property
    def current_round(self) -> RoundState | None:
        return self.rounds[-1] if self.rounds else None
    
    @property
    def total_score(self) -> int:
        return sum(round.round_score for round in self.rounds)
    
 