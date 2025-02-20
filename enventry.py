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

# Sidebar Navigation
def sidebar():
    with st.sidebar:
        st.write("Navigation")
        if st.button("Check Products"):
            st.session_state.view_products = True  # Set session state for product view
        st.button("Logout", on_click=logout)

# Product View Page
def display_products():
    st.title("All Registered Products")
    products = fetch_all_products()

    if products:
        for product in products:
            st.write({key: product[key] for key in product if key != "QRCode"})  # Exclude QRCode from display
            
            # Display QR Code if available
            if product["QRCode"]:
                st.image(BytesIO(product["QRCode"]), caption="Product QR Code", use_column_width=False)

                # Allow downloading the QR Code
                st.download_button(
                    label="Download QR Code",
                    data=product["QRCode"],
                    file_name=f"QR_{product['LotNumber']}.png",
                    mime="image/png"
                )
            st.markdown("---")
    else:
        st.warning("No products found in the database.")

# App Flow
if not st.session_state.logged_in:
    login()
else:
    sidebar()
    
    if "view_products" in st.session_state and st.session_state.view_products:
        display_products()
    else:
        product_registration()
