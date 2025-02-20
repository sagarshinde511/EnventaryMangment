import streamlit as st
import mysql.connector
import datetime
import qrcode
from io import BytesIO

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "view_products" not in st.session_state:
    st.session_state.view_products = False

# MySQL Database Connection
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1",
}

# Default login credentials
USERNAME = "admin"
PASSWORD = "password"

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

# Sidebar Navigation
def sidebar():
    with st.sidebar:
        st.write("Navigation")
        if st.button("Check Products"):
            st.session_state.view_products = True  # Set session state for product view
            st.rerun()  # Force rerun to update the page
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.view_products = False
            st.rerun()

# Connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Fetch all product data
def fetch_all_products():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Enventry ORDER BY id DESC")
        results = cursor.fetchall()
        conn.close()
        return results
    return []
# Product View Page
# Product View Page
def display_products():
    st.title("All Registered Products")

    products = fetch_all_products()

    if products:
        # Convert list of dictionaries to a Pandas DataFrame for table display
        import pandas as pd
        df = pd.DataFrame(products)

        # Exclude the QRCode binary data from table view
        if "QRCode" in df.columns:
            df = df.drop(columns=["QRCode"])

        # Display table
        st.dataframe(df)

        # Display each QR code separately
        for product in products:
            if product["QRCode"]:
                st.subheader(f"QR Code for {product['ProductName']} (Lot: {product['LotNumber']})")
                st.image(BytesIO(product["QRCode"]), caption="Product QR Code", use_column_width=False)

                # Allow downloading the QR Code
                st.download_button(
                    label=f"Download QR Code ({product['LotNumber']})",
                    data=product["QRCode"],
                    file_name=f"QR_{product['LotNumber']}.png",
                    mime="image/png"
                )
            st.markdown("---")
    else:
        st.warning("No products found in the database.")

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
            st.write({key: recent_entry[key] for key in recent_entry if key != "QRCode"})  # Exclude QRCode from print

            # Display QR Code from database
            if recent_entry["QRCode"]:
                st.image(BytesIO(recent_entry["QRCode"]), caption="Product QR Code", use_column_width=False)

                # Allow downloading the QR Code
                st.download_button(
                    label="Download QR Code",
                    data=recent_entry["QRCode"],
                    file_name="product_qr.png",
                    mime="image/png"
                )
        else:
            st.warning("No data found!")

# App Flow
if not st.session_state.logged_in:
    login()
else:
    sidebar()
    
    if st.session_state.view_products:
        display_products()
    else:
        product_registration()
