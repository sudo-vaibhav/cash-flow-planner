import json

import pandas as pd
import streamlit as st
import altair as alt
from flow_prediction.app.use_cases.simulation import CashflowSimulationUseCase
from flow_prediction.app.use_cases.simulation.samples import (
    vaibhav_sample_data,
)
v = json.loads(st.text_area(label="Custom JSON") or "{}")

bt = st.button("Run Simulation")
if bt:
    result = CashflowSimulationUseCase(v).execute()
    simulation = result["simulation"]
    warnings = result["warnings"]
    corpusInfo = []

    for yearData in simulation:
        for corpus in yearData["corpora"]:
            corpusInfo.append({
                "id": corpus["id"],
                "year": yearData["year"],
                "value": corpus["value"],
            })
    # for category, entries in simulation.items():
    #
    #     for entry in entries:
    #         row = {
    #             "category": category,
    #             "year": entry["year"],
    #             "value": entry["value"],
    #         }
    #         # Add a new key to indicate the category/fund type
    #
    #         corpusInfo.append(row)
    #
    df = pd.DataFrame(corpusInfo)
    #
    #
    # # Create a stacked area chart using Altair
    chart = (
        alt.Chart(df)
        .mark_area()
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value", stack="zero"),
            color=alt.Color("id:N", title="Corpus"),
        )
        .properties(width=700, height=400, title="Investment Stacked Area Chart")
    )
    #
    # # Render the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    #
    #
    [col1, col2] = st.columns(2)
    col1.write("## Expenses")
    for expense in v["expenses"]:
        if expense["enabled"]:
            col1.success(f"{expense["id"]} (enabled)")
        if not expense["enabled"]:
            col1.error(f"{expense["id"]} (disabled)")
    #
    col2.write("## Allocations")
    yearUnderAnalysis = col2.selectbox(options=[2025, 2026, 2027, 2028], label="Year")
    allocationsOfYearUnderAnalysis = [
        s for s in simulation if s["year"] == yearUnderAnalysis
    ][0]["cashflowAllocation"]
    col2.write("## Allocation Pie Chart")
    allocation_df = pd.DataFrame([
        {"id": corpus["id"], "value": corpus["value"]}
        for allocation in allocationsOfYearUnderAnalysis
        for corpus in allocation["corpora"]
    ])
    pie_chart = alt.Chart(allocation_df).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="id", type="nominal", title="Corpus"),
        tooltip=["id", "value"]
    ).properties(
        width=400,
        height=400,
        title=f"Allocation Pie Chart for {yearUnderAnalysis}"
    )
    col2.altair_chart(pie_chart, use_container_width=True)
    col2.write("## Warnings")
    for warning in warnings:
        col2.error(
            warning,
            icon="🚨",
        )


    with st.expander("Debug"):
        st.json(simulation)

with st.expander("Input"):
    st.json(v)

with st.expander("Sample"):
    st.json(vaibhav_sample_data)