# Graduate Skills Employability Dashboard

This project provides an interactive dashboard for exploring graduate employability outcomes (employment rates and starting salary) across universities, regions, fields of study, industries, and graduation years.

The repository uses a synthetic dataset modeled after common employability/rankings-style indicators (e.g., employment at 6/12 months, starting salary, employer reputation, skills in demand).

## Run locally

### 1) Download the repository

Clone the repo and move into the project folder:

``` bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills
cd DSCI-532_2026_12_GradSkills
```

### 2) Create and activate the conda environment

From the repository root:

``` bash
conda env create -f environment.yml conda activate graduate_skills
```

If you already created the environment before, you can update it instead:

``` bash
conda env update -f environment.yml --prune conda activate graduate_skills
```

### 3) Run the dashboard

From the repository root, run:

``` bash
shiny run src/app.py
```

Shiny will print a local URL in the terminal (typically [**http://127.0.0.1:8000**]{.underline}). Open it in your browser.

## Contributors

- Wesley Beard
- Harrison Li
- Hector Palafox Prieto
- Apoorva Srivastava