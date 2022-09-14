import streamlit as st
import pandas as pd
from bokeh.models.widgets import Div


def member_page(tabs):
    st.header("I am member of ITDP")
    st.write('Name of option is {}'.format(tabs))
    
    df = pd.read_excel("mock_data.xlsx")
# =============================================================================
#     training_data = pd.read_excel("mock_data.xlsx", sheet_name='Training Data')
#     virtual_attendance = pd.read_excel("mock_data.xlsx", sheet_name='Virtual Attendance')
#     event_sign_up = pd.read_excel("mock_data.xlsx", sheet_name='Event Sign-Up')
# =============================================================================
    
    # button to link to the form

    tab1, tab2, tab3 = st.tabs(["My Overview", "My ITDP Group", "Compare"])

    with tab1:
        mock_user = df.iloc[0]
        
        st.header("My Overview")
        st.subheader(f'You are logged in as {mock_user["Email"]}')
        st.write("Here you can find the overview of the courses you are currently working on.")

        total_minutes = int(mock_user["Minutes Video Consumed"])
        total_started = int(mock_user["No# of New Courses Started"])
        total_enrolled = int(mock_user["No# of New Courses Enrolled"])
                
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
        
        
        if st.button('Log hours outside Udemy and Learning Studio'):
            js = "window.open('https://forms.office.com/r/kN3vNjKJC5')"  # New tab or window
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)    

    with tab2:
        st.header("My ITDP Group")
        st.write("Here you can see the ITDP members in your group.")

        
    with tab3:
        st.header("Compare")
        st.write("Here you can compare yourself and your group to other groups and members.")
