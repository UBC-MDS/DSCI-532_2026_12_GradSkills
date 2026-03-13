# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2026-03-17

### Added

- Added packages to `requirements.txt` for lazy loading (ibis and DuckDB). @beardw

- <!-- New features, components, tests - one line each. Reference PRs where relevant (e.g. #12). -->

### Changed

- Updated `app.py` to lazy loading using parquet and DuckDB @beardw
- Refactored several parts of the codebase to account for parquet formatting of data. @beardw
- Updated `ai_tab.py` to lazy loading using parquet and DuckDB @beardw
- Moved AI Assistant tab chat sidebar to the right side of the layout for better visibility of outputs. @apoorva43
- Reordered AI Assistant tab layout so charts appear above the dataframe table. @apoorva43
- Moved Download CSV button to the right of the dataframe card header for cleaner presentation. @apoorva43
- **Addressed:** AI Assistant tab chat sidebar not static and non-intuitive layout ([#94](https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills/issues/94), [#95](https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills/issues/95)) via [#99](https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills/pull/99).
- Refactored functions for checkboxes for the filters. @harrisonlee0530

- <!-- Spec or design deviations, and motivation. -->
- <!-- Feedback items you addressed: "Addressed: <item description> (#<prioritization issue>) via #<PR>" -->

### Fixed

- Corrected any assignment of the underscore character that interferred with ibis capabilities. @beardw
- Fixed `ai_tab` import error on Posit Cloud using try/except for relative vs absolute import compatibility. @apoorva43
- Fixed missing pip dependencies (pyarrow, pyarrow-hotfix, duckdb, ibis-framework) in `environment.yml`. @apoorva43
- Removed color and y-axis label from top industries bar chart. @harrisonlee0530
- Removed animation play button for year filter slider. @harrisonlee0530
- Fixed AI Assistant tab chat sidebar to have a fixed height with internal scrolling so the input box remains visible during long conversations. @apoorva43

- **Feedback prioritization issue link:** #...

### Known Issues

- <!-- Anything incomplete or broken TAs should be aware of (so it isn't mistaken for unfinished work). -->

### Release Highlight: [Name of your advanced feature]

<!-- One short paragraph describing what you built and what it does for the user. -->

- **Option chosen:** D - Please note that this was completed during Milestone 3. We confirmed with Ilya that
this was alright. You'll note that this was the hard suggestion from the TA feedback linked below. We extended
the suggestion to make our table multi-select and update other outputs.
- **PR:** #65
- **Why this option over the others:** This was feedback provided by the TA. We also thought it aligns well with
our user stories where they may want to only select a subset of universities and compare them directly.
- **Feature prioritization issue link:** [https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills/issues/61](https://github.com/UBC-MDS/DSCI-532_2026_12_GradSkills/issues/61)

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** <!-- Link to the PR that updated it with your M3 retrospective and M4 norms. -->
- **M3 retrospective:** <!-- What changed in your workflow after M3 collaboration feedback. -->
- **M4:** <!-- What you tried or improved this milestone. -->

### Reflection

<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->

<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->

<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->

## [0.3.0] - 2026-03-08

### [0.3.0] Added

- Added a top-of-dashboard **About this dashboard** section with usage instructions and dataset limitations. @hpalafoxp
- Added **side-by-side university comparison** charts for employment rate after 6 months, employment rate after 1 year, and average starting salary. @hpalafoxp
- Added **baseline KPI comparisons** against the global average for the most recent 5 years (2021–2025). @hpalafoxp
- Added **AI assistant tab** with a querychat natural language interface for filtering the dataset. @apoorva43
- Added **filtered dataframe output** to the AI assistant tab that updates based on chat queries. @apoorva43
- Added **CSV download button** to export the querychat-filtered data. @apoorva43
- Added **Top Industries** and **Average Yearly Salary** charts to AI assistant tab that filters based on question asked and query results - from main page with stylistic updates. @beardw
- Added **Collapseable Toggle** to allow users to open or close all filters at once. @beardw
- Added **Select All** option to all checkbox filters, except for 'degree_level'. @beardw

### [0.3.0] Changed

- Changed the default graduation year filter to the **most recent 5 years**. @hpalafoxp
- Updated the reset button to restore that 5-year default view. @hpalafoxp
- Converted app layout from `page_fluid` to `page_navbar` to support multiple tabs. @apoorva43
- Moved AI tab UI and server logic into a separate `src/ai_tab.py` module for readability. @apoorva43
- Changed the layout of the AI Assistant page to have the table on left and charts stacked on right. @beardw
- Moved reset filter button to top of filters to prevent it being hidden if several filters are open. @beardw
- Made the 'About Me' description collapsed on load to prevent users from having to do this each time. @beardw

### [0.3.0] Removed

- Removed duplicated checkbox filter name that appeared when opening the dropdown. @beardw

### [0.3.0] Fixed

- Improved selected-university handling so comparison charts still render a meaningful overall view when no rows are selected. @hpalafoxp
- Bumped `shiny` to `1.5.1` in `requirements.txt` to resolve dependency conflict with `querychat==0.5.1`. @apoorva43

### [0.3.0] Known Issues

- The dataset only includes **46 universities** and covers **2015–2025** cohorts.
- Some universities appear only in certain, non-consecutive years.
- **Top Industry** is constrained by **Field of Study**.
- The baseline is a **global benchmark**, not a filter-specific peer baseline.
- Unselecting all in any one of the checkbox filters will leave dashboard blank.

### [0.3.0] Reflection

The dashboard now does a better job supporting exploration and direct comparison. Users can filter the data, compare one or more universities, and interpret results against a recent global benchmark. Current limitations come from the data set itself, including limited university coverage and uneven year availability.



## [v0.2.0] - 2026-02-28

### [0.2.0] Added

- Added `requirements.txt` to support reproducible setup and deployment on Posit Connect Cloud (both stable and dev views). @beardw
- Added `reports/m2_spec.md` with M2 documentation covering job stories, component inventory, the reactivity diagram, calculation details, and the documented interaction enhancement. @apoorva43 @hpalafoxp
- Added a ranked `Top Universities` table with selectable rows to support filtered benchmarking. @Harrisonlee0530
- Added a reset filters control to restore the default dashboard state. @Harrisonlee0530
- Added degree-level filtering in the sidebar so users can narrow outcomes by credential level. @hpalafoxp

### [0.2.0] Changed

- Reworked the dashboard layout to be easier to scan. KPI cards remain at the top, the university ranking moved from a chart to an interactive table, and the supporting charts were reorganized into a more compact layout. @beardw @hpalafoxp @Harrisonlee0530
- Upgraded the KPI summaries from simple text outputs to formatted cards showing average and quartile summaries. @beardw @hpalafoxp @Harrisonlee0530
- Expanded filtering beyond the original M1 emphasis so the dashboard now supports exploration across region, country, field of study, industry, graduation year, and degree level. @beardw @hpalafoxp @Harrisonlee0530
- Updated project documentation to reflect the implemented M2 design rather than the earlier placeholder scaffold. @hpalafoxp
- Refined dependency management by correcting the Shiny version and trimming unnecessary packages from `requirements.txt`. @beardw

### [0.2.0] Fixed

- Fixed the reset button so it properly invalidates and refreshes downstream reactive outputs. @beardw @hpalafoxp @Harrisonlee0530
- Fixed empty-filter cases so the dashboard handles empty data subsets more safely instead of failing during rendering. @hpalafoxp
- Aligned the M2 specification with the current dashboard terminology and interaction flow. @hpalafoxp @apoorva43
- Update overall layout of the table, charts, and KPI cards, change KPI wording to be more general and user understandable. @beardw

### [0.2.0] Known Issues

- The final dashboard no longer includes the dedicated degree distribution chart shown in the M1 sketch. Degree exploration is now handled primarily through filtering rather than a standalone visual comparison.

### [0.2.0] Reflection

#### [0.2.0] Job story status

- **Fully implemented:** Job Stories 2, 3, and 4 are fully implemented through linked filters, KPI summary cards, the ranked university table, and downstream chart updates.
- **Implemented differently than originally envisioned:** Job Story 1 is supported through field, geography, year, industry, and degree filtering, but the original sketch suggested a more explicit degree-focused chart. In the final build, that comparison is handled through filter-driven slicing rather than a dedicated degree visual.
- **Comparison metrics:** We might need to add a comparison metric to contrast against a baseline.

#### [0.2.0] Layout comparison to the M1 sketch and M2 spec

- Relative to the **M1 sketch**, the final layout kept the KPI summary area and the core industry and salary exploration, but changed two major pieces:
  - the **degree doughnut chart** was removed and replaced by a **degree filter** in the sidebar;
  - the **Top Universities bar chart** was replaced by an **interactive ranked DataGrid**, which provides a more useful control surface for filtering the rest of the dashboard.
- Relative to the **M2 spec**, the implemented product is more interactive than the initial draft. The specification has been updated to reflect the final filter set, the row-selection workflow, and the linked downstream outputs.
