import pandas as pd
import pathlib
import argparse
from src.utils import StatEnhancer, Types
import src.selectors as selectors
from sqlite3 import connect


parser = argparse.ArgumentParser()
parser.add_argument("datapath", type=pathlib.Path)
args = parser.parse_args()
data = pd.read_csv(args.datapath, index_col=("season", "episode"))
enhancer = StatEnhancer(data)
df = enhancer.df

connection = connect("./src/assets/klixx.sqlite")
cursor = connection.cursor()

selector_list = [
    (selectors.OverviewTable, Types.OVERVIEW),
    (selectors.Crowns, Types.CROWNS),
    (selectors.WinnerCount, Types.WINNERS),
    (selectors.TotalPointsWon, Types.TOTAL_POINTS),
    (selectors.LarsHitTable, Types.LARS_HIT),
    (selectors.LarsBetCount, Types.LARS_BET),
    (selectors.FlorentinHitTable, Types.FLORENTIN_HIT),
    (selectors.FlorentinBetCount, Types.FLORENTIN_BET),
    (selectors.ResultFrequency, Types.RESULT_FREQUENCY),
    (selectors.BetResultDifference, Types.BET_RESULT_DIFFERENCE),
    (selectors.VultureDataOrientated, Types.VULTURE_DATA_ORIENTED),
    (selectors.VultureCorridorVulture, Types.VULTURE_CORRIDOR_DEFINITION_VULTURE),
    (
        selectors.VultureCorridorScatterPlot,
        Types.VULTURE_CORRIDOR_DEFINITION_SCATTER_PLOT,
    ),
    (selectors.OverUnderEstimationInfluece, Types.OVER_OR_UNDER_ESTIMATION),
    (selectors.LowerSecondBets, Types.LOWER_SECOND_BETS),
    (selectors.FishCardCurse, Types.FISH_CARD_CURSE),
]

for selector, type in selector_list:
    cursor.execute(
        "INSERT INTO klixx VALUES (null, ?, (SELECT id from types where value=?), CURRENT_TIMESTAMP)",
        [selector(df).json_data, type.value],
    )
connection.commit()
