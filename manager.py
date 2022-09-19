import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def desicionFunc(df_row, selected, status):
    if df_row['Email'] == selected['Email'] and df_row['Type'] == selected['Type'] and df_row['Name'] == selected['Name'] and status == 'Approved':
        return 'Approved'
    elif df_row['Email'] == selected['Email'] and df_row['Type'] == selected['Type'] and df_row['Name'] == selected['Name'] and status == 'Declined':
        return 'Declined'
    return df_row['Status']

def aggrid_interactive_table(df: pd.DataFrame):
    option = GridOptionsBuilder.from_dataframe(
         df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    option.configure_side_bar()
    option.configure_selection("single", use_checkbox=True)
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=option.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        theme="material"
    )
    return selection

def aggrid_selection(selection):
    word_dict = {'y': 'Attended', 'n': 'Not Attended', 'x': 'Signed Up', 'None': 'Not Signed Up'}
    
    if selection['selected_rows']:
        row = selection['selected_rows'][0]
        del row['_selectedRowNodeInfo']

        for k,v in row.items():
            v = word_dict[str(v)] if str(v) in word_dict.keys() else v
            st.metric(k, v)

def manager_page():
    st.title(":bar_chart: ITDP  members overview")
    df = pd.read_excel("data/mock_data.xlsx")

    training_data = pd.read_excel("data/mock_data.xlsx", sheet_name='Training Data')
    virtual_attendance = pd.read_excel("data/mock_data.xlsx", sheet_name='Virtual Attendance')
    event_sign_up = pd.read_excel("data/mock_data.xlsx", sheet_name='Event Sign-Up')

    approval_data = pd.read_excel('data/manager_approvals.xlsx')

    tab1, tab2, tab3 = st.tabs(["Table filters", "Stats", "Approval Tab"])

    with tab1:
        with st.expander("Training data"):
            st.header("Training Data")
            selection = aggrid_interactive_table(df=training_data)
            aggrid_selection(selection)

        with st.expander("Virtual Attendance"):
            st.header("Virtual Attendance")
            selection = aggrid_interactive_table(df=virtual_attendance)
            aggrid_selection(selection)
        
        with st.expander("Event Sign-Up"):
            st.header("Event Sign-Up")
            selection = aggrid_interactive_table(df=event_sign_up)
            aggrid_selection(selection)

    with tab2:
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
            title="<b>Consumed minutes based on no of enrolled courses</b>",
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

    with tab3:
        st.header("Training Approval")
        st.write("Here you can approve members requests.") 
        st.subheader('Status of requests')

        pending_data = approval_data.query('Status == "Pending"')
        for i, row in pending_data.iterrows():     
            with st.expander(f"Email: {row['Email']}, Course: {row['Name']}, Type: {row['Type']}"):
                placeholder = st.empty()
                option = placeholder.selectbox(
                    'How would you like to decide?',
                    ('Pending', 'Approve', 'Decline'), key=i)

                if option == 'Approve':
                    st.success("Request was approved.")
                    approval_data['Status'] = approval_data.apply(lambda x: desicionFunc(x, row, 'Approved'), axis=1)
                    approval_data.to_excel("data/manager_approvals.xlsx", index = False)
                    df.loc[df['Email'] == row['Email'], 'No# of New Courses Enrolled'] += 1
                    df.loc[df['Email'] == row['Email'], 'No# of New Courses Started'] += 1
                    df.loc[df['Email'] == row['Email'], 'Minutes Video Consumed'] += (row['Time'] * 60)
                    with pd.ExcelWriter('data/mock_data.xlsx') as writer:  
                        df.to_excel(writer, sheet_name='Training Data', index = False)
                        virtual_attendance.to_excel(writer, sheet_name='Virtual Attendance', index = False)
                        event_sign_up.to_excel(writer, sheet_name='Event Sign-Up', index = False)
                    placeholder.empty()
                elif option == 'Decline':
                    st.error("Request was NOT approved.")
                    approval_data['Status'] = approval_data.apply(lambda x: desicionFunc(x, row, 'Declined'), axis=1)
                    approval_data.to_excel("data/manager_approvals.xlsx", index = False)
                    placeholder.empty()
                else:
                    st.warning("No decision was made yet.")

