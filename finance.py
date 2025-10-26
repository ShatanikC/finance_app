import streamlit as st,pandas as pd,gspread,time
from google.oauth2.service_account import Credentials
from typing import Union
st.set_page_config(layout='wide')

def connect_to_gsheet(sheetname='Sheet1'):
    scope = ["https://spreadsheets.google.com/feeds", 
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", 
             "https://www.googleapis.com/auth/drive"]
    creds_dict=st.secrets['gcp_service_account']
    credentials=Credentials.from_service_account_info(creds_dict,scopes=scope)
    client=gspread.authorize(credentials)
    sheet=client.open('Personal Finances')
    return sheet.worksheet(sheetname)

pfa: list[Union[str,int,float]]=[0,0,0,0]
def paid_to_amount():
    st.header('Amount Paid')
    sheet=connect_to_gsheet('Amount Paid')
    global pfa
    date=st.date_input('Enter the date of transaction',key='date')
    add_date=st.button('Add Date',key='date_add')
    if add_date:
        pfa[0]=date.isoformat()
    amount=st.number_input('Enter the amount of transaction',key='amount')
    add_amount=st.button('Add Amount',key='amount_add')
    if add_amount:
        pfa[1]=amount
    paid=st.text_input('Enter the person/organization paid to',key='paid')
    add_paid=st.button('Add Paid To Details',key='paid_add')
    if add_paid:
        pfa[2]=paid
    category=st.text_input('Enter category',key='category')
    add_category=st.button('Add Category',key='add_category')
    if add_category:
        pfa[3]=category
    submit=st.button('Submit',key='submit_add')
    if submit:
        sheet.append_row(pfa)
        pfa=[0,0,0,0]
        time.sleep(2)
        st.rerun()
    

pfr: list[Union[str,int,float]]=[0,0,0,0]
def received_amount():
    st.header('Amount Received')
    sheet=connect_to_gsheet('Amount Received')
    global pfr
    date=st.date_input('Enter the date of transaction',key='date_received')
    add_date=st.button('Add Date',key='date_received_add')
    if add_date:
        pfr[0]=date.isoformat()
    amount=st.number_input('Enter the amount of transaction',key='received_amount')
    add_amount=st.button('Add Amount',key='amount_received_add')
    if add_amount:
        pfr[1]=amount
    received=st.text_input('Enter the person/organization received from',key='received')
    add_received=st.button('Add Received From Details',key='amount_received_from_add')
    if add_received:
        pfa[2]=received
    category=st.text_input('Enter category',key='category_received')
    add_category=st.button('Add Category',key='category_received_add')
    if add_category:
        pfa[3]=category
    submit=st.button('Submit',key='submit_received')
    if submit:
        sheet.append_row(pfr)
        pfr=[0,0,0,0]
        time.sleep(2)
        st.rerun()

def dashboard():
    status=connect_to_gsheet('Current Status').get_all_records()
    st.dataframe(status)