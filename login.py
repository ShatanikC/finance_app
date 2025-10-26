from finance import paid_to_amount,received_amount,dashboard
import streamlit as st,streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import bcrypt

if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False

def main_page():
    st.title('Welcome to the Personal Finance App')
    st.header('View Current Finance')
    col1,col2=st.columns(2)
    with col1:
        paid_to_amount()
    with col2:
        received_amount()
    dashboard()
    logout=st.button('Logout',key='Logout')
    if logout:
        st.session_state.logged_in=False
        st.rerun()

def auth():
    st.title('Welcome to the Personal Finance App')
    with st.form('Login'):
        st.subheader('Please log in:')
        username=st.text_input('Username',key='username')
        password=st.text_input('Password',type='password',key='password')
        submit=st.form_submit_button('Login',key='submit')
        if submit:
            stored_user = st.secrets["credentials"]["name"]
            stored_hash = st.secrets["credentials"]["password"]
            if username == stored_user and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                st.session_state.logged_in = True
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

if st.session_state.logged_in:
    main_page()
else:
    auth()