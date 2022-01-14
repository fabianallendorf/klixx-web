import pandas as pd
import numpy as np
import json
from src.utils import NumpyEncoder


class BaseSelector:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.df = dataframe

    @property
    def data(self):
        raise NotImplementedError

    @property
    def json_data(self):
        return json.dumps(self.data, cls=NumpyEncoder)


class OverviewTable(BaseSelector):
    @property
    def data(self):
        return {
            "columns": ["Staffeln", "Episoden", "Tipps"],
            "data": [
                (
                    len(self.df.groupby(level=0)),
                    len(self.df.groupby(level=(0, 1))),
                    len(self.df.groupby(level=(0, 1, 2))),
                )
            ],
        }


class Crowns(BaseSelector):
    @property
    def data(self):
        agg_points_by_episode = self.df.groupby(["season", "episode"]).sum()
        lars_winner = (
            agg_points_by_episode["lars_points"]
            > agg_points_by_episode["florentin_points"]
        ).value_counts()[True]
        florentin_winner = (
            agg_points_by_episode["florentin_points"]
            > agg_points_by_episode["lars_points"]
        ).value_counts()[True]

        data = [lars_winner, florentin_winner]
        categories = ["Lars", "Florentin"]
        return {
            "datasets": [
                {
                    "label": "Anzahl Kronen (Gewonnene Folgen)",
                    "data": data,
                }
            ],
            "labels": categories,
        }


class WinnerCount(BaseSelector):
    @property
    def data(self):
        data = self.df["winner"].value_counts().tolist()
        categories = ["Lars", "Florentin", "Unentschieden"]
        return {
            "datasets": [
                {
                    "label": "Anzahl gewonnener Runden",
                    "data": data,
                }
            ],
            "labels": categories,
        }


class TotalPointsWon(BaseSelector):
    @property
    def data(self):
        data = [self.df.lars_points.sum(), self.df.florentin_points.sum()]
        return {
            "datasets": [
                {
                    "label": "Häufigkeit",
                    "data": data,
                }
            ],
            "labels": ["Lars", "Florentin"],
        }


class LarsHitTable(BaseSelector):
    @property
    def data(self):
        lars_hit = self.df.lars_bet == self.df.result
        hit_table = self.df.loc[lars_hit, ("lars_bet", "result")].reset_index()
        hit_table.columns = ["Staffel", "Episode", "Tipp", "Lars", "Views"]
        return hit_table.to_dict(orient="split")


class FlorentinHitTable(BaseSelector):
    @property
    def data(self):
        florentin_hit = self.df.florentin_bet == self.df.result
        hit_table = self.df.loc[
            florentin_hit, ("florentin_bet", "result")
        ].reset_index()
        hit_table.columns = ["Staffel", "Episode", "Tipp", "Florentin", "Views"]
        return hit_table.to_dict(orient="split")


class FlorentinBetCount(BaseSelector):
    @property
    def data(self):
        florentin_points_counted = self.df.florentin_bet.value_counts()
        data = florentin_points_counted.iloc[:30].to_list()
        categories = florentin_points_counted.iloc[:30].index.to_list()
        return {
            "datasets": [
                {
                    "label": "Häufigkeit",
                    "data": data,
                }
            ],
            "labels": categories,
        }


class LarsBetCount(BaseSelector):
    @property
    def data(self):
        lars_points_counted = self.df.lars_bet.value_counts()
        data = lars_points_counted.iloc[:30].to_list()
        categories = lars_points_counted.iloc[:30].index.to_list()
        return {
            "datasets": [{"label": "Häufigkeit", "data": data}],
            "labels": categories,
        }


class ResultFrequency(BaseSelector):
    @property
    def data(self):
        result_count = self.df.result.value_counts()
        data = result_count[:30].tolist()
        categories = result_count[:30].index.tolist()
        return {
            "datasets": [{"label": "Häufigkeit", "data": data}],
            "labels": categories,
        }


class BetResultDifference(BaseSelector):
    @property
    def data(self):
        bins = [0, 10, 20, 50, 80, 110, 160, 200]
        florentin_difference = abs(self.df.result - self.df.florentin_bet)
        florentin_bins, _ = np.histogram(florentin_difference, bins=bins)
        lars_difference = abs(self.df.result - self.df.lars_bet)
        lars_bins, _ = np.histogram(lars_difference, bins=bins)
        labels = [f"{bin+1} - {bins[i+1]}" for i, bin in enumerate(bins[:-1])]
        return {
            "datasets": [
                {
                    "label": "Lars Tipp Abweichung",
                    "data": lars_bins,
                },
                {
                    "label": "Florentin Tipp Abweichung",
                    "data": florentin_bins,
                },
            ],
            "labels": labels,
        }


class VultureDataOrientated(BaseSelector):
    @property
    def data(self):
        florentin_begin_and_lose = self.df.loc[
            (self.df.winner == "Lars") & (self.df.first_bet == "Florentin")
        ]

        player_bet_difference = abs(
            florentin_begin_and_lose.florentin_bet - florentin_begin_and_lose.lars_bet
        )
        lars_bet_result_difference = abs(
            florentin_begin_and_lose.result - florentin_begin_and_lose.lars_bet
        )
        lars_vulture = player_bet_difference < lars_bet_result_difference

        lars_begin_and_lose = self.df.loc[
            (self.df.winner == "Florentin") & (self.df.first_bet == "Lars")
        ]
        player_bet_difference = abs(
            lars_begin_and_lose.florentin_bet - lars_begin_and_lose.lars_bet
        )
        florentin_bet_result_difference = abs(
            lars_begin_and_lose.result - lars_begin_and_lose.florentin_bet
        )

        florentin_vulture = player_bet_difference < florentin_bet_result_difference

        data = [
            len(florentin_begin_and_lose.loc[lars_vulture]),
            len(lars_begin_and_lose.loc[florentin_vulture]),
        ]
        return {
            "datasets": [
                {
                    "label": "Häufigkeit",
                    "data": data,
                }
            ],
            "labels": ["Lars", "Florentin"],
        }


class VultureCorridorScatterPlot(BaseSelector):
    @property
    def data(self):
        scatter_data = (
            self.df.loc[:, ("lars_bet", "florentin_bet")]
            .rename(columns={"lars_bet": "x", "florentin_bet": "y"})
            .to_dict(orient="records")
        )

        first_bets = [
            "x" if first_bet == "Lars" else "y"
            for first_bet in self.df.first_bet.values
        ]

        return {
            "datasets": [
                {
                    "data": scatter_data,
                }
            ],
            "firstBets": first_bets,
        }


class VultureCorridorVulture(BaseSelector):
    @property
    def data(self):
        LIMIT_BELOW = 0.625
        LIMIT_ABOVE = 1.6

        florentin_begin = self.df.first_bet == "Florentin"
        lars_begin = self.df.first_bet == "Lars"
        florentin_below_vulture = (self.df.florentin_bet < self.df.lars_bet) & (
            self.df.florentin_bet > self.df.lars_bet * LIMIT_BELOW
        )
        florentin_above_vulture = (self.df.florentin_bet > self.df.lars_bet) & (
            self.df.florentin_bet < self.df.lars_bet * LIMIT_ABOVE
        )

        florentin_vulture = lars_begin & (
            florentin_above_vulture | florentin_below_vulture
        )

        lars_below_vulture = (self.df.lars_bet < self.df.florentin_bet) & (
            self.df.lars_bet > self.df.florentin_bet * LIMIT_BELOW
        )
        lars_above_vulture = (self.df.lars_bet > self.df.florentin_bet) & (
            self.df.lars_bet < self.df.florentin_bet * LIMIT_ABOVE
        )
        lars_vulture = florentin_begin & (lars_above_vulture | lars_below_vulture)

        data = [len(self.df.loc[lars_vulture]), len(self.df.loc[florentin_vulture])]
        return {
            "datasets": [
                {
                    "label": "Häufigkeit",
                    "data": data,
                }
            ],
            "labels": [
                "Lars",
                "Florentin",
            ],
        }


class OverUnderEstimationInfluece(BaseSelector):
    @property
    def data(self):
        lars_underestimation = self.df.lars_bet < self.df.result
        florentin_underestimation = self.df.florentin_bet < self.df.result
        florentin_winner_underestimation = (
            self.df.winner == "Florentin"
        ) & florentin_underestimation
        lars_winner_underestimation = (self.df.winner == "Lars") & lars_underestimation
        data_underestimation = [
            self.df.lars_bet[lars_winner_underestimation].count(),
            self.df.florentin_bet[florentin_winner_underestimation].count(),
        ]
        lars_overestimation = self.df.lars_bet > self.df.result
        florentin_overestimation = self.df.florentin_bet > self.df.result
        florentin_winner_overestimation = (
            self.df.winner == "Florentin"
        ) & florentin_overestimation
        lars_winner_overestimation = (self.df.winner == "Lars") & lars_overestimation
        data_overestimation = [
            self.df.lars_bet[lars_winner_overestimation].count(),
            self.df.florentin_bet[florentin_winner_overestimation].count(),
        ]

        return {
            "datasets": [
                {
                    "label": "Unterschätzt & Gewonnen",
                    "data": data_underestimation,
                },
                {
                    "label": "Überschätzt & Gewonnen",
                    "data": data_overestimation,
                },
            ],
            "labels": ["Lars", "Florentin"],
        }


class LowerSecondBets(BaseSelector):
    @property
    def data(self):
        self._add_loser_column()
        lars_begin = self.df.first_bet == "Lars"
        florentin_begin = self.df.first_bet == "Florentin"
        florentin_lower_lost = (
            lars_begin
            & (self.df.florentin_bet < self.df.lars_bet)
            & (self.df.winner == "Lars")
        )
        lars_lower_lost = (
            florentin_begin
            & (self.df.lars_bet < self.df.florentin_bet)
            & (self.df.winner == "Florentin")
        )
        florentin_lower_won = (
            lars_begin
            & (self.df.florentin_bet < self.df.lars_bet)
            & (self.df.winner == "Florentin")
        )
        lars_lower_won = (
            florentin_begin
            & (self.df.lars_bet < self.df.florentin_bet)
            & (self.df.winner == "Lars")
        )
        data_lost = self.df.loc[
            (florentin_lower_lost | lars_lower_lost), "winner"
        ].value_counts()
        data_won = self.df.loc[
            (florentin_lower_won | lars_lower_won), "winner"
        ].value_counts()

        return {
            "datasets": [
                {
                    "label": "Drunter getippt und verloren",
                    "data": data_won.astype("int32").tolist(),
                },
                {
                    "label": "Drunter getippt und gewonnen",
                    "data": data_lost.astype("int32").tolist(),
                },
            ],
            "labels": ["Lars", "Florentin"],
        }

    def _add_loser_column(self):
        self.df["loser"] = "Draw"
        self.df.loc[self.df.winner == "Florentin", "loser"] = "Lars"
        self.df.loc[self.df.winner == "Lars", "loser"] = "Florentin"


class FishCardCurse(BaseSelector):
    @property
    def data(self):
        lars_fish_card_loser = (self.df.lars_fish == 1) & (
            self.df.winner == "Florentin"
        )
        lars_fish_card_winner = (self.df.lars_fish == 1) & (self.df.winner == "Lars")
        florentin_fish_card_loser = (self.df.florentin_fish == 1) & (
            self.df.winner == "Lars"
        )
        florentin_fish_card_winner = (self.df.florentin_fish == 1) & (
            self.df.winner == "Florentin"
        )
        data_cursed = [
            len(self.df[florentin_fish_card_loser]),
            len(self.df[lars_fish_card_loser]),
        ]
        data_not_cursed = [
            len(self.df[florentin_fish_card_winner]),
            len(self.df[lars_fish_card_winner]),
        ]
        return {
            "datasets": [
                {
                    "label": "Anzahl verfluchter Fischkarte",
                    "data": data_cursed,
                },
                {
                    "label": "Anzahl erfolgreiche Fischkarte ",
                    "data": data_not_cursed,
                },
            ],
            "labels": ["Florentin", "Lars"],
        }
