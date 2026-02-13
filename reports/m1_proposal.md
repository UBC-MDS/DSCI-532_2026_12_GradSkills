# Milestone 1 Proposal

## Section 1: Motivation and Purpose

**Our Role:** Data science consultants designing an interactive employment analytics dashboard.

**Target Audience:** Prospective students, recent graduates, career advisors, and university administrators.

We are building this dashboard for individuals who need to interpret graduate employment outcomes to support academic and career decision-making. These users include:

- Prospective students deciding on a field of study or degree level
- Recent graduates evaluating job market outcomes across industries and regions
- Career advisors guiding students using outcome-based evidence
- University administrators assessing program performance

Our role is to translate multi-dimensional employment data into an accessible and interactive visual tool.

### Problem

Graduate employment data is inherently multi-dimensional and difficult to interpret without structured exploration. Variables such as region, country, field of study, industry, degree level, graduation year, employment rates, and starting salary interact in complex ways. While the data contains valuable insights, users often struggle to answer practical questions such as:

- Does pursuing a Master's degree significantly improve employment outcomes?
- Which industries hire the largest share of graduates in a specific field of study?
- How have starting salaries evolved over time?
- Do certain universities consistently demonstrate stronger employment performance?

Without interactive filtering and summarized metrics, extracting these insights requires time-consuming manual analysis and technical expertise that many users do not possess. 

### Solution

To address this challenge, we propose an interactive dashboard that allows users to dynamically explore employment outcomes through intuitive visualizations and filters. Multi-select dropdowns (Region, Country, Field of Study, Industry) and a graduation year slider enable users to tailor the dataset to their needs. Summary metric cards provide high-level indicators such as 6-month and 12-month employment rates and starting salary statistics. Supporting visualizations, including degree distribution, top industries, top universities, and salary trends over time, enable a thorough comparative analysis.

Ultimately, the goal is to empower users to make informed choices about education pathways, institutional performance, and career planning based on clear, accessible evidence.  

## Section 2: Description of the Data

## Section 3: Research Questions & Usage Scenarios

### Persona

Emma, a 22-year old final-year undergraduate student in Engineering, is considering whether to pursue a Master's degree, and is evaluating job prospects across different regions and industries. Emma wants concrete, data=driven insights on employment rates and salary trends before making this decision.

### Usage Scenario

Emma accesses the dashboard to explore employment outcomes for Engineering graduates. She filters the data by Region (North America), Field of Study (Engineering), and Graduation Year (2018-2025). The summary cards update to display 6-month and 12-month employment rates and average starting salary. She then examines the degree distribution chart to compare Bachelor's and Master's representation within her field. 

Next, she explores the salary trend visualization to understand how starting salaries have evolved over time. She also reviews the Top Industries chart to identify which sectors most frequently employ Engineering graduates. By adjusting filters and comparing visual outputs, Emma is able to assess whether pursuing a Master's degree is likely to improve her employment prospects and earning potential. 

### User Stories

**User Story 1:** As a prospective graduate student, I want to filter employment outcomes by degree level and field of study, so that I can compare whether pursuing a Master's degree improves employment rates and salary.

**User Story 2:** As a student exploring job opportunities, I want to compare top industries in my field so that I can target high-demand sectors.

**User Story 3:** As a career advisor, I want to visualize employment rates at both 6 and 12 months so that I can evaluate short-term versus longer-term employment stability for graduates.

**User Story 4:** As a university administrator, I want to view top-performing universities under specific filters so that I can benchmark institutional performance. 

## Section 4: Exploratory Data Analysis

## Section 5: App Sketch & Description

![App Sketch](../img/dashboard-mockup-commentary.png)

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
