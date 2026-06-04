# FarkleGame — CLAUDE.md

## Project Overview

A Python implementation of the dice game **Farkle**, designed as a reinforcement-learning environment. The core game engine is functional; agents, CLI, training infrastructure, and tests are all planned but not yet built.

## Directory Structure

```
dice_game/
├── game_environment/        # Core game engine (main implemented area)
│   ├── game_env.py          # Game loop, action dispatch, observation building
│   ├── game_state.py        # GameState and RoundState dataclasses
│   ├── legal_action_generator.py  # Action types, scoring rule registry, action validation
│   └── scoring_rules.py     # Abstract ScoringRules + three concrete rule classes
├── agents/                  # (empty) planned AI agent implementations
├── cli/                     # (empty) planned command-line interface
├── tests/                   # (empty) planned test suite
├── training/                # (empty) planned RL training code
```

## Game Rules (Farkle)

- 6 dice per turn. Roll all 6 to start a round.
- Each action: select a scoring combination from current dice, then choose to roll remaining dice or cash out.
- Cash out requires ≥ 300 points accumulated this round.
- **Hot dice**: if all 6 dice are scored in a turn, reset to 6 fresh dice and keep rolling.
- **Farkle (bust)**: if a roll yields no valid scoring combination, lose all round points.
- **Double Farkle penalty**: three consecutive busted rounds → −500 points applied.

### Scoring combinations (defined in `legal_action_generator.py` → `SCORING_RULES`)

| Combination | Points |
|---|---|
| Single 1 | 100 |
| Two 1s | 200 |
| Single 5 | 50 |
| Two 5s | 100 |
| Three of a kind (value V) | V × 100 (ones = 1000) |
| Four of a kind | × 2 of three-of-a-kind |
| Five of a kind | × 3 of three-of-a-kind |
| Six of a kind | × 4 of three-of-a-kind |
| Straight (1-2-3-4-5-6) | 1500 |
| Three pairs | 750 |

## Architecture

### `game_env.py` — `DiceGame`

The RL-style environment. `step(action)` returns `(observation, reward, done, legal_actions)`.

- **`reset()`** — starts a new game, returns initial observation.
- **`step(action)`** — dispatches to `_apply_score_action`, `_apply_roll`, or cash-out logic. Detects farkle after rolls. Closes round on cash-out or bust.
- **`_make_observation()`** — returns a dict: `{dice, dice_remaining, round_score, total_score, round_number, legal_actions, hot_dice, terminal}`.

### `game_state.py` — `RoundState` / `GameState`

Plain dataclasses. `GameState.total_score` sums all `RoundState.round_score` values. `RoundState.dice_remaining` is derived from the length of `dice_values`.

### `legal_action_generator.py` — `FarkleLegalActions`

Holds the canonical `SCORING_RULES` list and generates the legal action set for a given `RoundState`. Actions are typed dicts: either a score action `{rule_name, dice_used, points}` or a round action `{action: 'roll' | 'cash_out'}`.

### `scoring_rules.py` — Rule classes

| Class | Purpose |
|---|---|
| `IndividualDiceRule` | Ones and fives scored individually (e.g. one 1, two 5s) |
| `NOfAKindRule` | Three-or-more of a kind |
| `CountRule` | Whole-dice-set patterns (straight, three pairs) |

## Known Bugs

| Location | Issue |
|---|---|
| `game_env.py:111` | Hot dice resets `dice_values` to `[0]*max_dice` instead of rolling new dice. |
| `game_env.py` | `_check_farkle()` is an empty stub; farkle detection lives in `step()` instead. |

## What Is Not Yet Built

- `agents/` — no agent implementations (random, heuristic, or RL)
- `cli/` — no interactive or scriptable CLI
- `tests/` — no test suite; `test.py` is a scratch file
- `training/` — no training loop or RL scaffolding
- Logging calls are set up but never emit output

## Tech Stack

- Python 3.10+ (uses `match` statements, `dataclasses`, `TypedDict`, PEP 604 union types)
- No third-party dependencies in the game engine
- No build system or package config yet