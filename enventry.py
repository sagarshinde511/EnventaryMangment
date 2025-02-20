import streamlit as st
import mysql.connector
import datetime
import qrcode
from io import BytesIO

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

# Generate QR Code from dictionary
def generate_qr_code(data_dict):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(data_dict))  # Convert dictionary to string
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Save QR code to in-memory buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()  # Return QR code as binary data

# Insert product data into MySQL with QR code
def insert_product(product_name, lot_number, mfg, expire):
    # Create data dictionary
    product_data = {
        "ProductName": product_name,
        "LotNumber": lot_number,
        "Mfg": str(mfg),
        "Expire": str(expire),
    }

    # Generate QR code
    qr_code_data = generate_qr_code(product_data)

    # Insert data into MySQL
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO Enventry (ProductName, LotNumber, Mfg, Expire, QRCode)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (product_name, lot_number, mfg, expire, qr_code_data)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        st.success("Product registered successfully!")

# Fetch the most recent entry including QR Code
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
# App Flow
if not st.session_state.logged_in:
    login()
else:
    sidebar()
    product_registration()
