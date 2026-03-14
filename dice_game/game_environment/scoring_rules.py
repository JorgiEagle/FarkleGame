from abc import ABC, abstractmethod

class ScoringRules(ABC):
    @abstractmethod
    def matches(self, dice_values) -> bool:
        pass

    @abstractmethod
    def dice_used(dice_values) -> list[int]:
        pass

    @abstractmethod
    def points(dice_used) -> int:
        pass


class Single1(ScoringRules):
    def matches(self, dice_values) -> bool:
        return 1 in dice_values
 
