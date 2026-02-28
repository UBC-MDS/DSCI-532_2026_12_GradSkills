# Graduate Skills Employability Dashboard

This project provides an interactive dashboard for exploring graduate employability outcomes (employment rates and starting salary) across universities, regions, fields of study, industries, and graduation years.

The repository uses a synthetic dataset modeled after common employability/rankings-style indicators (e.g., employment at 6/12 months, starting salary).

## For Users

### Who should use this dashboard?

This interactive employment analytics dashboard helps prospective students, recent graduates, career advisors, and university administrators explore graduate employment outcomes across universities, regions, fields of study, industries, and degree levels. Its purpose is to make complex, multi-dimensional employment data easier to understand with clear, interactive visualisations and summary metrics. The dashboard supports data-driven decisions about education pathways, career planning, and program benchmarking by enabling users to compare employment rates, starting salaries, top industries, and institutional performance.

### Try it yourself

Stable app: <https://019c9895-4ca7-509b-005a-24f784953ff2.share.connect.posit.cloud/>
Preview app: <preview-url>

### Demo

![Here is a demo of the dashboard:](img/demo.gif)

## For contributors

### Run locally

#### 1) Download the repository

Clone the repo and move into the project folder:

``` bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills
cd DSCI-532_2026_12_GradSkills
```

#### 2) Create and activate the conda environment

From the repository root:

``` bash
conda env create -f environment.yml
conda activate graduate_skills
```

If you already created the environment before, you can update it instead:

``` bash
conda env update -f environment.yml --prune
conda activate graduate_skills
```

#### 3) Run the dashboard

From the repository root, run:

``` bash
shiny run src/app.py
```

Shiny will print a local URL in the terminal, typically **http://127.0.0.1:8000**. Open it in your browser.

**For more details, refer to [CONTRIBUTING.md](CONTRIBUTING.md)**

### Main Contributors

- Wesley Beard
- Harrison Li
- Hector Palafox Prieto
- Apoorva Srivastava