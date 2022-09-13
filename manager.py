import streamlit as st

def manager_page(tabs):
    st.header("I am manager")
    st.write('Name of option is {}'.format(tabs))
    
    # button to link to the form
    from bokeh.models.widgets import Div

    if st.button("View member's hours outside Udemy and Learning Studio"):
        js = "window.open('https://forms.office.com/Pages/AnalysisPage.aspx?AnalyzerToken=J6swEn0mO08mqRLUIdTRVn2Ro1BDmt0O&id=mhlclKKDgE6fjFqRvldS3Xs7AIzsLtNKntGWCmL_NyBUOUZOMzZDT1M3SjZaNFY2QzgxR1YyRzZFQi4u')"  # New tab or window
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
            
            