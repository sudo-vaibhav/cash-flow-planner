import pandas as pd
import streamlit as st
import altair as alt
from flow_prediction.app.use_cases.simulation import CashflowSimulationUseCase
from flow_prediction.app.use_cases.simulation.samples import (
    vaibhav_sample_data,
)

result = CashflowSimulationUseCase(vaibhav_sample_data).execute()
simulation = result["simulation"]
warnings = result["warnings"]

records = []
for category, entries in simulation.items():

    for entry in entries:
        row = {
            "category": category,
            "year": entry["year"],
            "value": entry["value"],
        }
        # Add a new key to indicate the category/fund type

        records.append(row)

df = pd.DataFrame(records)


# Create a stacked area chart using Altair
chart = (
    alt.Chart(df)
    .mark_area()
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("value:Q", title="Value", stack="zero"),
        color=alt.Color("category:N", title="Investment Category"),
    )
    .properties(width=700, height=400, title="Investment Stacked Area Chart")
)

# Render the chart in Streamlit
st.altair_chart(chart, use_container_width=True)


[col1, col2] = st.columns(2)
col1.write("## Expenses")
col2.write("## Warnings")
for expense in vaibhav_sample_data["expenses"]:
    if expense["enabled"]:
        col1.success(f"{expense["id"]} (enabled)")
    if not expense["enabled"]:
        col1.error(f"{expense["id"]} (disabled)")
for warning in warnings:
    col2.error(
        warning,
        icon="🚨",
    )
