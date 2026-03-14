from dataclasses import dataclass
from dice_game.game_environment.game_state import GameMode, GameState, RoundState
from random import randint


class DiceGame:
    """
    Game engine for a dice game
    """
    def __init__(self, number_of_dice: int) -> None:
        self.current_dice = number_of_dice
        self._max_dice = number_of_dice
        self.game_state = self._new_game_state()
        # self.legal_action_generator = LegalActionGenerator()


    def _new_game_state(self) -> GameState:
        return GameState(0, self._new_round_state(), 0, False)
    

    def _new_round_state(self) -> RoundState:
        return RoundState(0, [randint(1, 6) for _ in range(self._max_dice)], 0, False, False)
    
    def _start_new_round(self):
        self.game_state.current_round = self._new_round_state()
        self.game_state.round_number += 1

    def reset(self):
        self.current_dice = self._max_dice
        self.game_state = self._new_game_state()

    def _make_observation(self):
        return {
            'dice_values': self.game_state.current_round.dice_values,
            'dice_remaining': self.game_state.current_round.dice_remaining,
            'round_score': self.game_state.current_round.round_score,
            'total_score': self.game_state.total_score,
            'round_number': self.game_state.round_number,
            # 'legal_actions': self.get_legal_actions(),
            'hot_dice': self.game_state.current_round.hot_dice,
            'is_terminal': self.game_state.current_round.terminal
        }
    
    # def get_legal_actions(self):
    #     return self.legal_action_generator.