import streamlit as st
import pandas as pd
from bokeh.models.widgets import Div
import plotly.express as px
from PIL import Image

def member_page():
    st.header("I am member of ITDP")

    df = pd.read_excel("data/mock_data.xlsx")
    learning_log_data = pd.read_excel('data/learning_time_log.xlsx', usecols=['Type','Name','Learning time','Status'])

    # button to link to the form

    tab1, tab2, tab3 = st.tabs(["My Overview", "Training Outside Udemy/Learning Studio", "Compare"])

    with tab1:
        mock_user = df.iloc[3]

        st.header("My Overview")
        st.subheader(f'You are logged in as {mock_user["Email"]}')
        st.write("Here you can find the overview of the courses you are currently working on.")

        total_minutes = int(mock_user["Minutes Video Consumed"])
        total_started = int(mock_user["No# of New Courses Started"])
        total_enrolled = int(mock_user["No# of New Courses Enrolled"])

        jay = Image.open('img/jay.jpg')
        ok = Image.open('img/ok.jpg')
        poor = Image.open('img/poor.jpg')
        no = Image.open('img/no.jpg')

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

        if total_minutes >= 4000:
            st.image(jay, caption= 'You are doing great!')
        elif total_minutes < 4000 and (total_minutes>=2000):
            st.image(ok, caption ='You are doing well.')
        elif total_minutes < 2000 and (total_minutes>=600):
            st.image(poor, caption='Try to learn more.')
        else:
            st.image(no, caption='You are not hitting the minimum amount of training.')

    with tab2:
        st.header("Training Outside Udemy/Learning Studio")
        st.write("Here you can log hours outside Udemy/Learning Studio and see the status of your requests.")

        if st.button('Log hours outside Udemy and Learning Studio'):
            js = "window.open('https://forms.office.com/r/kN3vNjKJC5')"  # New tab or window
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)

        # This is a mock table    
        st.subheader('Status of my requests')
        def color_negative(v, color):
            if v == 'Denied':
                color = 'red'
            elif v == 'Approved':
                color = 'green'
            elif v == 'Pending':
                color = 'orange'
            else:
                color = None
            return f"color: {color};"
        learning_log_data=learning_log_data.style.applymap(color_negative, color='')
        st.table(learning_log_data)

        # def highlight_cells(val):
    #     color = 'red' if "Denied" in val else 'white'
    #
    #     (st.dataframe.style.applymap(highlight_cells, subset=["Denied"]).to_excel(learning_log_data, index=False))
    #     styles = st.dataframe.style.apply(highlight_cells, axis=None)
    #     styles.to_excel(learning_log_data)
    #     return f'background-color: {color}'


            #color = 'green' if 'Approved' in val else 'white'
            #(st.dataframe.style.applymap(highlight_cells, subset=['Approved'])
             #.to_excel("learning_time_log.xlsx", index=False))
            #color = 'orange' if 'Pending' in val else 'white'
            #(st.dataframe.style.applymap(highlight_cells, subset=['Pending'])
             #.to_excel("learning_time_log.xlsx", index=False))



    with tab3:
        st.header("Compare")
        st.write("Here you can compare yourself and your group to other groups and members.")

        st.subheader("Filter Here:")

        left,mid= st.columns(2)

        groups = left.multiselect(
            "Groups",
            options=df["Groups"].unique(),
            default=df["Groups"].unique()
        )

        country = mid.multiselect(
            "Work Country",
            options=df["Work Country"].unique(),
            default=df["Work Country"].unique()
        )

        manager_name = st.multiselect(
            "L5 Mgr Name",
            options=df["L5 Mgr Name"].unique(),
            default=df["L5 Mgr Name"].unique()
        )

        top_n = st.slider(
            "TOP N ITDP's",
            min_value = 1,
            max_value = len(df),
            value = 10,
            step = 1)

        df = df.query(
            "Groups == @groups  & `L5 Mgr Name` ==@manager_name & `Work Country` == @country"
        )

        #TOP N
        df = df.nlargest(n=top_n, columns=['Minutes Video Consumed'])

        #extract names from Email
        names = df['Email'].str.split('@', expand=True)[0]
        df['Name'] = names

        #BAR CHART
        fig_comparison = px.bar(df, x='Minutes Video Consumed', y='Name', text='Minutes Video Consumed',orientation='h')
        fig_comparison.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_comparison.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig_comparison, use_container_width=True)