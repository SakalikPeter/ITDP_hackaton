import streamlit as st
import pandas as pd
from st_on_hover_tabs import on_hover_tabs
from manager import manager_page
from member import member_page

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


with st.sidebar:
    tabs = on_hover_tabs(tabName=['Manager', 'ITDP member'], 
                         iconName=['manager', 'person'], default_choice=0)


if tabs == 'Manager':
    manager_page(tabs)

elif tabs == 'ITDP member':
    member_page(tabs)
    
