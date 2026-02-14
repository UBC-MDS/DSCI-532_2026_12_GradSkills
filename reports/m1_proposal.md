# Milestone 1 Proposal

## Section 1: Motivation and Purpose

**Our Role:** Data science consultants designing an interactive employment analytics dashboard.

**Target Audience:** Prospective students, recent graduates, career advisors, and university administrators.

We are building this dashboard for individuals who need to interpret graduate employment outcomes to support academic and career decision-making. These users include:

- Prospective students deciding on a field of study or degree level
- Recent graduates evaluating job market outcomes across industries and regions
- Career advisors guiding students using outcome-based evidence
- University administrators assessing program performance

Our role is to translate multi-dimensional employment data into an accessible and interactive visual tool that supports clear comparison and informed decision-making. 

### Problem

Graduate employment data is inherently multi-dimensional and difficult to interpret without structured exploration. Variables such as region, country, field of study, industry, degree level, graduation year, employment rates, and starting salary interact in complex ways across institutions and geographies. While the data contains valuable insights, users often struggle to answer practical questions such as:

- Does pursuing a Master's degree significantly improve employment outcomes?
- Which industries hire the largest share of graduates in a specific field of study?
- How have starting salaries evolved over time?
- Do certain universities consistently demonstrate stronger employment performance?

Without interactive filtering and summarized metrics, extracting these insights requires time-consuming manual analysis and technical expertise that many users do not possess, increasing the likelihood of decisions being made based on incomplete or misinterpreted information. 

### Solution

To address this challenge, we propose an interactive dashboard that allows users to dynamically explore employment outcomes through intuitive visualizations and filters. Multi-select dropdowns (Region, Country, Field of Study, Industry) and a graduation year slider enable users to tailor the dataset to their needs. Summary metric cards provide high-level indicators such as 6-month and 12-month employment rates and starting salary statistics. Supporting visualizations, including degree distribution, top industries, top universities, and salary trends over time, enable a thorough comparative analysis. Together, these features allow users to move seamlessly between high-level summaries and detailed comparisons, reducing cognitive overload and enabling evidence-based decision-making. 

Ultimately, the goal is to empower users to make informed choices about education pathways, institutional performance, and career planning based on clear, accessible evidence.  

## Section 2: Description of the Data

We use a dataset that models graduate employability outcomes for major universities worldwide between **2015 and 2025**. The dataset contains **3,500 rows** and **18 columns**. Each row represents an aggregated outcome record for a (University × Graduation Year × Degree Level × Field of Study × Industry/Role) combination rather than an individual student.

This structure supports our user stories (**USx**) and proposed dashboard interactions:

- **Geography & institution context** (Region, Country, University_Name) enables users to narrow comparisons to relevant locations and benchmark schools (**User Stories 3–4**).
- **Education attributes** (Degree_Level, Field_of_Study, Graduation_Year) enable comparisons across programs and time windows (especially for evaluating degree pathways; **User Story 1**).
- **Outcome metrics** (Employment_Rate_6_Months, Employment_Rate_12_Months, Average_Starting_Salary_USD) directly power the dashboard’s KPI cards and trend/benchmark charts (**User Stories 1, 3, 4**).
- **Career context** (Top_Industry, Job_Role, Skill_1–Skill_3, Skill_Demand_Score, Remote_Work_Availability, Employer_Reputation_Score) supports job-market exploration and provides explanatory signals for differences in outcomes (**User Story 2**, plus deeper drill-down/tooltip context).

The table below summarizes each variable and how it maps to user tasks and dashboard components.

| Column name | Description | Counts | Relevant info | A description of the variable | Relevance |
|---|---|---:|---|---|---|
| Country | University location country | 3500 | Distinct categories: 21 | Identifies the country where the university is based. | Sidebar geography filter; segmentation for US3/US4 comparisons. |
| Region | Broad world region | 3500 | Distinct categories: 5 | Groups each record into a global region (e.g., North America, Europe) for regional comparisons. | Primary geography filter; used to contextualize benchmarks (US3/US4). |
| University_Name | University name | 3500 | Distinct categories: 46 | The institution attended by the graduate; useful for benchmarking outcomes by university. | Powers “Top Universities” ranking/benchmark view (US4). |
| Degree_Level | Degree type completed | 3500 | Distinct categories: 3 | The level of the completed qualification (e.g., Bachelor, Master, PhD). | Drives degree distribution chart + degree comparisons (US1). |
| Field_of_Study | Academic discipline | 3500 | Distinct categories: 7 | The graduate’s study area (e.g., Computer Science, Engineering), used to compare outcomes across disciplines. | Sidebar filter; comparisons across disciplines for US1/US2/US3. |
| Graduation_Year | Graduation year | 3500 | Min: 2015.00 • Mean: 2020.02 • Median: 2020.00 • Max: 2025.00 | The year the student graduated (2015–2025), enabling time-based trend analyses. | Year range slider + time trends (US1/US2/US3). |
| Employment_Rate_6_Months (%) | Employment within 6 months | 3500 | Min: 65.50 • Mean: 85.74 • Median: 85.60 • Max: 99.00 | Percentage of graduates employed within six months after graduation. | KPI card + short-term outcome comparisons (US3). |
| Employment_Rate_12_Months (%) | Employment within 12 months | 3500 | Min: 68.00 • Mean: 90.41 • Median: 90.60 • Max: 100.00 | Percentage of graduates employed within twelve months after graduation. | KPI card + longer-term outcome comparisons (US3) and benchmarking (US4). |
| Average_Starting_Salary_USD | Starting salary (USD) | 3500 | Min: -1200.00 • Mean: 64668.00 • Median: 63900.00 • Max: 189400.00 | Average starting salary for graduates, standardized to USD for cross-country comparability. | KPI card + salary trend chart; supports ROI comparisons (US1/US2). |
| Top_Industry | Typical graduate industry | 3500 | Distinct categories: 7 | The most common industry sector graduates enter, useful for sector-level outcome comparisons. | Industry filter + “Top Industries” view (US2). |
| Job_Role | Graduate job title/role | 3500 | Distinct categories: 29 | The specific professional role associated with the outcome record (e.g., Data Analyst, Software Engineer). | Optional drill-down/tooltip context; supports “what jobs do grads get?” exploration (US2). |
| Skill_1 | Primary in-demand skill | 3500 | Distinct categories: 34 | The main skill most associated with success in the role (technical or soft skill). | Optional drill-down context; supports skill-oriented exploration (US2). |
| Skill_2 | Secondary skill | 3500 | Distinct categories: 34 | A complementary skill that supports performance and progression in the role/field. | Optional drill-down context; supports skill-oriented exploration (US2). |
| Skill_3 | Tertiary skill | 3500 | Distinct categories: 34 | An additional competency commonly linked to the job role or industry expectations. | Optional drill-down context; supports skill-oriented exploration (US2). |
| Skill_Demand_Score (1–100) | Market demand index | 3500 | Min: 30.00 • Mean: 65.19 • Median: 64.00 • Max: 100.00 | An index (1–100) approximating how strongly the labor market demands the graduate’s skill profile. | Candidate enhancement for “high demand” sectors/roles; supports US2. |
| Remote_Work_Availability (%) | Remote work availability | 3500 | Min: 5.00 • Mean: 40.06 • Median: 37.30 • Max: 90.00 | Estimated share (%) of roles in this field that offer remote work options. | Candidate enhancement for career planning; supports US2. |
| Employer_Reputation_Score (1–100) | Employer reputation score | 3500 | Min: 40.00 • Mean: 69.74 • Median: 70.00 • Max: 100.00 | A score (1–100) reflecting perceived employer reputation/standing relevant to graduate outcomes. | Candidate enhancement for benchmarking/context; supports US4. |
| Year | Analysis year index | 3500 | Min: 2015.00 • Mean: 2020.02 • Median: 2020.00 • Max: 2025.00 | Duplicates `Graduation_Year` to make time-series analysis and indexing simpler. | Implementation detail; can be dropped/ignored in the app to avoid confusion. |


## Section 3: Research Questions & Usage Scenarios

### Research Questions

- How do employment rates differ across degree levels within specific fields of study?
- Which industries employ the largest share of graduates within a selected region and time frame?
- How have starting salaries evolved over time across fields and regions? 

### Persona

Emma is a 22-year-old final-year undergraduate student in Engineering who is considering whether to pursue a Master's degree. She is evaluating job prospects across different regions and industries, and wants concrete, data-driven insights on employment rates and salary trends before making this decision.

### Usage Scenario

Emma accesses the dashboard to explore employment outcomes for Engineering graduates. She filters the data by Region (North America), Field of Study (Engineering), and Graduation Year (2018-2025). The summary cards update to display 6-month and 12-month employment rates and average starting salary. She then examines the degree distribution chart to compare employment representation between Bachelor's and Master's graduates within her field. 

Next, she explores the salary trend visualization to understand how starting salaries have evolved over time. She also reviews the Top Industries chart to identify which sectors most frequently employ Engineering graduates. By adjusting filters and comparing visual outputs, Emma is able to assess whether pursuing a Master's degree is likely to improve her employment prospects and earning potential. 

### User Stories

**User Story 1:** As a prospective graduate student, I want to filter employment outcomes by degree level and field of study, so that I can compare whether pursuing a Master's degree improves employment rates and salary.

**User Story 2:** As a student exploring job opportunities, I want to compare top industries in my field so that I can target high-demand sectors.

**User Story 3:** As a career advisor, I want to visualize employment rates at both 6 and 12 months so that I can evaluate short-term versus longer-term employment stability for graduates.

**User Story 4:** As a university administrator, I want to view top-performing universities under specific filters so that I can benchmark institutional performance. 

## Section 4: Exploratory Data Analysis

**Selected user story:** **User Story 3** — *As a career advisor, I want to visualize employment rates at both 6 and 12 months so that I can evaluate short-term versus longer-term employment stability for graduates.*

Before building the dashboard, we validated that the dataset contains meaningful information in both employment horizons:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| Employment rate (6 months) | 85.74% | 65.50% | 99.00% |
| Employment rate (12 months) | 90.41% | 68.00% | 100.00% |

This shows that employment outcomes typically improve between 6 and 12 months, but there is still substantial variation across records, therefore supporting the need for short and long-term indicators in the dashboard.

Next, we examined which institutions tend to perform best overall. The following chart ranks universities by **average employment rate (2015-2025)**, with tooltips exposing both 6 and 12-month rates. This directly motivates the dashboard’s design: KPI summary cards for both time horizons plus a “Top Universities” comparison view that can be filtered by region/country/field/industry and graduation year.

![Top universities by employment rate](../img/eda_plots/employment.png)

For better context, you can dive into our [EDA notebook](../notebooks/eda_analysis.ipynb).

## Section 5: App Sketch & Description

![App Sketch](../img/sketch.png)

This app contains several types of visualizations related to employment outcomes
of different university programs. Featured are summary statistics, trends,
and overall rankings. These are illustrated with the cards at the top that aggregate
the underlying data to provide the user with a high-level unfiltered overview.

On the left-sided sidebar, the first two filters allow the user to select
what location they are interested in - with 'Country' allowing for more granularity
when compared to 'Region'. The user can apply the subsequent two filters to select the
field and industries of their choice. The 'Graduation Year' slider provides the user
the ability to investigate different date ranges they may be interested in or, for
example, a more recent period. All filters will update the visuals on the right.

The center charts each provide a breakdown of a specific aspect of the dataset. The
doughnut chart depicts the proportion of degree levels. Additionally, there are two
bar charts to highlight popular universities and industries. And, finally, the user
will be able to gauge the starting salary trend over time.
