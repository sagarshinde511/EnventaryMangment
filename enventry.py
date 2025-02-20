import streamlit as st
import mysql.connector
import datetime

# MySQL Database Connection
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students",
}

# Default login credentials
USERNAME = "admin"
PASSWORD = "password"

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Create table if not exists
def create_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enventry (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ProductName VARCHAR(255),
                LotNumber VARCHAR(255),
                Mfg DATE,
                Expire DATE
            )
        """)
        conn.commit()
        conn.close()

# Insert product data into MySQL
def insert_product(product_name, lot_number, mfg, expire):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO Enventry (ProductName, LotNumber, Mfg, Expire) VALUES (%s, %s, %s, %s)"
        values = (product_name, lot_number, mfg, expire)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        st.success("Product registered successfully!")

# Fetch the most recent entry
def fetch_recent_entry():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionary
        cursor.execute("SELECT * FROM Enventry ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result
    return None

# Login Page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

# Product Registration Page
def product_registration():
    st.title("Product Registration")

    product_name = st.text_input("Product Name")
    lot_number = st.text_input("Lot Number")
    manufacture_date = st.date_input("Manufacture Date", datetime.date.today())
    expiry_date = st.date_input("Expiry Date", datetime.date.today())

    if st.button("Submit"):
        insert_product(product_name, lot_number, manufacture_date, expiry_date)

    # Fetch and display the most recent entry
    recent_entry = fetch_recent_entry()
    if recent_entry:
        st.subheader("Most Recent Entry:")
        st.write(recent_entry)  # Print dictionary format
    else:
        st.warning("No data found!")

# Sidebar Navigation
def sidebar():
    with st.sidebar:
        st.write("Navigation")
        st.button("Logout", on_click=logout)

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# Initialize database
create_table()

# App Flow
if not st.session_state.logged_in:
    login()
else:
    sidebar()
    product_registration()
