from enum import Enum
import numpy as np
import json


class StatEnhancer:
    def __init__(self, data):
        self.df = data
        self.add_winner_each_round()
        self.add_points_won_each_round()
        self.add_bet_numbering()
        self.humanize_first_bet_column()

    def add_winner_each_round(self):
        self.df["winner"] = ""
        self.df.loc[self.lars_winner_mask, "winner"] = "Lars"
        self.df.loc[self.florentin_winner_mask, "winner"] = "Florentin"
        self.df.loc[self.draw_mask, "winner"] = "Draw"

    @property
    def _lars_distance_to_result(self):
        return abs(self.df["lars_bet"] - self.df["result"])

    @property
    def _florentin_distance_to_result(self):
        return abs(self.df["florentin_bet"] - self.df["result"])

    @property
    def lars_winner_mask(self):
        return self._lars_distance_to_result < self._florentin_distance_to_result

    @property
    def florentin_winner_mask(self):
        return self._lars_distance_to_result > self._florentin_distance_to_result

    @property
    def draw_mask(self):
        return self._lars_distance_to_result == self._florentin_distance_to_result

    @property
    def lars_hit_mask(self):
        return self._lars_distance_to_result == 0

    @property
    def florentin_hit_mask(self):
        return self._florentin_distance_to_result == 0

    @property
    def lars_fish_mask(self):
        return self.df["lars_fish"] == 1

    @property
    def florentin_fish_mask(self):
        return self.df["florentin_fish"] == 1

    def add_points_won_each_round(self):
        self.df["florentin_points"] = 0
        self.df["lars_points"] = 0

        self._compute_total_points_for_lars()
        self._compute_total_points_for_florentin()

    def _compute_total_points_for_lars(self):
        # Set basic point
        self.df.loc[self.lars_winner_mask, "lars_points"] = 1
        # Add direct hit amount
        self.df.loc[self.lars_hit_mask, "lars_points"] = self.df.loc[
            self.lars_hit_mask, "lars_bet"
        ]
        # Add bonus first
        self.df.loc[self.lars_winner_mask, "lars_points"] += self.df.loc[
            self.lars_winner_mask, "bonus"
        ]
        # Apply fish multiplicator
        self.df.loc[self.lars_fish_mask, "lars_points"] *= 2
        # Multiplicator applied last
        self.df.loc[self.lars_winner_mask, "lars_points"] *= self.df.loc[
            self.lars_winner_mask, "multiplicator"
        ]

    def _compute_total_points_for_florentin(self):
        # Set basic point
        self.df.loc[self.florentin_winner_mask, "florentin_points"] = 1
        # Add direct hit amount
        self.df.loc[self.florentin_hit_mask, "florentin_points"] = self.df.loc[
            self.florentin_hit_mask, "florentin_bet"
        ]
        # Add bonus first
        self.df.loc[self.florentin_winner_mask, "florentin_points"] += self.df.loc[
            self.florentin_winner_mask, "bonus"
        ]
        # Apply fish multiplicator
        self.df.loc[self.florentin_fish_mask, "florentin_points"] *= 2
        # Multiplicator applied last
        self.df.loc[self.florentin_winner_mask, "florentin_points"] *= self.df.loc[
            self.florentin_winner_mask, "multiplicator"
        ]

    def _compute_total_points(
        self, winner_mask, points_column, hit_mask, bet_column, fish_mask
    ):
        self.df.loc[winner_mask, points_column] = 1
        self.df.loc[hit_mask, points_column] = self.df.loc[hit_mask, bet_column]
        self.df.loc[winner_mask, points_column] += self.df.loc[winner_mask, "bonus"]
        self.df.loc[winner_mask, points_column] *= self.df.loc[
            fish_mask, "multiplicator"
        ]
        self.df.loc[winner_mask, points_column] *= self.df.loc[
            winner_mask, "multiplicator"
        ]  # Multiplicator applied last

    def add_bet_numbering(self):
        _, amount_bets_per_episode = np.unique(self.df.index, return_counts=True)
        bet_numbering = [range(1, amount + 1) for amount in amount_bets_per_episode]
        bet_numbering = np.hstack(bet_numbering)
        self.df["bet_number"] = bet_numbering
        self.df.set_index("bet_number", inplace=True, append=True)

    def humanize_first_bet_column(self):
        self.df.loc[self.df.first_bet == "f", "first_bet"] = "Florentin"
        self.df.loc[self.df.first_bet == "l", "first_bet"] = "Lars"


class Types(Enum):
    GENERAL = "GENERAL"
    OVERVIEW = "OVERVIEW"
    CROWNS = "CROWNS"
    WINNERS = "WINNERS"
    TOTAL_POINTS = "TOTAL_POINTS"
    LARS_HIT = "LARS_HIT"
    LARS_BET = "LARS_BET"
    FLORENTIN_HIT = "FLORENTIN_HIT"
    FLORENTIN_BET = "FLORENTIN_BET"
    RESULT_FREQUENCY = "RESULT_FREQUENCY"
    BET_RESULT_DIFFERENCE = "BET_RESULT_DIFFERENCE"
    VULTURE_DATA_ORIENTED = "VULTURE_DATA_ORIENTED"
    VULTURE_CORRIDOR_DEFINITION_VULTURE = "VULTURE_CORRIDOR_DEFINITION_VULTURE"
    VULTURE_CORRIDOR_DEFINITION_SCATTER_PLOT = (
        "VULTURE_CORRIDOR_DEFINITION_SCATTER_PLOT"
    )
    OVER_OR_UNDER_ESTIMATION = "OVER_OR_UNDER_ESTIMATION"
    LOWER_SECOND_BETS = "LOWER_SECOND_BETS"
    FISH_CARD_CURSE = "FISH_CARD_CURSE"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)
