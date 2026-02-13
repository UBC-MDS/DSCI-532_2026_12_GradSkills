import numpy as np
import pandas as pd
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, render_widget, output_widget

# import altair as alt

raw_data = pd.read_csv("data/raw/global_graduate_employability_index.csv")

regions = sorted(raw_data["Region"].dropna().unique().tolist())
studies = sorted(raw_data["Field_of_Study"].dropna().unique().tolist())
industries = sorted(raw_data["Top_Industry"].dropna().unique().tolist())


app_ui = ui.page_fluid(
    ui.panel_title("Graduate Skills Employability Dashboard"), 
    ui.layout_sidebar(
        ui.sidebar(
            ui.accordion(
                ui.accordion_panel("Region", (
                    ui.input_checkbox_group(
                        id="region",
                        label="Region",
                        choices=regions,
                        selected=regions,
                    )
                )),
                ui.accordion_panel("Country", (
                    ui.input_checkbox_group(
                        id="country", 
                        label="Country", 
                        choices=[], selected=[], 
                    )
                )), 
                ui.accordion_panel("Field of Study", (
                    ui.input_checkbox_group(
                        id="study", 
                        label="Study", 
                        choices=studies, selected=studies, 
                    )
                )), 
                ui.accordion_panel("Industry", (
                    ui.input_checkbox_group(
                        id="industry", 
                        label="Industry", 
                        choices=industries, selected=industries, 
                    )
                )), 
                open=False
            ),
            ui.input_slider(
                id="grad_year",
                label="Graduation Year",
                min=raw_data["Graduation_Year"].min(),
                max=raw_data["Graduation_Year"].max(),
                value=[raw_data["Graduation_Year"].min(), raw_data["Graduation_Year"].max()],
                step=1, ticks=True, animate=True
            ),
        ),
        ui.layout_columns(
            ui.value_box("Employment Rate 6 Month", ui.output_text("emp_rate_6")),
            ui.value_box("Employment Rate 12 Month", ui.output_text("emp_rate_12")),
            ui.value_box("Starting Salary", ui.output_text("starting_salary")),
            fill=False
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Degrees"), 
                output_widget("degrees_pie"), 
                full_screen=True
            ), 
            ui.card(
                ui.card_header("Industries"), 
                output_widget("industries_bar"), 
                full_screen=True
            ), 
        ), 
        ui.layout_columns(
            ui.card(
                ui.card_header("Top Universities"), 
                output_widget("universities_bar"), 
                full_screen=True
            ), 
            ui.card(
                ui.card_header("Yearly Starting Salary for each Field of Study"), 
                output_widget("study_salary_plot"), 
                full_screen=True
            ), 
        )
    ),
)


def server(input, output, session):

    @reactive.calc
    def filtered_data():
        df = raw_data.copy()

        # filters
        idx0 = df["Graduation_Year"].between(
            left=input.grad_year()[0],
            right=input.grad_year()[1],
            inclusive="both",
        )
        idx1 = df["Region"].isin(input.region())
        idx2 = df["Country"].isin(input.country())
        idx3 = df["Field_of_Study"].isin(input.study())
        idx4 = df["Top_Industry"].isin(input.industry())

        return df[idx0 & idx1 & idx2 & idx3 & idx4]

    @render.text
    def emp_rate_6():
        col = filtered_data()["Employment_Rate_6_Months (%)"]
        return "Max: {:.1f}%\nMin: {:.1f}%\nAverage: {:.1f}%".format(
            col.max(), col.min(), col.mean()
        )
    
    @render.text
    def emp_rate_12():
        col = filtered_data()["Employment_Rate_12_Months (%)"]
        return "Max: {:.1f}%\nMin: {:.1f}%\nAverage: {:.1f}%".format(
            col.max(), col.min(), col.mean()
        )
    
    @render.text
    def starting_salary():
        col = filtered_data()["Average_Starting_Salary_USD"]
        return "Max: {}\nMin: {}\nAverage: {:.0f}".format(
            col.max(), col.min(), col.mean()
        )

    @reactive.effect
    @reactive.event(input.region)
    def update_countries_by_region():
        filtered_by_region = raw_data[raw_data["Region"].isin(input.region())]

        countries = sorted(
            filtered_by_region["Country"].dropna().unique().tolist()
        )

        ui.update_checkbox_group(
            id="country",
            choices=countries,
            selected=countries,  # select all in these regions
        )


app = App(app_ui, server)
