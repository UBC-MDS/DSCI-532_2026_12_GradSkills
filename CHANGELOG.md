## [0.2.0] - 2026-02-28

### Added
- Added `requirements.txt` to support reproducible setup and deployment on Posit Connect Cloud.
- Added `reports/m2_spec.md` with M2 documentation covering job stories, component inventory, the reactivity diagram, calculation details, and the documented interaction enhancement.
- Added a ranked `Top Universities` table with selectable rows to support filtered benchmarking.
- Added linked exploratory visuals for top industries and yearly starting salary by field of study.
- Added a reset filters control to restore the default dashboard state.
- Added degree-level filtering in the sidebar so users can narrow outcomes by credential level.

### Changed
- Reworked the dashboard layout to be easier to scan. KPI cards remain at the top, the university ranking moved from a chart to an interactive table, and the supporting charts were reorganized into a more compact layout.
- Upgraded the KPI summaries from simple text outputs to formatted cards showing average and quartile summaries.
- Expanded filtering beyond the original M1 emphasis so the dashboard now supports exploration across region, country, field of study, industry, graduation year, and degree level.
- Updated project documentation to reflect the implemented M2 design rather than the earlier placeholder scaffold.
- Refined dependency management by correcting the Shiny version and trimming unnecessary packages from `requirements.txt`.

### Fixed
- Fixed the reset button so it properly invalidates and refreshes downstream reactive outputs.
- Fixed empty-filter cases so the dashboard handles empty data subsets more safely instead of failing during rendering.
- Aligned the M2 specification with the current dashboard terminology and interaction flow.

### Known Issues
- The final dashboard no longer includes the dedicated degree distribution chart shown in the M1 sketch. Degree exploration is now handled primarily through filtering rather than a standalone visual comparison.

### Reflection

#### Job story status
- **Fully implemented:** Job Stories 2, 3, and 4 are fully implemented through linked filters, KPI summary cards, the ranked university table, and downstream chart updates.
- **Implemented differently than originally envisioned:** Job Story 1 is supported through field, geography, year, industry, and degree filtering, but the original sketch suggested a more explicit degree-focused chart. In the final build, that comparison is handled through filter-driven slicing rather than a dedicated degree visual.
- **Pending M3:** No required M2 work appears to remain. A natural M3 extension would be restoring a dedicated degree-comparison visual if the team wants Job Story 1 represented more directly.

#### Layout comparison to the M1 sketch and M2 spec
- Relative to the **M1 sketch**, the final layout kept the KPI summary area and the core industry and salary exploration, but changed two major pieces:
  - the **degree doughnut chart** was removed and replaced by a **degree filter** in the sidebar;
  - the **Top Universities bar chart** was replaced by an **interactive ranked DataGrid**, which provides a more useful control surface for filtering the rest of the dashboard.
- Relative to the **M2 spec**, the implemented product is more interactive than the initial draft. The specification has been updated to reflect the final filter set, the row-selection workflow, and the linked downstream outputs.