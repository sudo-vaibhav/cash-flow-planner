import json

import altair as alt
import pandas as pd
import streamlit as st

from flow_prediction.app.use_cases.simulation import CashflowSimulationUseCase
from flow_prediction.app.use_cases.simulation.samples import bachelor_for_life


def getSessionData():
    if "data" not in st.session_state:
        st.session_state["data"] = bachelor_for_life
    return st.session_state["data"]


def mutateSessionData(data: dict):
    st.session_state["data"] = {
        **getSessionData(),
        **data,
    }


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------


def get_remaining_money(simulation):
    """Compute remaining money (both nominal and inflation-adjusted)
    from the last year’s corpus in the simulation."""
    last_year = simulation[-1]
    remaining = sum(corpus["value"]["amount"] for corpus in last_year["corpora"])
    inflation_adjusted = sum(
        corpus["value"]["inflationAdjusted"] for corpus in last_year["corpora"]
    )
    return remaining, inflation_adjusted


def run_simulation(data):
    """Run the cashflow simulation use case using the provided data."""
    result = CashflowSimulationUseCase(data).execute()
    return result


def prepare_corpus_df(simulation):
    """Flatten simulation corpus data into a DataFrame for charting."""
    corpus_info = []
    for year_data in simulation:
        year = year_data["year"]
        for corpus in year_data["corpora"]:
            corpus_info.append(
                {
                    "id": corpus["id"],
                    "year": year,
                    "value": corpus["value"]["amount"],
                }
            )
    return pd.DataFrame(corpus_info)


def expense_editor(expenses, corpora):
    """
    Display a form where the user can select an expense (or add a new one)
    and update its properties (enabled, start/end years, initial and recurring values).
    Returns the updated list of expenses.
    """
    st.header("Expense Editor")

    with st.form("expense_form", clear_on_submit=True):
        expense_id = st.text_input("Expense ID")
        enabled = st.checkbox("Enabled")
        start_year = st.number_input(
            "Start Year",
            min_value=1900,
            max_value=3000,
            step=1,
        )
        end_year = st.number_input(
            "End Year",
            min_value=1900,
            max_value=3000,
            step=1,
        )
        growth_rate = st.number_input(
            "Growth Rate",
            min_value=0.0,
            max_value=10.0,
            step=0.01,
            format="%.2f",
        )
        initial_value = st.number_input(
            "Initial Value",
            step=1000,
        )
        recurring_value = st.number_input(
            "Recurring Value",
            step=1000,
        )
        funding_corpora = st.multiselect(
            "Funding Corpora",
            options=[corp["id"] for corp in corpora],
        )
        submitted = st.form_submit_button("Save Expense")

    if submitted:
        updated_expense = {
            "id": expense_id,
            "startYear": int(start_year),
            "endYear": int(end_year),
            "enabled": enabled,
            "growthRate": growth_rate,
            "initialValue": {"amount": initial_value, "referenceTime": 2025},
            "recurringValue": {"amount": recurring_value, "referenceTime": 2025},
            "fundingCorpora": list(map(lambda x: {"id": x}, funding_corpora)),
        }
        # Update the selected expense
        for i, exp in enumerate(expenses):
            if exp["id"] == expense_id:
                expenses[i] = updated_expense
                st.toast(f"Updated expense '{expense_id}'.")
                break
        else:
            expenses.append(updated_expense)
            st.toast(f"Added new expense '{expense_id}'.")

        mutateSessionData({"expenses": expenses})
    # return expenses


def corpora_editor(corpora):
    st.header("Corpora Editor")
    corpus_ids = [corp["id"] for corp in corpora]

    # Prepare a default corpus template.
    default_corpus = {
        "id": "",
        "growthRate": 0.00,
        "startYear": 2025,
        "endYear": 2100,
        "initialAmount": 0,
    }

    with st.form("corpus_form"):
        corpus_id = st.text_input("Corpus ID")
        growth_rate = st.number_input(
            "Growth Rate",
            min_value=0.0,
            max_value=10.0,
            step=0.01,
            format="%.2f",
        )
        start_year = st.number_input(
            "Start Year",
            min_value=1900,
            max_value=3000,
            step=1,
        )
        end_year = st.number_input(
            "End Year",
            min_value=1900,
            max_value=3000,
            step=1,
        )
        initial_amount = st.number_input(
            "Initial Amount",
            step=1000,
        )
        submitted = st.form_submit_button("Save Corpus")
    if submitted:
        updated_corpus = {
            "id": corpus_id,
            "growthRate": growth_rate,
            "startYear": int(start_year),
            "endYear": int(end_year),
            "initialAmount": initial_amount,
        }
        for i, corp in enumerate(corpora):
            if corp["id"] == corpus_id:
                corpora[i] = updated_corpus
                st.success(f"Updated corpus '{corpus_id}'.")
                break
        else:
            corpora.append(updated_corpus)
            st.success(f"Added new corpus '{corpus_id}'.")
        mutateSessionData({"corpora": corpora})


def cashFlowEditor(cashflows):
    """
    Display a form to edit allocations (i.e. how cashflows are distributed over corpora)
    for a selected cashflow. For each allocation period, the user can adjust the start/end
    years and the splits (corpus & ratio). User can also mark splits or entire allocation
    periods for deletion.
    Returns the updated cashflows list.
    """
    st.header("Allocations Editor")
    with st.form("allocation_form"):
        cashflow = st.selectbox(
            "Select Cashflow to Edit Allocations",
            options=["Add New Cashflow"] + list(map(lambda x: x["id"], cashflows)),
        )

        cashflowSetting = st.text_area(
            label="Cashflow Settings",
            value=json.dumps(
                next((cf for cf in cashflows if cf["id"] == cashflow), {})
            ),
        )
        submitted = st.form_submit_button("Save Allocations")
    if submitted:
        updated_cashflow = json.loads(cashflowSetting)
        for i, cf in enumerate(cashflows):
            if cf["id"] == updated_cashflow["id"]:
                cashflows[i] = updated_cashflow
                st.toast(f"Updated cashflow '{updated_cashflow['id']}'.")
                break
        else:
            cashflows.append(updated_cashflow)
            st.toast(f"Added new cashflow '{updated_cashflow['id']}'.")
        mutateSessionData({"cashflows": cashflows})


# ------------------------------------------------------------------------------
# Main App
# ------------------------------------------------------------------------------


def main():
    st.set_page_config(layout="wide", page_title="Die With Zero Calculator")
    st.title("Die With Zero Calculator")

    # Use the sample data as a baseline.
    data = getSessionData()

    formCol1, formCol2 = st.columns(2)
    with formCol1:
        expense_editor(
            data.get("expenses", []),
            data.get("corpora", []),
        )
    with formCol2:
        corpora_editor(data.get("corpora", []))
        cashFlowEditor(
            data.get("cashflows", []),
        )
    # Run the simulation with the current (possibly modified) sample data.
    simulation_result = run_simulation(data)
    simulation = simulation_result.get("simulation", [])
    warnings = simulation_result.get("warnings", [])

    # Prepare and display the main investment stacked area chart.
    corpus_df = prepare_corpus_df(simulation)
    area_chart = (
        alt.Chart(corpus_df)
        .mark_area()
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value", stack="zero"),
            color=alt.Color("id:N", title="Corpus"),
        )
        .properties(width=700, height=400, title="Investment Stacked Area Chart")
    )

    col_left, col_right = st.columns([2, 1])
    col_left.altair_chart(area_chart, use_container_width=True)

    # Display warnings (only first 3 by default; option to show all).
    show_all = col_right.checkbox(f"Show All Warnings ({len(warnings)})", value=False)
    warnings_to_show = warnings if show_all else warnings[:3]
    for warn in warnings_to_show:
        col_right.error(warn, icon="🚨")

    # Show remaining money info.
    remaining, inflation_adjusted = get_remaining_money(simulation)
    st.warning(
        f"You finished with {remaining} extra, ({inflation_adjusted} in {data['simulation']['startYear']} terms)"
    )

    # ------------------------------------------------------------------------------
    # Additional Panels: Expenses, Allocation Pie, and Corpus Analysis
    # ------------------------------------------------------------------------------

    col_expenses, col_allocations, col_corpus = st.columns(3)
    with col_expenses:
        showExpenses(data)

    # Allocation Pie Chart.
    applicable_years = list(
        range(
            data["simulation"]["startYear"],
            data["simulation"]["endYear"] + 1,
        )
    )
    analysis_year = col_allocations.selectbox(
        "Select Year for Allocation", options=applicable_years, index=0
    )
    year_data = next(item for item in simulation if item["year"] == analysis_year)
    allocations = year_data.get("cashflowAllocations", [])

    # Build pie chart data.
    pie_data = [
        {
            "id": f"{allocation.get('id', 'split')}-{corpus.get('id', '')}",
            "value": corpus.get("value", 0),
        }
        for allocation in allocations
        for corpus in allocation.get("corpora", [])
    ]
    allocation_df = pd.DataFrame(pie_data)
    col_allocations.write("## Allocation Pie Chart")
    if allocation_df.empty:
        col_allocations.warning(
            "No cashflow allocation for this year, are you retired?"
        )
    else:
        pie_chart = (
            alt.Chart(allocation_df)
            .mark_arc()
            .encode(
                theta=alt.Theta(field="value", type="quantitative"),
                color=alt.Color(field="id", type="nominal", title="Corpus"),
                tooltip=["id", "value"],
            )
            .properties(width=400, height=400, title=f"Allocation for {analysis_year}")
        )
        col_allocations.altair_chart(pie_chart, use_container_width=True)
    col_corpus.write("## Corpus Bird's Eye")

    year_under_corpus_analysis = col_corpus.selectbox(
        "Select Year for Corpus Analysis",
        options=applicable_years,
        index=len(applicable_years) - 1,
    )

    # Get the data for that year
    corpus_data_of_year = next(
        (d for d in simulation if d["year"] == year_under_corpus_analysis), {}
    ).get("corpora", [])

    # Convert to a DataFrame
    df_corpus = pd.DataFrame(
        [
            {
                "Corpus": corpus["id"],
                "Amount": corpus["value"].get("amount", 0),
                "Inflation Adjusted": corpus["value"].get("inflationAdjusted", 0),
            }
            for corpus in corpus_data_of_year
        ]
    )

    # Display a nice table of corpora
    col_corpus.write("### Corpus Table")
    if not df_corpus.empty:
        col_corpus.dataframe(
            df_corpus.style.format(
                {"Amount": "{:,.2f}", "Inflation Adjusted": "{:,.2f}"}
            )
        )
    else:
        col_corpus.info("No corpus data found for this year.")

    # Display a bar chart (horizontal) of amounts
    if not df_corpus.empty:
        chart = (
            alt.Chart(df_corpus)
            .mark_bar()
            .encode(
                y=alt.Y("Corpus:N", sort="-x"),
                x=alt.X("Amount:Q", title="Corpus Amount"),
                tooltip=["Corpus", "Amount", "Inflation Adjusted"],
            )
            .properties(
                width=450,
                height=300,
                title=f"Corpora for Year {year_under_corpus_analysis}",
            )
        )
        col_corpus.altair_chart(chart, use_container_width=True)

    # ------------------------------------------------------------------------------
    # Display the current sample data in one collapsed expander.
    # ------------------------------------------------------------------------------
    with st.expander("Current Sample Data", expanded=False):
        st.json(getSessionData())
    with st.form("override-data"):
        st.write("## Override Sample Data")
        data_json = st.text_area(
            "Data JSON",
            value=json.dumps(getSessionData(), indent=2),
            height=400,
        )
        if st.form_submit_button("Update Sample Data"):
            try:
                new_data = json.loads(data_json)
                mutateSessionData(new_data)
                st.success("Sample data updated successfully.")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")


def showExpenses(data):
    st.write("## Expenses")
    for expenseIdx, expense in enumerate(data["expenses"]):
        # Create two columns: one for the content and one for the button.
        col_text, col_button = st.columns([3, 1])

        with col_text:
            content = f"""**{expense["id"]} ({"enabled" if expense["enabled"] else "disabled"}) (from {expense["startYear"]} to {expense["endYear"]})**  
Initial Cost: {expense["initialValue"]["amount"]}  
Recurring Cost: {expense["recurringValue"]["amount"]} (≈ {expense["recurringValue"]["amount"] / 12:.2f} per month)\n
Growth Rate: {expense["growthRate"]}\n
Funding: {", ".join(corp["id"] for corp in expense["fundingCorpora"])}
            """
            if expense["enabled"]:
                st.success(content)
            else:
                st.error(content)

        with col_button:
            # Display a single button based on the current state.
            if expense["enabled"]:
                st.button(
                    "Disable",
                    key=f"disable-{expense['id']}",
                    on_click=lambda idx=expenseIdx: setExpenseEnabled(idx, False),
                )
            else:
                st.button(
                    "Enable",
                    key=f"enable-{expense['id']}",
                    on_click=lambda idx=expenseIdx: setExpenseEnabled(idx, True),
                )


def setExpenseEnabled(expenseIdx, enabled):
    data = getSessionData()
    data["expenses"][expenseIdx]["enabled"] = enabled
    mutateSessionData({"expenses": data["expenses"]})


if __name__ == "__main__":
    main()
