from pathlib import Path
from shiny import ui, reactive, render
import querychat
from chatlas import ChatGithub
from dotenv import load_dotenv
import pandas as pd

# Load API keys from .env (project root)
load_dotenv(Path(__file__).parent.parent / ".env")

raw_data = pd.read_csv("data/processed/processed_data.csv")

qc = querychat.QueryChat(
    raw_data.copy(),
    "graduate_employability",
    greeting="""👋 Ask me anything about graduate employability.

* <span class="suggestion">Filter to Computer Science graduates</span>
* <span class="suggestion">Which universities have the highest employment rate?</span>
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
    add docstring
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
    add docstring
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