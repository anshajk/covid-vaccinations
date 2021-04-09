import streamlit as st
import urllib
import pandas as pd
import altair as alt


def get_vaccination_data():
    DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
    df = pd.read_csv(DATA_URL)
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.date
    return df


st.title("Covid19 vaccination and infection data")
try:
    df = get_vaccination_data()
    selected_locations = st.multiselect(
        "Select countries", df["location"].unique().tolist(), default=["India"],
    )
    if len(selected_locations) > 5:
        st.warning(
            "Please select a maximum of 5 locations while comparing to see the results clearly"
        )
    df = df[df["location"].isin(selected_locations)]
    daily_vaccination_chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", axis=alt.Axis(title="Date")),
            y=alt.X("daily_vaccinations:Q", axis=alt.Axis(title="Daily vaccinations")),
            tooltip=["date", "daily_vaccinations"],
            color="location",
        )
        .interactive()
        .properties(width=800, height=400)
    )
    st.header("Daily covid19 vaccination count")
    st.write(daily_vaccination_chart)
    daily_vaccination_chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", axis=alt.Axis(title="Date")),
            y=alt.X("daily_vaccinations:Q", axis=alt.Axis(title="Daily vaccinations")),
            tooltip=["date", "daily_vaccinations"],
            color="location",
        )
        .interactive()
        .properties(width=800, height=400)
    )


except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

st.text("Data courtesy: Our world in data - https://ourworldindata.org/coronavirus")
