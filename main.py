if __name__ != "__main__":
    pass
else:
    import json
    import altair as alt
    import pandas as pd
    import streamlit as st

    from flow_prediction.app.use_cases.simulation import (
        CashflowSimulationUseCase,
    )
    from flow_prediction.app.use_cases.simulation.samples.vaibhav_sample_data import (
        # no_marriage_cost,
        vaibhav_sample_data,
    )

    # st.title("Die With Zero Calculator")

    def getRemainingMoney(simulation):
        remainingMoney = sum(
            map(lambda x: x["value"]["amount"], simulation[-1]["corpora"])
        )
        inflationAdjustedRemainingMoney = sum(
            map(
                lambda x: x["value"]["inflationAdjusted"],
                simulation[-1]["corpora"],
            )
        )
        return remainingMoney, inflationAdjustedRemainingMoney

    st.set_page_config(layout="wide", page_title="Die With Zero Calculator")
    st.write("# Die With Zero Calculator")
    text_area = st.text_area(label="Custom JSON")

    v = (
        json.loads(text_area) if text_area else vaibhav_sample_data
    )  # vaibhav_sample_data
    result = CashflowSimulationUseCase(v).execute()

    applicableYears = list(
        range(v["simulation"]["startYear"], v["simulation"]["endYear"] + 1)
    )

    simulation = result["simulation"]
    warnings = result["warnings"]
    corpusInfo = []

    for yearData in simulation:
        for corpus in yearData["corpora"]:
            corpusInfo.append(
                {
                    "id": corpus["id"],
                    "year": yearData["year"],
                    "value": corpus["value"]["amount"],
                }
            )
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
    hero_col1, hero_col2 = st.columns([2, 1])
    showAllWarnings = hero_col2.toggle(f"Show All ({len(warnings)})")
    for warning in warnings[: 3 if not showAllWarnings else len(warnings)]:
        hero_col2.error(
            warning,
            icon="🚨",
        )

    # # Render the chart in Streamlit
    hero_col1.altair_chart(chart, use_container_width=True)
    remainingMoney, inflationAdjustedRemainingMoney = getRemainingMoney(simulation)
    st.warning(
        f"You finished with {remainingMoney} extra, ({inflationAdjustedRemainingMoney} in {v['simulation']['startYear']} terms)"
    )

    [col1, col2, col3] = st.columns(3)
    col1.write("## Expenses")
    for expense in v["expenses"]:
        if expense["enabled"]:
            col1.success(f"{expense["id"]} (enabled)")
        if not expense["enabled"]:
            col1.error(f"{expense["id"]} (disabled)")
    #
    col2.write("## Allocations")
    yearUnderAnalysis = col2.selectbox(options=applicableYears, label="Year")
    allocationsOfYearUnderAnalysis = [
        s for s in simulation if s["year"] == yearUnderAnalysis
    ][0]["cashflowAllocations"]
    col2.write("## Allocation Pie Chart")
    data_points = [
        {"id": f"{allocation["id"]}-{corpus["id"]}", "value": corpus["value"]}
        for allocation in allocationsOfYearUnderAnalysis
        for corpus in allocation["corpora"]
    ]
    allocation_df = pd.DataFrame(data_points)

    if len(allocation_df) == 0:
        col2.warning("No cashflow allocation for this year, are you retired?")
    else:
        pie_chart = (
            alt.Chart(allocation_df)
            .mark_arc()
            .encode(
                theta=alt.Theta(field="value", type="quantitative"),
                color=alt.Color(field="id", type="nominal", title="Corpus"),
                tooltip=["id", "value"],
            )
            .properties(
                width=400,
                height=400,
                title=f"Allocation Pie Chart for {yearUnderAnalysis}",
            )
        )
        col2.altair_chart(pie_chart, use_container_width=True)

    col3.write("## Corpus Bird's Eye")

    yearUnderCorpusAnalysis = col3.selectbox(
        options=applicableYears,
        label="Year",
        key="corpus-analysis",
        index=len(applicableYears) - 1,
    )
    corpusDataOfYear = [d for d in simulation if d["year"] == yearUnderCorpusAnalysis][
        0
    ]["corpora"]

    for corpus in corpusDataOfYear:
        col3.write(f"**{corpus['id']}**")
        col3.write(f"Value: {corpus['value']}")

    with st.expander("Debug"):
        st.json(simulation)

    with st.expander("Input"):
        st.json(v)

    with st.expander("Sample"):
        st.json(v)
