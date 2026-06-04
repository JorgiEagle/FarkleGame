from dice_game.game_environment.scoring_rules import ScoringRules, IndividualDiceRule, NOfAKindRule, CountRule
from dice_game.game_environment.game_state import RoundState
from typing import TypedDict, TypeVar, Literal, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FarkleGameRules:
    rounds: int
    minimum_round_score: int
    

class ScoreActionType(TypedDict):
    type: Literal['score']
    rule: str
    dice_used: list[int]
    points: int


class RoundActionType(TypedDict):
    type: Literal['cash_out', 'roll']


FarkleLegalAction = ScoreActionType | RoundActionType
ActionType = TypeVar('ActionType')


class LegalActionGenerator(Generic[ActionType], ABC):
    @abstractmethod
    def get_legal_actions(self, round_state: RoundState) -> list[ActionType]:
        pass

    @abstractmethod
    def has_scoring_options(self, dice_roll: list[int]) -> bool:
        pass


class FarkleLegalActions(LegalActionGenerator[FarkleLegalAction]):
    def __init__(self, scoring_rules: list[ScoringRules]) -> None:
        self._rules = scoring_rules
    
    def register(self, rule: ScoringRules):
        self._rules.append(rule)

    def get_legal_actions(self, round_state: RoundState) -> list[FarkleLegalAction]:
        if round_state.terminal:
            return []
        legal_actions: list[FarkleLegalAction] = []
        if round_state.has_scored:
            legal_actions.append({'type': 'roll'})
        if round_state.round_score >= 300:
            legal_actions.append({'type': 'cash_out'})

        for rule in self._rules:
            if rule.matches(round_state.dice_values):
                legal_actions.append({
                    'type': 'score',
                    'rule': str(rule),
                    'dice_used': rule.dice_used(round_state.dice_values),
                    'points': rule.points
                })
        return legal_actions

    def has_scoring_options(self, dice_roll: list[int]) -> bool:
        return any(rule.matches(dice_roll) for rule in self._rules)
    

CLASSIC_RULES = [
    IndividualDiceRule(1, 1, 100),
    IndividualDiceRule(1, 2, 100),
    IndividualDiceRule(5, 1, 50),
    IndividualDiceRule(5, 2, 50),

    CountRule('straight', [1, 1, 1, 1, 1, 1], 1500),
    CountRule('three_pair', [2, 2, 2], 750),

    NOfAKindRule(1, 3, 1000),
    NOfAKindRule(1, 4, 1000),
    NOfAKindRule(1, 5, 1000),
    NOfAKindRule(1, 6, 1000),

    NOfAKindRule(2, 3, 200),
    NOfAKindRule(2, 4, 200),
    NOfAKindRule(2, 5, 200),
    NOfAKindRule(2, 6, 200),

    NOfAKindRule(3, 3, 300),
    NOfAKindRule(3, 4, 300),
    NOfAKindRule(3, 5, 300),
    NOfAKindRule(3, 6, 300),

    NOfAKindRule(4, 3, 400),
    NOfAKindRule(4, 4, 400),
    NOfAKindRule(4, 5, 400),
    NOfAKindRule(4, 6, 400),

    NOfAKindRule(5, 3, 500),
    NOfAKindRule(5, 4, 500),
    NOfAKindRule(5, 5, 500),
    NOfAKindRule(5, 6, 500),

    NOfAKindRule(6, 3, 600),
    NOfAKindRule(6, 4, 600),
    NOfAKindRule(6, 5, 600),
    NOfAKindRule(6, 6, 600),
]
