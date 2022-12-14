import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def member_page():

    df = pd.read_excel("data/mock_data.xlsx")
    event_sign_up = pd.read_excel("data/mock_data.xlsx", sheet_name='Event Sign-Up')
    #experimental
    manager_approvals = pd.read_excel("data/manager_approvals.xlsx")
    
    # button to link to the form
    mock_user = df.iloc[3]
    mock_user_email = mock_user['Email']
    
    tab1, tab2, tab3, tab4 = st.tabs(["My Overview", "Training Outside Udemy/Learning Studio", "Compare", "Events"])

    with tab1:

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
        with st.form("log_form", clear_on_submit=True):
            learning_type =  st.selectbox(
                'What you want to submit:', 
                ['Course outside Udemy/Learning Studio', 'Exercises for Udemy courses', 'Learning project']
                )
            course_name = st.text_input('Course/Project Name')
            time = st.text_input('Learning Time in Hours')
            submit = st.form_submit_button('Submit')

        if submit:
            new_data = {"Email": [mock_user_email], "Type": [learning_type], "Name": [course_name], "Time": [int(time)], "Status": ["Pending"]}
            new_df = pd.DataFrame(new_data)
            manager_approvals = pd.concat([manager_approvals, new_df], ignore_index=True)
            manager_approvals.to_excel("data/manager_approvals.xlsx", index = False)

        st.subheader('Status of my requests')
        def color_negative(v, color):
            if v == 'Declined':
                color = 'red'
            elif v == 'Approved':
                color = 'green'
            elif v == 'Pending':
                color = 'orange'
            else:
                color = None
            return f"color: {color};"
        select_user = manager_approvals.loc[manager_approvals['Email'] == mock_user_email]
        select_user = select_user.style.applymap(color_negative, color='')
        st.table(select_user)

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
        
        if df.empty:
            st.write("There is no such record!")
        else:
            #TOP N
            df = df.nlargest(n=top_n, columns=['Minutes Video Consumed'])
            
            #extract names from Email
            df['Name'] = df['Email'].str.split('@', expand=True)[0]
        
            #BAR CHART
            fig_comparison = px.bar(df, x='Minutes Video Consumed', y='Name', text='Minutes Video Consumed',orientation='h')
            fig_comparison.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig_comparison.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        
    with tab4:
        st.header("Events")
        st.write("Here you can find information about upcoming events.")
        st.subheader('You are enrolled to these events:')
        
        for data in event_sign_up.columns:
            filtered_data = event_sign_up.query('Email == @mock_user_email')
            for x in filtered_data[data]:
                if x == 'x':
                    st.write(f'{data}')

        st.subheader('See who is coming to the events:')

        #extract names from Email - events tab
        event_sign_up['Name'] = event_sign_up['Email'].str.split('@', expand=True)[0]
        dict_of_dfs = {f'{i}':event_sign_up.filter(['Name', i], axis =1).dropna()['Name'] for i in event_sign_up.columns[1:-1]}

        event_list = list(dict_of_dfs.keys())
        option = st.selectbox('Please select event:', event_list)
        
        for name, df in dict_of_dfs.items():
            if option == name:
                attendees = dict_of_dfs[name]
                st.write(attendees)