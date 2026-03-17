import pandas as pd
from pandas.testing import assert_frame_equal

## Find the python function module source in src/, otherwise we would
## need to do some weird stuff, orrrr making it a package.
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from logic import compute_top_universities


def test_compute_top_universities_aggregates_rows_per_university():
    """
    Verifies that multiple rows for the same university are averaged before ranking,
    which matters because the dashboard should rank grouped university performance
    rather than raw rows.
    """
    data = pd.DataFrame(
        {
            "University_Name": ["Alpha", "Alpha", "Beta"],
            "Region": ["North America", "North America", "Europe"],
            "Country": ["USA", "USA", "France"],
            "Employment_Rate_6_Months (%)": [80, 100, 90],
            "Employment_Rate_12_Months (%)": [70, 90, 80],
        }
    )

    result = compute_top_universities(data)

    expected = pd.DataFrame(
        {
            "rank": [1, 1],
            "University_Name": ["Alpha", "Beta"],
            "mean_overall": [85.0, 85.0],
        }
    )

    assert_frame_equal(result.reset_index(drop=True), expected)



def test_compute_top_universities_ranks_highest_mean_first():
    """
    Verifies that universities are ranked from highest to lowest overall
    employment mean, which matters because the dashboard should surface the
    strongest-performing universities first.
    """
    data = pd.DataFrame(
        {
            "University_Name": ["Alpha", "Beta", "Gamma"],
            "Region": ["North America", "North America", "Europe"],
            "Country": ["USA", "Canada", "France"],
            "Employment_Rate_6_Months (%)": [95, 85, 75],
            "Employment_Rate_12_Months (%)": [85, 75, 65],
        }
    )

    result = compute_top_universities(data)

    expected = pd.DataFrame(
        {
            "rank": [1, 2, 3],
            "University_Name": ["Alpha", "Beta", "Gamma"],
            "mean_overall": [90.0, 80.0, 70.0],
        }
    )

    assert_frame_equal(result.reset_index(drop=True), expected)


def test_compute_top_universities_returns_empty_dataframe_for_empty_input():
    """
    Verifies that an empty input returns an empty result with the expected columns,
    which matters because the dashboard should handle no-match filter states
    gracefully.
    """
    data = pd.DataFrame(
        columns=[
            "University_Name",
            "Region",
            "Country",
            "Employment_Rate_6_Months (%)",
            "Employment_Rate_12_Months (%)",
        ]
    )

    result = compute_top_universities(data)

    expected = pd.DataFrame(columns=["rank", "University_Name", "mean_overall"])

    assert_frame_equal(result, expected)