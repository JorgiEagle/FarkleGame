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
    round_number: int
    current_round: RoundState
    total_score: int
    game_over: bool
    mode: GameMode = GameMode.CLASSIC
