
import numpy as np
import pandas as pd
import altair as alt
from dotenv import load_dotenv
from shiny import App, render, ui, reactive, req
from shinywidgets import render_altair, render_widget, output_widget
from pathlib import Path

from ai_tab import ai_tab_ui, ai_tab_server

load_dotenv(Path(__file__).parent.parent / ".env")

raw_data = pd.read_csv("data/processed/processed_data.csv")
dashboard_description = Path("src/dashboard_description.md").read_text(encoding="utf-8")


regions = sorted(raw_data["Region"].dropna().unique().tolist())
studies = sorted(raw_data["Field_of_Study"].dropna().unique().tolist())
industries = sorted(raw_data["Top_Industry"].dropna().unique().tolist())
degrees = sorted(raw_data["Degree_Level"].dropna().unique().tolist())

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
    spacing_scale=0.72,   # controls padding / margins / gaps
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

    ### Then again, I asked ChatGPT to help me with this HTML formatting.

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
                font-size: {pt(12)};
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


## Preprocess baseline metrics


baseline_data = raw_data.copy()
last_year = int(baseline_data["Graduation_Year"].max())

baseline_data = baseline_data[baseline_data["Graduation_Year"] > last_year - 5]

emp_6_baseline = baseline_data["Employment_Rate_6_Months (%)"].mean()
emp_12_baseline = baseline_data["Employment_Rate_12_Months (%)"].mean()
salary_baseline = baseline_data["Average_Starting_Salary_USD"].mean()




app_ui = ui.page_navbar(
    #ui.nav_title("Dashboard"),
    ui.accordion(
        ui.accordion_panel(
            "About this dashboard",
            ui.card(
                ui.markdown(dashboard_description)
            ),
        ),
    ),
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
                    raw_data["Graduation_Year"].max() - 4,
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
            ui.output_ui("emp_rate_6"),
            ui.output_ui("emp_rate_12"),
            ui.output_ui("starting_salary"),
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
                )
            )
        )
    ),
    ai_tab_ui(),
    title="Graduate Skills Employability Dashboard",
    footer=ui.p(
        (
            "Graduate employability dashboard"
            " | Authors: Wesley Beard, Harrison Li, Hector Palafox Prieto, Apoorva Srivastava |"
            " Repository: https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills |"
            " Last updated: 2026-02-28"
        ),
        class_="text-center text-muted",
    )
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
            plot_data = pd.DataFrame({
                "University_Name": ["All"],
                "Country": ["All"],
                "Region": ["All"],
                "avg_col": [data_source[col].mean()]
            })

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
                    alt.Tooltip("avg_col" + col_style, title=col_title, format=col_format),
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
                int(raw_data["Graduation_Year"].max() - 4),
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

    @reactive.calc
    def display_data():
        data = filter_data_by_university()
        req(not data.empty, cancel_output=True)
        return data


app = App(app_ui, server)
