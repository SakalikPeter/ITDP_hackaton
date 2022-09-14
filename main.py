import streamlit as st
import pandas as pd
from st_on_hover_tabs import on_hover_tabs
from manager import manager_page
from member import member_page

st.set_page_config(layout="wide")

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Manager', 'ITDP member'], 
                         iconName=['manager', 'person'],
                         styles = {'navtab': {'background-color':'#262730',
                                                  'color': '#949494',
                                                  'font-size': '25px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'}}, default_choice=0)


if tabs == 'Manager':
    manager_page(tabs)

elif tabs == 'ITDP member':
    member_page(tabs)
    
