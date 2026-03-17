import pandas as pd


def compute_top_universities(data: pd.DataFrame) -> pd.DataFrame:
    """Compute ranked universities by the mean of 6- and 12-month employment rates."""
    if data.empty:
        return pd.DataFrame(columns=["rank", "University_Name", "mean_overall"])

    uni_emp_summary: pd.DataFrame = data.groupby(
        ["University_Name", "Region", "Country"], as_index=False
    ).agg(
        mean_6=("Employment_Rate_6_Months (%)", "mean"),
        mean_12=("Employment_Rate_12_Months (%)", "mean"),
    )

    uni_emp_summary["mean_overall"] = uni_emp_summary[["mean_6", "mean_12"]].mean(
        axis=1
    )

    uni_emp_summary["rank"] = (
        uni_emp_summary["mean_overall"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    top_uni = pd.DataFrame(
        uni_emp_summary.sort_values(
            ["mean_overall", "University_Name"], ascending=[False, True]
        ).copy()
    )

    ordered_unis = top_uni["University_Name"].tolist()

    top_uni = top_uni.set_index("University_Name").reindex(ordered_unis).reset_index()

    return top_uni[["rank", "University_Name", "mean_overall"]]