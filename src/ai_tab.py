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
- Region: geographic region (e.g. North America, Europe, Asia)
- Country: country of the university
- University_Name: name of the university
- Field_of_Study: academic discipline (e.g. Computer Science, Business, Engineering)
- Degree_Level: Bachelor, Master, PhD, MBA
- Graduation_Year: year of graduation
- Employment_Rate_6_Months (%): % of graduates employed within 6 months
- Employment_Rate_12_Months (%): % of graduates employed within 13 months
- Average_Starting_Salary_USD: average first-year salary in USD
- Top_Industry: the industry most graduates from the row entered
""",
    client=ChatGithub(model="gpt-4.1-mini"),    
)
    
def ai_tab_ui():
    """
    add docstring
    """
    return ui.nav_panel(
        "AI Assistant",
        ui.layout_sidebar(
            qc.sidebar(),
            ui.card(
                ui.card_header(ui.output_text("ai_chat_title")),
                ui.output_data_frame("ai_chat_table"),
                full_screen=True,
            ),
            fillable=True,
        ),
    )

def ai_tab_server(input, output, session):
    """
    add docstring
    """
    qc_vals = qc.server()

    @output
    @render.text
    def ai_chat_title():
        return qc_vals.title() or "Graduate Employability Dataset"
    
    @output
    @render.data_frame
    def ai_chat_table():
        return qc_vals.df()
    
    # Expose qc_vals so app.py can use the filtered df
    return qc_vals