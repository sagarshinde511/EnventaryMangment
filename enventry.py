import streamlit as st
import datetime

# Default credentials
USERNAME = "admin"
PASSWORD = "password"

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Product registration page
def product_registration():
    st.title("Product Registration")

    product_name = st.text_input("Product Name")
    lot_number = st.text_input("Lot Number")
    manufacture_date = st.date_input("Manufacture Date", datetime.date.today())
    expiry_date = st.date_input("Expiry Date", datetime.date.today())

    if st.button("Submit"):
        st.success(f"Product '{product_name}' registered successfully!")

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.write("Navigation")
        st.button("Logout", on_click=lambda: logout())

# Logout function
def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# App flow
if not st.session_state.logged_in:
    login()
else:
    sidebar()
    product_registration()
