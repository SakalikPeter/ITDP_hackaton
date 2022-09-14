import streamlit as st

def member_page(tabs):
    st.header("I am member of ITDP")
    st.write('Name of option is {}'.format(tabs))

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
        

