from playwright.sync_api import Page
from shiny.playwright import controller
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

## We need this to run the pytest/playwright thing from the root, and avoid
## having to do some weird stuff with imports and whatnot.
from pathlib import Path
app = create_app_fixture(
    Path(__file__).resolve().parents[1] / "src" / "app.py"
)

def test_university_table_renders_with_expected_columns(page: Page, app: ShinyAppProc):
    """
    Verifies that the ranked university table renders with the expected columns,
    because row-based university comparison depends on that table loading correctly.
    """
    page.goto(app.url)

    table = controller.OutputDataFrame(page, "university_table")
    table.expect_column_labels(["Rank", "Name", "Mean Employment Rate (%)"])
    table.expect_ncol(3)
    table.expect_cell("1", row=0, col=0)


def test_reset_button_restores_region_filter_defaults(page: Page, app: ShinyAppProc):
    """
    Verifies that the Reset Filters button restores the default region filter state,
    because users need a reliable way to return to the dashboard baseline view.
    """
    page.goto(app.url)

    table = controller.OutputDataFrame(page, "university_table")
    table.expect_column_labels(["Rank", "Name", "Mean Employment Rate (%)"])

    page.get_by_role("button", name="Region").click()

    region_all = controller.InputCheckbox(page, "region_all")
    region_group = controller.InputCheckboxGroup(page, "region")
    reset_btn = controller.InputActionButton(page, "reset_btn")
    all_regions = page.locator("#region input[type='checkbox']").evaluate_all(
        "(nodes) => nodes.map((node) => node.value)"
    )

    region_group.set(all_regions[:1])
    region_group.expect_selected(all_regions[:1])
    region_all.expect_checked(False)

    reset_btn.click()

    region_all.expect_checked(True)
    region_group.expect_selected(all_regions)


def test_clear_selected_rows_button_clears_table_selection(page: Page, app: ShinyAppProc):
    """
    Verifies that Clear selected rows removes the current university selection,
    because the comparison views should return to the overall state when no
    universities are selected.
    """
    page.goto(app.url)

    table = controller.OutputDataFrame(page, "university_table")
    table.expect_column_labels(["Rank", "Name", "Mean Employment Rate (%)"])

    clear_btn = controller.InputActionButton(page, "clear_uni_selection")

    table.select_rows([0])
    table.expect_selected_rows([0])

    clear_btn.click()
    table.expect_selected_num_rows(0)