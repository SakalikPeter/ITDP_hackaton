import streamlit as st
from manager import manager_page
from member import member_page
import pickle
import streamlit_authenticator as stauth
from pathlib import Path

st.set_page_config(layout="wide")

names = ["ITDP MEMBER", "ITDP MANAGER"]
usernames = ["itdp_member", "itdp_manager"]

file_path = Path(__file__).parent / "keygen/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status and username == "itdp_manager":

    with st.sidebar:
        st.sidebar.image("img/Dell_Logo.png", width=100)
        st.markdown(f"**Welcome {name}**")
        authenticator.logout("Logout")
    manager_page()

elif authentication_status and username == "itdp_member":
    with st.sidebar:
        st.sidebar.image("img/Dell_Logo.png", width=100)
        st.markdown(f"**Welcome {name}**")
        authenticator.logout("Logout")
    member_page()
