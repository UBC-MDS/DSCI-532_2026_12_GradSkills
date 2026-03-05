"""
AI Assistant Tab for the Graduate Skills Employability Dashboard.

This module contains the querychat-powered AI tab which allows users to
filter the graduate employability dataset using natural language queries.

Setup: 
Requires a .env file in the project root with the following key:
    GITHUB_TOKEN=your_github_token_here
"""


from pathlib import Path
from shiny import ui, render
import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
import pandas as pd

# Load API keys from .env (project root)
# .env should exist at the root of the directory, not inside src/
load_dotenv(Path(__file__).parent.parent / ".env")

raw_data = pd.read_csv("data/processed/processed_data.csv")

qc = querychat.QueryChat(
    raw_data.copy(),
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
        ui.layout_sidebar(
            qc.sidebar(),
            ui.download_button("download_data", "Download filtered data as CSV"),
            ui.card(
                ui.card_header(ui.output_text("ai_chat_title")),
                ui.output_data_frame("ai_chat_table"),
                full_screen=True,
            ),
            fillable=True,
        ),
        FOOTER,
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
    
    # Expose qc_vals so app.py can use the filtered df
    return qc_vals