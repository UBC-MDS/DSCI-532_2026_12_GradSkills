## [0.2.0] - 2026-02-28

### Added
- Added `requirements.txt` to support reproducible setup and deployment into POSIT.
- Added `reports/m2_specs.md` with M2 documentation covering job stories, component inventory, the reactivity diagram, and calculation details.
- Added a ranked `Top Universities` table with selectable rows to support filtered benchmarking.
- Added linked exploratory visuals for top industries and yearly starting salary by field of study.
- Added a reset-filters control to restore the default dashboard state.
- Added degree-level filtering in the sidebar so users can narrow outcomes by credential level.

### Changed
- Reworked the dashboard layout to be easier to scan: KPI cards remain at the top, the university ranking moved from a chart to an interactive table, and the supporting charts were reorganized into a more compact layout.
- Upgraded the KPI summaries from simple text outputs to formatted cards showing average and quartile summaries.
- Expanded filtering beyond the original M1 emphasis so the dashboard now supports broader context-based exploration across region, country, field of study, industry, graduation year, and degree level.
- Updated project documentation to reflect the implemented M2 design rather than the earlier placeholder/spec scaffold.
- Refined dependency management by correcting the Shiny version and trimming unnecessary packages from `requirements.txt`.

### Fixed
- Fixed the reset button so it properly invalidates and refreshes downstream reactive outputs.
- Fixed empty-filter cases so the dashboard handles empty data subsets more safely instead of failing during rendering.
- Restored and finalized the M2 specification document after earlier add/revert/re-add iterations.

### Known Issues
- The final dashboard no longer includes the dedicated degree distribution chart shown in the M1 sketch. Degree exploration is now primarily handled through filtering rather than a standalone visual comparison.
- Documentation terminology still needs to stay synchronized across artifacts: the code uses `degree`, while parts of the specification/history refer to `degree_level` or omit degree from the revised job story text.

### Reflection

#### Job story status
- **Fully implemented:**
  - **Job Story 2** - Compare top industries in a field through the interactive industries salary chart.
  - **Job Story 3** - Compare 6-month and 12-month employment outcomes through reactive KPI summary cards.
  - **Job Story 4** - Benchmark universities under selected filters through the ranked, selectable university table and linked downstream views.
- **Partially implemented / implemented differently than originally envisioned:**
  - **Job Story 1** - The app supports comparison through field, geography, graduation-year, industry, and degree filtering, but the original M1 sketch suggested a more explicit degree-focused visual. In the final build, that comparison is handled through filter-driven slicing rather than a dedicated degree chart.
- **Pending M3:**
  - No required M2 work appears to remain. A natural M3 extension would be restoring an explicit degree-comparison visual if the team wants Job Story 1 represented more directly.

#### Layout comparison to the M1 sketch and M2 spec
- Relative to the **M1 sketch**, the final layout kept the top KPI summary area and the core industry/salary exploration, but changed two major pieces:
  - the **degree doughnut chart** was removed and replaced by a **degree filter** in the sidebar;
  - the **Top Universities bar chart** was replaced by an **interactive ranked DataGrid**, which provides a more useful control surface for filtering the rest of the dashboard.
- Relative to the **M2 spec**, the final product is stronger and more interactive than the initial placeholder/spec draft. The spec was progressively updated to include job stories, dependencies, outputs, and calculation details, but it should continue to be kept aligned with the codebase terminology and final UI behavior.
- Under **Changed**, this means the spec should note that the final layout prioritizes linked filtering and tabular university ranking over the earlier degree-distribution visualization.

#### Key PRs and commits considered
- **PR #35 - feat: added m2_spec.md file** (Hector Palafox)
  - Key commit: `3cd5e29`
  - Established the initial M2 specification scaffold.
- **PR #36 / #40 / #41 / #42 - requirements and environment documentation** (Wes Beard)
  - Key commits: `a7308b2`, `5665b15`, `0f7729b`
  - Added `requirements.txt`, corrected the Shiny version, and removed unnecessary packages.
- **PR #43 - layout and design enhancement** (Harrison Li)
  - Key commits: `d7dd134`, `5153336`, `a46aae2`, `89f887b`, `74e9e9a`, `8c32397`, `f0bcf2e`
  - Delivered the main dashboard implementation pass: richer KPI cards, layout reorganization, top-university table, linked chart interactions, and reset control.
- **PR #44 - Diagram** (Hector Palafox)
  - Key commit: `bf30242`
  - Added diagram/spec improvements and documentation structure.
- **PR #47 - fix: fix reset filter button** (Harrison Li)
  - Key commit: `e2a522d`
  - Corrected reset-button behavior so filters properly refresh outputs.
- **PR #48 - Updated job stories and calculation details** (Apoorva Srivastava)
  - Key commits: `f1b00b4`, `7e9bd05`, `09f2e93`, `9ae54d3`, `c02a69b`, `00ff728`
  - Finalized the job story table, dependency descriptions, and calculation-detail writeup.
- **Post-PR polish on branch export** (Hector Palafox)
  - Key commits: `31972a5`, `94c98ef`, `37eee01`
  - Added the final aesthetic pass, improved empty-data handling, and updated documentation to reflect degree-related dashboard changes.

#### Contributors reflected in this release
- **Hector Palafox** - primary contributor to dashboard polish, documentation evolution, and final app safeguards.
- **Harrison Li** - primary contributor to the dashboard feature build and interaction design.
- **Apoorva Srivastava** - primary contributor to job stories, calculation details, and specification refinement.
- **Wes Beard** - primary contributor to dependency management and reproducibility/deployment setup.
