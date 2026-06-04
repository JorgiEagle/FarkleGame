from abc import ABC, abstractmethod
from collections import Counter


class ScoringRules(ABC):
    INT_NAME_MAPPING = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six'
    }

    @abstractmethod
    def matches(self, dice_values: list[int]) -> bool:
        pass

    @abstractmethod
    def dice_used(self, dice_values: list[int]) -> list[int]:
        pass

    @property
    @abstractmethod
    def points(self) -> int:
        pass


class IndividualDiceRule(ScoringRules):   
    def __init__(self, dice_value: int, dice_count: int, points: int) -> None:
        self._dice_value = dice_value
        self._dice_count = dice_count
        self._points = points

    def matches(self, dice_values: list[int]) -> bool:
        return Counter(dice_values).get(self._dice_value, 0) >= self._dice_count
    
    def dice_used(self, dice_values: list[int]) -> list[int]:
        return [self._dice_value] * self._dice_count
    
    @property
    def points(self) -> int:
        return self._points * self._dice_count
    
    def __str__(self) -> str:
        return f'{self.INT_NAME_MAPPING[self._dice_count]}_{self._dice_value}{"s" if self._dice_count > 1 else ""}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._dice_value}, {self._dice_count}, {self.points})'    


class NOfAKindRule(ScoringRules):
    def __init__(self, dice_value: int, dice_count: int, base_points: int) -> None:
        self._dice_value = dice_value
        self._dice_count = dice_count
        self._points = base_points * (dice_count-2)

    def matches(self, dice_values: list[int]) -> bool:
        return Counter(dice_values).get(self._dice_value, 0) >= self._dice_count
    
    def dice_used(self, dice_values: list[int]) -> list[int]:
        return [self._dice_value] * self._dice_count
    
    @property
    def points(self) -> int:
        return self._points    
    
    def __str__(self) -> str:
        return f'{self.INT_NAME_MAPPING[self._dice_count]}_{self._dice_value}s'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._dice_value}, {self._dice_count}, {self.points})'    


class CountRule(ScoringRules):
    """
    Instances of these rules are based off total count, of objects
    """
    def __init__(self, name: str, required_count: list[int], points: int) -> None:
        self._required_count = required_count 
        self._points = points
        self._name = name
        
    def matches(self, dice_values: list[int]) -> bool:
         return all(x == self._required_count for x in Counter(dice_values).values())
    
    def dice_used(self, dice_values: list[int]) -> list[int]:
        return dice_values[:]
    
    @property
    def points(self) -> int:
        return self._points

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._name}, {self._required_count}, {self.points})'    
  

