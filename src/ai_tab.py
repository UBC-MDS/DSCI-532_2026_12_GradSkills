"""
AI Assistant Tab for the Graduate Skills Employability Dashboard.

This module contains the querychat-powered AI tab which allows users to
filter the graduate employability dataset using natural language queries.

Setup:
Requires a .env file in the project root with the following key:
    GITHUB_TOKEN=your_github_token_here
"""

# Standard imports
from pathlib import Path
import sys

# Third-party imports
import altair as alt
from chatlas import ChatGithub
from dotenv import load_dotenv
import duckdb
import ibis
from ibis import _
import numpy as np
import pandas as pd
import querychat

# Shiny-related imports
from shiny import App, render, ui, reactive, req
from shinywidgets import render_altair, render_widget, output_widget

# Load API keys from .env (project root)
# .env should exist at the root of the directory, not inside src/
load_dotenv(Path(__file__).parent.parent / ".env")

con = ibis.duckdb.connect()
raw_data = con.read_parquet("data/processed/processed_data.parquet")

qc = querychat.QueryChat(
    raw_data.execute(),
    "graduate_employability",
    greeting="""👋 Ask me anything about graduate employability.

* <span class="suggestion">Which universities have the highest 12-month employment rate?</span>
* <span class="suggestion">Compare starting salaries across degree levels</span>
* <span class="suggestion">Filter to Technology industry graduates after 2020</span>
* <span class="suggestion">Show me PhD graduates with salary above 80000</span>
* <span class="suggestion">Which fields of study have the best 6-month employment rates?</span>
""",
    data_description="""
Graduate employability dataset with the following columns:
- Country: country of the university (21 distinct countries)
- Region: geographic region (e.g. North America, Europe etc.)
- University_Name: name of the university (46 distinct categories)
- Degree_Level: degree type completed (e.g. Bachelor, Master, PhD)
- Field_of_Study: academic discipline (e.g. Computer Science, Business, Engineering)
- Graduation_Year: year of graduation (2015-2025)
- Employment_Rate_6_Months (%): % of graduates employed within 6 months (range: 65.5-99.0)
- Employment_Rate_12_Months (%): % of graduates employed within 12 months (range: 68.0-100.0)
- Average_Starting_Salary_USD: average first-year salary in USD (range: -1200 to 189400)
- Top_Industry: most common industry graduates entered (7 distinct industries)
- Job_Role: specific professional role (e.g. Data Analyst, Software Engineer)
- Skill_1: primary in-demand skill associated with the role
- Skill_2: secondary in-demand skill
- Skill_3: tertiary in-demand skill
- Skill_Demand_Score: market demand index for the graduate's skill profile (1-100)
- Remote_Work_Availability (%): estimated share of roles offering remote work (range: 5-90)
- Employer_Reputation_Score: employer reputation score (1-100)
""",
    client=ChatGithub(model="gpt-4.1-mini"),
)

FOOTER = ui.p(
    "Graduate employability dashboard"
    " | Authors: Wesley Beard, Harrison Li, Hector Palafox Prieto, Apoorva Srivastava |"
    " Repository: https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills |"
    " Last updated: 2026-03-05",
    class_="text-center text-muted",
)


def ai_tab_ui():
    """
    Return the AI Assistant nav_panel to be added to page_navbar in app.py

    Contains the querychat sidebar for natural language filtering, a download
    button to export the filtered data as CSV, and a dataframe card showing 
    the current filtered dataset.
    """

    return ui.nav_panel(
        "AI Assistant",
        ui.page_fillable(
            ui.layout_sidebar(
                qc.sidebar(
                    width=400,
                    open="always",
                    position="right",
                    style="height: 85vh; overflow-y: auto;",
                ),
                ui.layout_columns(
                    ui.card(
                        ui.card_header(
                            ui.output_text("ai_chat_title"),
                            ui.download_button("download_data", "Download CSV"),
                        ),
                        ui.card(
                            ui.output_data_frame("ai_chat_table"),
                            full_screen=True,
                        ),
                    ),
                    ui.layout_column_wrap(
                        ui.card(
                            ui.card_header("Top Industries by Average Starting Salary (USD)"),
                            output_widget("ai_industries_bar"),
                            full_screen=True,
                        ),
                        ui.card(
                            ui.card_header("Average Yearly Starting Salary (USD)"),
                            output_widget("ai_study_salary_plot"),
                            full_screen=True
                        ),
                        width=1,
                    ),
                    col_widths=(6, 6),
                ),
            ),
            FOOTER
        ),
    )


def ai_tab_server(input, output, session):
    """
    Register all server-side logic for the AI Assistant tab.

    Calls qc.server() to initialize the querychat reactive values, then
    wires up the dataframe output, the card title, and the CSV download
    handler. Returns qc_vals so callers can access the filtered dataframe.

    Parameters
    ----------
    input, output, session: Shiny session objects
        Passed in from the main server() function in app.py

    Returns
    -------
    qc_vals: querychat reactive values
        Exposes qc_vals.df() (filtered dataframe) and qc_vals.title()
        for use in app.py if needed.
    """
    qc_vals = qc.server()

    @render.text
    def ai_chat_title():
        return qc_vals.title() or "Graduate Employability Dataset"

    @render.data_frame
    def ai_chat_table():
        return qc_vals.df()

    @render.download(filename="graduate_employability_filtered.csv")
    def download_data():
        yield qc_vals.df().to_csv(index=False)

    @render_altair
    def ai_industries_bar():
        data = qc_vals.df()

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
                x=alt.X("avg_salary:Q", title=None, axis=alt.Axis(format="$,.0f")),
                color=alt.Color("Top_Industry:N", title="Industry", legend=None),
                tooltip=[
                    alt.Tooltip("rank:Q", title="Rank"),
                    alt.Tooltip("Top_Industry:N", title="Industry"),
                    alt.Tooltip("avg_salary:Q", title="Avg Salary (USD)", format="$,.2f"),
                ],
            )
            .properties(
                width="container",
                height="container",
            )
        )

        return industries_bar

    @render_altair
    def ai_study_salary_plot():
        data = qc_vals.df()

        salary_over_time = data.groupby(
            ["Graduation_Year", "Field_of_Study"], as_index=False
        ).agg(avg_salary=("Average_Starting_Salary_USD", "mean"))

        highlight = alt.selection_point(fields=["Field_of_Study"], bind="legend")

        ymin, ymax = (
            salary_over_time["avg_salary"].min() * 0.95,
            salary_over_time["avg_salary"].max() * 1.05
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
                    legend=alt.Legend(
                        orient="top",
                        direction="horizontal",
                        columns=3
                    )
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

# Expose qc_vals so app.py can use the filtered df
    return qc_vals
