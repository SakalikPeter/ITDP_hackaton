import streamlit as st

def member_page(tabs):
    st.header("I am member of ITDP")
    st.write('Name of option is {}'.format(tabs))
    
    # button to link to the form
    from bokeh.models.widgets import Div

    with st.sidebar:
        if st.button('Log hours outside Udemy and Learning Studio'):
            js = "window.open('https://forms.office.com/r/kN3vNjKJC5')"  # New tab or window
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)


    tab1, tab2, tab3 = st.tabs(["My Overview", "My ITDP Group", "Compare"])

    with tab1:
        st.header("My Overview")
        st.write("Here you can find the overview of the courses you are currently working on.")


    with tab2:
        st.header("My ITDP Group")
        st.write("Here you can see the ITDP members in your group.")

        
    with tab3:
        st.header("Compare")
        st.write("Here you can compare yourself and your group to other groups and members.")
        
