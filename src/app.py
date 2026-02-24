import numpy as np
import pandas as pd
import altair as alt
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, render_widget, output_widget

raw_data = pd.read_csv("data/processed/processed_data.csv")

regions = sorted(raw_data["Region"].dropna().unique().tolist())
studies = sorted(raw_data["Field_of_Study"].dropna().unique().tolist())
industries = sorted(raw_data["Top_Industry"].dropna().unique().tolist())

app_ui = ui.page_fluid(
    ui.panel_title("Graduate Skills Employability Dashboard"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.accordion(
                ui.accordion_panel(
                    "Region",
                    (
                        ui.input_checkbox_group(
                            id="region",
                            label="Region",
                            choices=regions,
                            selected=regions,
                        )
                    ),
                ),
                ui.accordion_panel(
                    "Country",
                    (
                        ui.input_checkbox_group(
                            id="country",
                            label="Country",
                            choices=[],
                            selected=[],
                        )
                    ),
                ),
                ui.accordion_panel(
                    "Field of Study",
                    (
                        ui.input_checkbox_group(
                            id="study",
                            label="Study",
                            choices=studies,
                            selected=studies,
                        )
                    ),
                ),
                ui.accordion_panel(
                    "Industry",
                    (
                        ui.input_checkbox_group(
                            id="industry",
                            label="Industry",
                            choices=industries,
                            selected=industries,
                        )
                    ),
                ),
                open=False,
            ),
            ui.input_slider(
                id="grad_year",
                label="Graduation Year",
                min=raw_data["Graduation_Year"].min(),
                max=raw_data["Graduation_Year"].max(),
                value=[
                    raw_data["Graduation_Year"].min(),
                    raw_data["Graduation_Year"].max(),
                ],
                step=1,
                ticks=True,
                animate=True,
            ),
        ),
        ui.layout_columns(
            ui.value_box("Employment Rate 6 Month", ui.output_ui("emp_rate_6")),
            ui.value_box("Employment Rate 12 Month", ui.output_ui("emp_rate_12")),
            ui.value_box("Starting Salary", ui.output_ui("starting_salary")),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Top Universities"),
                ui.output_data_frame("university_table"),
                full_screen=True,
            ),
            ui.layout_column_wrap(
                ui.card(
                    ui.card_header("Industries"),
                    output_widget("industries_bar"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Yearly Starting Salary for each Field of Study"),
                    output_widget("study_salary_plot"),
                    full_screen=True,
                ),
                fill=True,
            ),
        ),
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

    @render.ui
    def emp_rate_6():
        col = filtered_data()["Employment_Rate_6_Months (%)"]
        return ui.HTML(
            """
                       <div style="font-size: 16pt;line-height:1.5;">
                       Q1: {:.1f}%<br/>
                       median: {:.1f}%<br/>
                       Q3: {:.1f}%<br/>
                       mean: {:.1f}%
                       </div>
                       """.format(
                col.quantile(0.25), col.median(), col.quantile(0.75), col.mean()
            )
        )

    @render.ui
    def emp_rate_12():
        col = filtered_data()["Employment_Rate_12_Months (%)"]
        return ui.HTML(
            """
                       <div style="font-size: 16pt;line-height:1.5;">
                       Q1: {:.1f}%<br/>
                       median: {:.1f}%<br/>
                       Q3: {:.1f}%<br/>
                       mean: {:.1f}%
                       </div>
                       """.format(
                col.quantile(0.25), col.median(), col.quantile(0.75), col.mean()
            )
        )

    @render.ui
    def starting_salary():
        col = filtered_data()["Average_Starting_Salary_USD"]
        return ui.HTML(
            """
                       <div style="font-size: 16pt; line-height:1.5;">
                       Q1: {:.1f}<br/>
                       median: {:.1f}<br/>
                       Q3: {:.1f}<br/>
                       mean: {:.1f}
                       </div>
                       """.format(
                col.quantile(0.25), col.median(), col.quantile(0.75), col.mean()
            )
        )

    @reactive.effect
    @reactive.event(input.region)
    def update_countries_by_region():
        filtered_by_region = raw_data[raw_data["Region"].isin(input.region())]

        countries = sorted(filtered_by_region["Country"].dropna().unique().tolist())

        ui.update_checkbox_group(
            id="country",
            choices=countries,
            selected=countries,  # select all in these regions
        )

    @render.data_frame
    def university_table():
        data = filtered_data()
        if data.empty:
            return render.DataGrid(
                pd.DataFrame(columns=["Name", "Rank", "Mean Employment Rate (%)"])
            )

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

        top50 = pd.DataFrame(
            uni_emp_summary.sort_values(
                ["mean_overall", "University_Name"], ascending=[False, True]
            )
            .head(50)
            .copy()
        )

        ordered_unis = top50["University_Name"].tolist()

        top50 = top50.set_index(
            "University_Name"
        ).reindex(ordered_unis).reset_index()

        table_display = top50[
            ["University_Name", "rank", "mean_overall"]
        ].copy()
        table_display.columns = ["Name", "Rank", "Mean Employment Rate (%)"]
        table_display["Mean Employment Rate (%)"] = table_display[
            "Mean Employment Rate (%)"
        ].round(1)

        return render.DataGrid(table_display, selection_mode="rows")


app = App(app_ui, server)
