import streamlit as st
import pandas as pd
from st_on_hover_tabs import on_hover_tabs
from manager import manager_page
from member import member_page
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
st.set_page_config(layout="wide")


names = ["ITDP MEMBER", "ITDP MANAGER"]
usernames = ["itdp_member", "itdp_manager"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


#create authenticator 
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status and username == "itdp_manager":

    with st.sidebar:
        #welcome manager with name and format it to bold
        st.markdown(f"**Welcome {name}**")
        authenticator.logout("Logout")
        tabs = on_hover_tabs(tabName=['Manager'], 
                            iconName=['manager'],
                            styles = {'navtab': {'background-color':'#262730',
                                                    'color': 'white',
                                                    'font-size': '25px',
                                                    'transition': '.3s',
                                                    'white-space': 'nowrap',
                                                    'text-transform': 'uppercase'}}, default_choice=0)


    if tabs == 'Manager' :
        manager_page(tabs)

elif authentication_status and username == "itdp_member":

    with st.sidebar:
        st.markdown(f"**Welcome {name}**")
        authenticator.logout("Logout")
        tabs = on_hover_tabs(tabName=[ 'ITDP member'], 
                            iconName=[ 'person'],
                            styles = {'navtab': {'background-color':'#262730',
                                                    'color': 'white',
                                                    'font-size': '25px',
                                                    'transition': '.3s',
                                                    'white-space': 'nowrap',
                                                    'text-transform': 'uppercase'}}, default_choice=0)


    
    if tabs == 'ITDP member':
        member_page(tabs)
    
