from random import randint
from logging import Logger
from typing import TypeAlias
from abc import ABC, abstractmethod
from dice_game.game_environment.game_state import GameMode, GameState, RoundState
from dice_game.game_environment.legal_action_generator import FarkleLegalActions, FarkleLegalAction, ScoreActionType, RoundActionType, LegalActionGenerator

logger = Logger(__name__)

StepReturn: TypeAlias = tuple[dict, int, bool, list]

class DiceGame:
    """
    Game engine for a dice game
    """
    def __init__(self, number_of_dice: int, number_of_rounds: int, legal_action_generator: LegalActionGenerator, observation_builder: FarkleObservation) -> None:
        self._max_dice = number_of_dice
        self.game_state = self._new_game()
        self.legal_action_generator = legal_action_generator
        self._max_rounds = number_of_rounds
        self.observer = observation_builder
        
    @property
    def current_round(self) -> RoundState:
        if self.game_state.current_round:
            return self.game_state.current_round
        else:
            raise ValueError('No active round')

    # Public API

    def reset(self) -> None:
        self.game_state = self._new_game()
        self._start_new_round()


    def step(self, action: FarkleLegalAction) -> StepReturn:
        # Check if round is over after returning Farkle or cash out
        if self.current_round.terminal:
            # act like roll action
            if self.game_state.round_number == self._max_rounds:
                self.game_state.game_over = True
            else:
                self._start_new_round()
            return self._make_observation(), 0, self.game_state.game_over, self.legal_action_generator.get_legal_actions(self.current_round)
        else:
            # Validate
            if action not in self.legal_action_generator.get_legal_actions(self.current_round):
                raise ValueError('Illegal Action')
            match action['type']:
                case 'score':
                    self._apply_score_action(action)
                    self.current_round.has_scored = True
                case 'roll':
                    self.current_round.has_scored = False
                    self._apply_roll()
                    if self._check_farkle():
                        # Farkle
                        self.current_round.busted = True
                        self.current_round.terminal = True
                        if all(round.busted and round.round_score ==  0 for round in self.game_state.rounds[-3:-1]):
                            self.current_round.round_score = -500
                        else:
                            self.current_round.round_score = 0
                case 'cash_out':
                    self.current_round.terminal = True
        reward = self.current_round.round_score
        return self._make_observation(), reward, False, self.legal_action_generator.get_legal_actions(self.current_round)
        
    # Internal Handlers

    def _new_game(self) -> GameState:
        logger.info('Starting new game')
        return GameState([], False)
    
    def _new_round(self) -> RoundState:
        logger.info('Starting new Round')
        return RoundState(0, self._roll_dice(self._max_dice), False, 0, False, False)
    
    @staticmethod
    def _roll_dice(num_of_dice):
        return [randint(1, 6) for _ in range(num_of_dice)]

    def _start_new_round(self) -> None:
        logger.info(f'Adding new round, {self.game_state.round_number=}')
        self.game_state.rounds.append(self._new_round())

    def _apply_score_action(self, action: ScoreActionType):
        round_state = self.current_round
        # Remove dice used
        for die in action['dice_used']:
            round_state.dice_values.remove(die)
        # Update points
        round_state.round_score += action['points']

        # handle hot dice
        if round_state.dice_remaining == 0:
            round_state.hot_dice += 1
            round_state.dice_values = []

    def _make_observation(self):
        return self.observer.observe(self.current_round, self.game_state, self.legal_action_generator)

    def _apply_roll(self):
        dice_to_roll = self.current_round.dice_remaining if self.current_round.dice_remaining else self._max_dice
        self.current_round.dice_values = self._roll_dice(dice_to_roll)

    def _check_farkle(self):
        """
        Returns true if current roll is a farkle state
        """
        return not self.legal_action_generator.has_scoring_options(self.current_round.dice_values)
    

class FarkleObservation:
    def observe(self, round_state: RoundState, game_state: GameState, legal_action_generator: LegalActionGenerator) -> dict:
        return {
            'dice_values': round_state.dice_values,
            'dice_remaining': round_state.dice_remaining,
            'round_score': round_state.round_score,
            'total_score': game_state.total_score,
            'round_number': game_state.round_number,
            'legal_actions': legal_action_generator.get_legal_actions(round_state),
            'hot_dice': round_state.hot_dice,
            'is_terminal': round_state.terminal
        }
