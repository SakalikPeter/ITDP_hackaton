import streamlit as st
import pandas as pd
import plotly.express as px  # pip install plotly-express   

def manager_page(tabs):
    st.write('Name of option is {}'.format(tabs))
    st.title(":bar_chart: ITDP  members overview")
    df = pd.read_excel("mock_data.xlsx")



    st.header("Filter Here:")

    left,mid= st.columns(2)

    groups = left.multiselect(
        "Groups",
        options=df["Groups"].unique(),
        default=df["Groups"].unique()
    )

    country = mid.multiselect(
        "Work Country",
        options=df["Work Country"].unique(),
        default=df["Work Country"].unique(),
    )

    manager_name = st.multiselect(
        "L5 Mgr Name",
        options=df["L5 Mgr Name"].unique(),
        default=df["L5 Mgr Name"].unique()
    )

    df = df.query(
    "Groups == @groups  & `L5 Mgr Name` ==@manager_name & `Work Country` == @country"
    )
    total_minutes = int(df["Minutes Video Consumed"].sum())
    total_started = int(df["No# of New Courses Started"].sum())
    total_enrolled = int(df["No# of New Courses Enrolled"].sum())

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Minutes spent on courses:")
        st.subheader(f" ⌛{total_minutes} minutes")
    with middle_column:
        st.subheader("Total courses started:")
        st.subheader(f" ⭐{total_started} ")
    with right_column:
        st.subheader("Total courses enrolled:")
        st.subheader(f" 💻{total_enrolled}")

    st.markdown("""---""")

    minutes_by_groups = (
        df.groupby(by=["Groups"]).sum()[["Minutes Video Consumed"]].sort_values(by="Minutes Video Consumed")
    )
    fig_minutes_by_groups = px.bar(
        minutes_by_groups,
        x="Minutes Video Consumed",
        y=minutes_by_groups.index,
        orientation="h",
        title="<b>Minutes consumed based on groups</b>",
        color_discrete_sequence=["#0083B8"] * len(minutes_by_groups),
        template="plotly_white",
    )
    fig_minutes_by_groups.update_layout(
        xaxis=(dict(showgrid=False))
    )


    last_activity_by_region=(
        df.groupby(by=["No# of New Courses Enrolled"]).max()[["Minutes Video Consumed"]].sort_values(by="Minutes Video Consumed")
    )
    fig_last_activity_by_region = px.line(
        last_activity_by_region,
        x="Minutes Video Consumed",
        y=last_activity_by_region.index,
        orientation="h",
        title="<b>Last activity by region</b>",
        color_discrete_sequence=["#0083B8"] * len(last_activity_by_region),
        template="plotly_white",
    )
    fig_last_activity_by_region.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    fig = px.scatter(df,
        title="<b>Last activity since joined</b>",
    
     x="Date Joined", y="Date of Last Activity", color="Work Region")


    fig2 = px.bar(df,
        title="<b>Minutes consumed based on country</b>",
     x="Work Country", y="Minutes Video Consumed", barmode="group")



    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_minutes_by_groups, use_container_width=True)
    right_column.plotly_chart(fig, use_container_width=True)



    left_column2, right_column2 = st.columns(2)
    left_column2.plotly_chart(fig_last_activity_by_region, use_container_width=True)
    right_column2.plotly_chart(fig2, use_container_width=True)
