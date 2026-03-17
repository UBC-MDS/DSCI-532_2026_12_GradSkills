"""Main file for the Graduate Skills Employability Dashboard."""

# Standard imports
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Third-party imports
import altair as alt
from dotenv import load_dotenv
import duckdb
import ibis
from ibis import _
import numpy as np
import pandas as pd

# Shiny-related imports
from shiny import App, render, ui, reactive, req
from shinywidgets import render_altair, render_widget, output_widget

try:
    from .ai_tab import ai_tab_ui, ai_tab_server  # Posit deployment
except ImportError:
    from ai_tab import ai_tab_ui, ai_tab_server  # To run code locally


load_dotenv(Path(__file__).parent.parent / ".env")

CSV = "data/processed/processed_data.csv"
OUT = "data/processed/processed_data.parquet"

duckdb.execute(
    f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
"""
)

con = ibis.duckdb.connect()
raw_data = con.read_parquet("data/processed/processed_data.parquet")

dashboard_description = Path("src/dashboard_description.md").read_text(encoding="utf-8")


def unique_values(col):
    """Returns the distinct values from a columnn of interest from a parquet format."""
    return (
        raw_data.filter(_[col].notnull())
        .select(col)
        .distinct()
        .execute()[col]
        .sort_values()
        .tolist()
    )


regions = unique_values("Region")
studies = unique_values("Field_of_Study")
industries = unique_values("Top_Industry")
degrees = unique_values("Degree_Level")
countries = unique_values("Country")


def render_metric_card(
    title,
    avg,
    q1,
    median,
    q3,
    baseline,
    unit_prefix="",
    unit_suffix="",
    threshold_pct=1.0,
    comparison_label="Global Last 5 Years",
    font_scale=0.75,
    spacing_scale=0.72,  # controls padding / margins / gaps
):
    def fmt(x):
        if pd.isna(x):
            return "-"
        return f"{unit_prefix}{x:.1f}{unit_suffix}"

    def pt(x):
        return f"{x * font_scale:.1f}pt"

    def px(x):
        return f"{x * spacing_scale:.1f}px"

    bg_color = "#8b8b8b"
    delta_line_1 = f"Same vs {comparison_label}"
    delta_line_2 = f"({fmt(baseline)})"

    if not pd.isna(avg) and not pd.isna(baseline) and baseline != 0:
        delta_pct = ((avg - baseline) / baseline) * 100

        if abs(delta_pct) < threshold_pct:
            bg_color = "#8b8b8b"
            delta_line_1 = f"Same vs {comparison_label}"
            delta_line_2 = f"({fmt(baseline)})"
        elif delta_pct > 0:
            bg_color = "#06b84f"
            delta_line_1 = f"↑ {delta_pct:+.0f}% vs {comparison_label}"
            delta_line_2 = f"({fmt(baseline)})"
        else:
            bg_color = "#ff1616"
            delta_line_1 = f"↓ {delta_pct:+.0f}% vs {comparison_label}"
            delta_line_2 = f"({fmt(baseline)})"

    # Then again, I asked ChatGPT to help me with this HTML formatting.

    return f"""
        <div style="
            width: 100%;
            min-height: {px(320)};
            background: {bg_color};
            color: white;
            border-radius: {px(34)};
            padding: {px(18)} {px(18)} {px(20)} {px(18)};
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            box-sizing: border-box;
        ">
            <div style="
                font-size: {pt(19)};
                font-weight: 500;
                line-height: 1.20;
                margin-top: {px(2)};
                margin-bottom: {px(20)};
            ">
                {title}
            </div>

            <div style="
                font-size: {pt(24)};
                font-weight: 400;
                line-height: 1.10;
                margin-bottom: {px(4)};
            ">
                Average
            </div>

            <div style="
                font-size: {pt(46)};
                font-weight: 700;
                line-height: 1.0;
                margin-bottom: {px(12)};
            ">
                {fmt(avg)}
            </div>

            <div style="
                font-size: {pt(16)};
                font-weight: 700;
                line-height: 1.20;
                margin-bottom: {px(18)};
            ">
                {delta_line_1}<br>
                <span style="
                    font-size: {pt(16)};
                    font-weight: 700;
                ">
                    {delta_line_2}
                </span>
            </div>

            <div style="
                display: grid;
                grid-template-columns: auto auto;
                justify-content: center;
                column-gap: {px(14)};
                row-gap: {px(3)};
                font-size: {pt(14)};
                line-height: 1.20;
            ">
                <div style="text-align: right; font-weight: 400;">Bottom 25%:</div>
                <div style="text-align: left; font-weight: 400;">&lt; {fmt(q1)}</div>

                <div style="text-align: right; font-weight: 400;">Median:</div>
                <div style="text-align: left; font-weight: 400;">~ {fmt(median)}</div>

                <div style="text-align: right; font-weight: 400;">Top 25%:</div>
                <div style="text-align: left; font-weight: 400;">&gt; {fmt(q3)}</div>
            </div>
        </div>
    """


# preprocess baseline metrics

last_year = raw_data.Graduation_Year.max().execute()
min_year = raw_data.Graduation_Year.min().execute()
max_year = raw_data.Graduation_Year.max().execute()

baseline_data = raw_data.filter(_.Graduation_Year == last_year)

emp_6_baseline = baseline_data["Employment_Rate_6_Months (%)"].mean().execute()
emp_12_baseline = baseline_data["Employment_Rate_12_Months (%)"].mean().execute()
salary_baseline = baseline_data["Average_Starting_Salary_USD"].mean().execute()


FOOTER = ui.p(
    "Graduate employability dashboard"
    " | Authors: Wesley Beard, Harrison Li, Hector Palafox Prieto, Apoorva Srivastava |"
    " Repository: https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills |"
    " Last updated: 2026-03-05",
    class_="text-center text-muted",
)

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Dashboard",
        ui.accordion(
            ui.accordion_panel(
                "Click to learn more about this dashboard.",
                ui.card(ui.markdown(dashboard_description)),
            ),
            open=False,
        ),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_action_button("reset_btn", "Reset Filters"),
                ui.input_switch("sidebar_switch", "Open/Close Dropdowns"),
                ui.input_slider(
                    id="grad_year",
                    label="Graduation Year",
                    min=min_year,
                    max=max_year,
                    value=[
                        max_year - 4,
                        max_year,
                    ],
                    step=1,
                    ticks=True,
                    sep="",
                ),
                ui.accordion(
                    ui.accordion_panel(
                        "Region",
                        (
                            ui.input_checkbox("region_all", "Select All", True),
                            ui.input_checkbox_group(
                                id="region",
                                label=None,
                                choices=regions,
                                selected=regions,
                            ),
                        ),
                    ),
                    ui.accordion_panel(
                        "Country",
                        (
                            ui.input_checkbox("country_all", "Select All", True),
                            ui.input_checkbox_group(
                                id="country",
                                label=None,
                                choices=countries,
                                selected=countries,
                            ),
                        ),
                    ),
                    ui.accordion_panel(
                        "Field of Study",
                        (
                            ui.input_checkbox("study_all", "Select All", True),
                            ui.input_checkbox_group(
                                id="study",
                                label=None,
                                choices=studies,
                                selected=studies,
                            ),
                        ),
                    ),
                    ui.accordion_panel(
                        "Degree Level",
                        (
                            ui.input_checkbox_group(
                                id="degree",
                                label=None,
                                choices=degrees,
                                selected=degrees,
                            )
                        ),
                    ),
                    ui.accordion_panel(
                        "Industry",
                        (
                            ui.input_checkbox("industry_all", "Select All", True),
                            ui.input_checkbox_group(
                                id="industry",
                                label=None,
                                choices=industries,
                                selected=industries,
                            ),
                        ),
                    ),
                    id="sidebar_panels",
                    open=False,
                ),
                width=300,
            ),
            ui.layout_columns(
                ui.output_ui("emp_rate_6"),
                ui.output_ui("emp_rate_12"),
                ui.output_ui("starting_salary"),
                fill=False,
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Top Universities"),
                    ui.input_action_button(
                        "clear_uni_selection", "Clear selected rows"
                    ),
                    ui.output_data_frame("university_table"),
                    full_screen=True,
                ),
                ui.layout_column_wrap(
                    ui.card(
                        ui.card_header("Average Starting Salary (USD) for Top Industries by Field"),
                        output_widget("industries_bar"),
                        full_screen=True,
                    ),
                    ui.card(
                        ui.card_header(
                            "Average Yearly Starting Salary (USD)"
                        ),
                        output_widget("study_salary_plot"),
                        full_screen=True,
                    ),
                    width=1,
                    fill=True,
                ),
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Side-by-side University comparison"),
                    ui.layout_column_wrap(
                        ui.card(
                            ui.card_header("Employment Rate (after 6 months)"),
                            output_widget("uni_emp_rate_6"),
                            full_screen=True,
                        ),
                        ui.card(
                            ui.card_header("Employment Rate (after 1 year)"),
                            output_widget("uni_emp_rate_12"),
                            full_screen=True,
                        ),
                        ui.card(
                            ui.card_header("Average Yearly Starting Salary"),
                            output_widget("uni_salary"),
                            full_screen=True,
                        ),
                    ),
                )
            ),
        ),
        FOOTER,
    ),
    ai_tab_ui(),
    title="Graduate Skills Employability Dashboard",
)


def server(input, output, session):

    ai_tab_server(input, output, session)

    def generate_uni_plot(col, col_title, col_style, col_format):

        data_source = filter_data_by_university()
        req(not data_source.empty, cancel_output=True)

        plot_data = (
            data_source[["University_Name", "Country", "Region", col]]
            .groupby(["University_Name", "Country", "Region"], as_index=False)
            .agg(avg_col=(col, "mean"))
        )

        selected_rows = list(input.university_table_selected_rows() or [])

        if not selected_rows:
            plot_data = pd.DataFrame(
                {
                    "University_Name": ["All"],
                    "Country": ["All"],
                    "Region": ["All"],
                    "avg_col": [data_source[col].mean()],
                }
            )

        req(not plot_data.empty, cancel_output=True)

        return (
            alt.Chart(plot_data)
            .mark_bar()
            .encode(
                x=alt.X("University_Name", title=""),
                y=alt.Y("avg_col" + col_style, title=""),
                color=alt.Color("University_Name", legend=None),
                tooltip=[
                    alt.Tooltip("University_Name", title="University"),
                    alt.Tooltip("Country", title="Country"),
                    alt.Tooltip("Region", title="Region"),
                    alt.Tooltip(
                        "avg_col" + col_style, title=col_title, format=col_format
                    ),
                ],
            )
            .properties(width="container", height="container", title="")
        )

    @reactive.effect
    @reactive.event(input.reset_btn)
    def _reset_filters():
        ui.update_slider(
            "grad_year",
            value=[
                raw_data.Graduation_Year.max().execute() - 4,
                raw_data.Graduation_Year.max().execute(),
            ],
        )
        ui.update_checkbox("region_all", value=True)
        ui.update_checkbox("country_all", value=True)
        ui.update_checkbox("study_all", value=True)
        ui.update_checkbox("industry_all", value=True)
        ui.update_checkbox_group("degree", choices=degrees, selected=degrees)


    @reactive.calc
    def filtered_data():
        input.reset_btn()

        return raw_data.filter(
            [
                _.Graduation_Year.between(input.grad_year()[0], input.grad_year()[1]),
                _.Region.isin(input.region()),
                _.Country.isin(input.country()),
                _.Field_of_Study.isin(input.study()),
                _.Top_Industry.isin(input.industry()),
                _.Degree_Level.isin(input.degree()),
            ]
        )

    @reactive.calc
    def display_data():
        data = filtered_data().execute()
        req(not data.empty, cancel_output=True)
        return data

    @render.ui
    def emp_rate_6():
        col = filter_data_by_university()["Employment_Rate_6_Months (%)"]

        if col.empty:
            return ui.HTML(
                render_metric_card(
                    title="Employment Rate (after 6 months)",
                    avg=np.nan,
                    q1=np.nan,
                    median=np.nan,
                    q3=np.nan,
                    baseline=emp_6_baseline,
                    unit_suffix="%",
                )
            )

        return ui.HTML(
            render_metric_card(
                title="Employment Rate (after 6 months)",
                avg=col.mean(),
                q1=col.quantile(0.25),
                median=col.median(),
                q3=col.quantile(0.75),
                baseline=emp_6_baseline,
                unit_suffix="%",
            )
        )

    @render.ui
    def emp_rate_12():
        col = filter_data_by_university()["Employment_Rate_12_Months (%)"]

        if col.empty:
            return ui.HTML(
                render_metric_card(
                    title="Employment Rate (after 1 year)",
                    avg=np.nan,
                    q1=np.nan,
                    median=np.nan,
                    q3=np.nan,
                    baseline=emp_12_baseline,
                    unit_suffix="%",
                )
            )

        return ui.HTML(
            render_metric_card(
                title="Employment Rate (after 1 year)",
                avg=col.mean(),
                q1=col.quantile(0.25),
                median=col.median(),
                q3=col.quantile(0.75),
                baseline=emp_12_baseline,
                unit_suffix="%",
            )
        )

    @render.ui
    def starting_salary():
        col = filter_data_by_university()["Average_Starting_Salary_USD"]

        if col.empty:
            return ui.HTML(
                render_metric_card(
                    title="Starting Annual Salary (USD)",
                    avg=np.nan,
                    q1=np.nan,
                    median=np.nan,
                    q3=np.nan,
                    baseline=salary_baseline / 1000,
                    unit_prefix="$",
                    unit_suffix="K",
                )
            )

        return ui.HTML(
            render_metric_card(
                title="Starting Annual Salary (USD)",
                avg=col.mean() / 1000,
                q1=col.quantile(0.25) / 1000,
                median=col.median() / 1000,
                q3=col.quantile(0.75) / 1000,
                baseline=salary_baseline / 1000,
                unit_prefix="$",
                unit_suffix="K",
            )
        )

    @reactive.calc
    def top_uni():
        data = display_data()

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

        top_uni = (
            top_uni.set_index("University_Name").reindex(ordered_unis).reset_index()
        )
        return top_uni[["rank", "University_Name", "mean_overall"]]

    @reactive.calc
    def filter_data_by_university():
        data = display_data()

        if data.empty:
            return data

        selected_rows = list(input.university_table_selected_rows() or [])
        if not selected_rows:
            return data

        current_top = top_uni()

        valid_rows = [i for i in selected_rows if 0 <= i < len(current_top)]

        if not valid_rows:
            return data

        selected_universities = current_top.iloc[valid_rows]["University_Name"].tolist()

        return data[data["University_Name"].isin(selected_universities)]

    @render.data_frame
    def university_table():
        input.clear_uni_selection()

        table_display = top_uni()[["rank", "University_Name", "mean_overall"]].copy()
        table_display.columns = ["Rank", "Name", "Mean Employment Rate (%)"]
        table_display["Mean Employment Rate (%)"] = table_display[
            "Mean Employment Rate (%)"
        ].round(1)

        return render.DataGrid(table_display, selection_mode="rows")

    @render_altair
    def industries_bar():
        data = filter_data_by_university()

        industry_salary = data.groupby("Top_Industry", as_index=False).agg(
            avg_salary=("Average_Starting_Salary_USD", "mean")
        )

        industry_salary["rank"] = (
            industry_salary["avg_salary"]
            .rank(method="dense", ascending=False)
            .astype(int)
        )

        top_industries = industry_salary.sort_values(
            "avg_salary", ascending=False
        ).copy()

        industries_bar = (
            alt.Chart(top_industries)
            .mark_bar()
            .encode(
                y=alt.Y("Top_Industry:N", sort=None, title=None),
                x=alt.X(
                    "avg_salary:Q",
                    title=None,
                    axis=alt.Axis(format="$,.0f"),
                ),
                tooltip=[
                    alt.Tooltip("rank:Q", title="Rank"),
                    alt.Tooltip("Top_Industry:N", title="Industry"),
                    alt.Tooltip(
                        "avg_salary:Q", title="Avg Salary (USD)", format="$,.2f"
                    ),
                ],
            )
            .properties(
                width="container",
                height="container",
            )
        )

        return industries_bar

    @render_altair
    def study_salary_plot():
        data = filter_data_by_university()

        salary_over_time = data.groupby(
            ["Graduation_Year", "Field_of_Study"], as_index=False
        ).agg(avg_salary=("Average_Starting_Salary_USD", "mean"))

        highlight = alt.selection_point(fields=["Field_of_Study"], bind="legend")

        ymin, ymax = (
            salary_over_time["avg_salary"].min() * 0.95,
            salary_over_time["avg_salary"].max() * 1.05,
        )

        line_chart = (
            alt.Chart(salary_over_time)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "Graduation_Year:O",
                    title=None,
                    sort="ascending",
                    axis=alt.Axis(labelAngle=0)
                    ),
                y=alt.Y(
                    "avg_salary:Q",
                    title=None,
                    axis=alt.Axis(format="$,.0f"),
                    scale=alt.Scale(domain=[ymin, ymax]),
                ),
                color=alt.Color(
                    "Field_of_Study:N",
                    title="Field of Study",
                    legend=alt.Legend(orient="top", direction="horizontal", columns=3),
                ),
                opacity=alt.condition(highlight, alt.value(1), alt.value(0.12)),
                tooltip=[
                    alt.Tooltip("Graduation_Year:O", title="Year"),
                    alt.Tooltip("Field_of_Study:N", title="Field of Study"),
                    alt.Tooltip(
                        "avg_salary:Q", title="Avg Salary (USD)", format="$,.2f"
                    ),
                ],
            )
            .add_params(highlight)
            .properties(
                width="container",
                height="container",
            )
        )

        return line_chart

    @render_altair
    def uni_emp_rate_6():

        col = "Employment_Rate_6_Months (%)"
        col_title = "Employment Rate (6 months) %"
        col_style = ":Q"
        col_format = ".2f"

        return generate_uni_plot(col, col_title, col_style, col_format)

    @render_altair
    def uni_emp_rate_12():

        col = "Employment_Rate_12_Months (%)"
        col_title = "Employment Rate (1 year) %"
        col_style = ":Q"
        col_format = ".2f"

        return generate_uni_plot(col, col_title, col_style, col_format)

    @render_altair
    def uni_salary():

        col = "Average_Starting_Salary_USD"
        col_title = "Average Starting Salary (USD)"
        col_style = ":Q"
        col_format = "$,.2f"

        return generate_uni_plot(col, col_title, col_style, col_format)

    @reactive.effect
    @reactive.event(input.sidebar_switch)
    def switch_logic():
        if input.sidebar_switch():
            ui.update_accordion("sidebar_panels", show=True)
        else:
            ui.update_accordion("sidebar_panels", show=False)

    # aware that this code needs to be refactored, however,
    # wanted concepted to be available on dashboard
    def _update_checkbox_group(select_all_input, checkbox_input, checkbox_id, choices):
        # select all
        if select_all_input:
            return ui.update_checkbox_group(checkbox_id, selected=choices)
        # deselect all if and only if all checkboxes are selected
        elif set(checkbox_input) == set(choices):
            return ui.update_checkbox_group(checkbox_id, selected=[])

    def _select_all_checkbox(checkbox_input, select_all_id, choices):
        if checkbox_input:
            # update select all checkbox based on checkbox groups
            if set(checkbox_input) == set(choices):
                return ui.update_checkbox(select_all_id, value=True)
            else:
                return ui.update_checkbox(select_all_id, value=False)

    # region
    @reactive.effect
    @reactive.event(input.region_all)
    def region_event_all():
        _update_checkbox_group(input.region_all(), input.region(), "region", regions)

    @reactive.effect
    @reactive.event(input.region)
    def region_select_all():
        _select_all_checkbox(input.region(), "region_all", regions)

    # country
    @reactive.effect
    @reactive.event(input.country_all)
    def country_event_all():
        _update_checkbox_group(input.country_all(), input.country(), "country", countries)

    @reactive.effect
    @reactive.event(input.country)
    def country_select_all():
        _select_all_checkbox(input.country(), "country_all", countries)

    # study
    @reactive.effect
    @reactive.event(input.study_all)
    def study_event_all():
        _update_checkbox_group(input.study_all(), input.study(), "study", studies)

    @reactive.effect
    @reactive.event(input.study)
    def study_select_all():
        _select_all_checkbox(input.study(), "study_all", studies)

    # industry
    @reactive.effect
    @reactive.event(input.industry_all)
    def industry_event_all():
        _update_checkbox_group(input.industry_all(), input.industry(), "industry", industries)

    @reactive.effect
    @reactive.event(input.industry)
    def industry_select_all():
        _select_all_checkbox(input.industry(), "industry_all", industries)


app = App(app_ui, server)
