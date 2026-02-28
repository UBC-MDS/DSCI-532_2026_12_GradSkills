import numpy as np
import pandas as pd
import altair as alt
from shiny import App, render, ui, reactive, req
from shinywidgets import render_altair, render_widget, output_widget

raw_data = pd.read_csv("data/processed/processed_data.csv")

regions = sorted(raw_data["Region"].dropna().unique().tolist())
studies = sorted(raw_data["Field_of_Study"].dropna().unique().tolist())
industries = sorted(raw_data["Top_Industry"].dropna().unique().tolist())
degrees = sorted(raw_data["Degree_Level"].dropna().unique().tolist())

def render_cards_with_format(size, avg, q1, median, q3, unit_prefix="", unit_suffix=""):
    """
    This function helps data cards render more _professionally_ B)
    I did the HTML with ChatGPT because I do not have the time to
    learn how to centre divs.
    """
    return (
        f"""
            
            <div style="width: 100%; text-align: center;">

                <div style="font-size: {size}pt; margin-bottom: 6px;">
                    <br/>Average
                </div>

                <div style="font-size: {size * 2}pt; font-weight: 700; line-height: 1.1; margin-bottom: 24px;">
                    {unit_prefix}{avg:.1f}{unit_suffix}
                </div>

                <div style="
                    display: grid;
                    grid-template-columns: auto auto;
                    justify-content: center;
                    column-gap: 18px;
                    row-gap: 6px;
                    font-size: {int(size * 0.8)}pt;
                    line-height: 1.4;
                ">
                    <div style="text-align: right;">Q1:</div>
                    <div style="font-weight: 700; text-align: left;">{unit_prefix}{q1:.1f}{unit_suffix}</div>

                    <div style="text-align: right;">Median:</div>
                    <div style="font-weight: 700; text-align: left;">{unit_prefix}{median:.1f}{unit_suffix}</div>

                    <div style="text-align: right;">Q3:</div>
                    <div style="font-weight: 700; text-align: left;">{unit_prefix}{q3:.1f}{unit_suffix}</div>
                </div>

            </div>
        """
    )

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
                    "Degree Level",
                    (
                        ui.input_checkbox_group(
                            id="degree",
                            label="Degree",
                            choices=degrees,
                            selected=degrees,
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
                open=False
                
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
                sep="",
            ),
            ui.input_action_button("reset_btn", "Reset Filters"),
            width=300
        ),
        ui.layout_columns(
            ui.value_box(
                ui.div("Employment Rate (after 6 months)", class_="text-center w-100"),
                ui.output_ui("emp_rate_6")
            ),
            ui.value_box(
                ui.div("Employment Rate (after 1 year)", class_="text-center w-100"),
                ui.output_ui("emp_rate_12")
            ),
            ui.value_box(
                ui.div("Starting Annual Salary (USD)", class_="text-center w-100"),
                ui.output_ui("starting_salary")
            ),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Top Universities"),
                ui.input_action_button("clear_uni_selection", "Clear selected rows"),
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
                width=1,
                fill=True,
            ),
        ),
    ),
)


def server(input, output, session):

    @reactive.effect
    @reactive.event(input.reset_btn)
    def _reset_filters():
        ui.update_slider(
            "grad_year",
            value=[
                int(raw_data["Graduation_Year"].min()),
                int(raw_data["Graduation_Year"].max()),
            ],
        )
        ui.update_checkbox_group("region", choices=regions, selected=regions)
        ui.update_checkbox_group("study", choices=studies, selected=studies)
        ui.update_checkbox_group("industry", choices=industries, selected=industries)
        ui.update_checkbox_group("degree", choices=degrees, selected=degrees)

    @reactive.calc
    def filtered_data():
        _ = input.reset_btn()
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
        idx5 = df["Degree_Level"].isin(input.degree())

        return df[idx0 & idx1 & idx2 & idx3 & idx4 & idx5]

    @render.ui
    def emp_rate_6():
        col = display_data()["Employment_Rate_6_Months (%)"]

        size = 14   

        q1 = col.quantile(0.25)
        median = col.median()
        q3 = col.quantile(0.75)
        avg = col.mean()

        return ui.HTML(
            render_cards_with_format(
                size, avg, q1, median, q3, unit_suffix="%"
            )
        )

    @render.ui
    def emp_rate_12():
        col = display_data()["Employment_Rate_12_Months (%)"]

        size = 14

        q1 = col.quantile(0.25)
        median = col.median()
        q3 = col.quantile(0.75)
        avg = col.mean()

        return ui.HTML(
            render_cards_with_format(
                size, avg, q1, median, q3, unit_suffix="%"
            )
        )

    @render.ui
    def starting_salary():
        col = display_data()["Average_Starting_Salary_USD"]

        size = 14

        q1 = col.quantile(0.25) / 1000
        median = col.median() / 1000
        q3 = col.quantile(0.75) / 1000
        avg = col.mean() / 1000

        ## I asked ChatGPT how to tune this so that it looked nicer from the defaults
        return ui.HTML(
            render_cards_with_format(
                size, avg, q1, median, q3, unit_prefix="$", unit_suffix="K"
            )
        )

    @reactive.effect
    @reactive.event(input.region, input.reset_btn)
    def update_countries_by_region():
        filtered_by_region = raw_data[raw_data["Region"].isin(input.region())]

        countries = sorted(filtered_by_region["Country"].dropna().unique().tolist())

        ui.update_checkbox_group(
            id="country",
            choices=countries,
            selected=countries,  # select all in these regions
        )

    @reactive.calc
    def top_uni():
        data = filtered_data()

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
        data = filtered_data()
        university_idx = list(input.university_table_selected_rows())
        if not university_idx:
            return data
        selected_universities = (
            top_uni().iloc[university_idx]["University_Name"].tolist()
        )
        # print(selected_universities)
        return data[data["University_Name"].isin(selected_universities)]

    @render.data_frame
    def university_table():

        _ = input.clear_uni_selection()

        table_display = top_uni()[["rank", "University_Name", "mean_overall"]].copy()
        table_display.columns = ["Rank", "Name", "Mean Employment Rate (%)"]
        table_display["Mean Employment Rate (%)"] = table_display[
            "Mean Employment Rate (%)"
        ].round(1)

        return render.DataGrid(table_display, selection_mode="rows")

    @render_altair
    def industries_bar():
        data = display_data()

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
                y=alt.Y("Top_Industry:N", sort=None, title="Top Industry"),
                x=alt.X(
                    "avg_salary:Q",
                    title="Average Starting Salary (USD)",
                    axis=alt.Axis(format="$,.0f"),
                ),
                color=alt.Color("Top_Industry:N", title="Industry", legend=None),
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
                title="Top Industries by Average Starting Salary",
            )
        )

        return industries_bar

    @render_altair
    def study_salary_plot():
        data = display_data()

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
                x=alt.X("Graduation_Year:O", title="Year", sort="ascending"),
                y=alt.Y(
                    "avg_salary:Q",
                    title="Average Starting Salary (USD)",
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
                title="Average Starting Salary Over Time",
            )
        )

        return line_chart
    
    @reactive.calc
    def display_data():
        data = filter_data_by_university()
        req(not data.empty, cancel_output=True)
        return data


app = App(app_ui, server)
