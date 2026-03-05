# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-03-08

### [0.3.0] Added

- Added a top-of-dashboard **About this dashboard** section with usage instructions and dataset limitations. @hpalafoxp
- Added **side-by-side university comparison** charts for employment rate after 6 months, employment rate after 1 year, and average starting salary. @hpalafoxp
- Added **baseline KPI comparisons** against the global average for the most recent 5 years (2021–2025). @hpalafoxp

### [0.3.0] Changed

- Changed the default graduation year filter to the **most recent 5 years**. @hpalafoxp
- Updated the reset button to restore that 5-year default view. @hpalafoxp

### [0.3.0] Fixed

- Improved selected-university handling so comparison charts still render a meaningful overall view when no rows are selected. @hpalafoxp

### [0.3.0] Known Issues

- The dataset only includes **46 universities** and covers **2015–2025** cohorts.
- Some universities appear only in certain, non-consecutive years.
- **Top Industry** is constrained by **Field of Study**.
- The baseline is a **global benchmark**, not a filter-specific peer baseline.

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
