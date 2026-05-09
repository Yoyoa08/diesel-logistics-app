import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import string
import csv


st.set_page_config(page_title="Philip's Online Diesel Supply Ltd", page_icon="⛽", layout="wide")

DB_FILE = "ago_orders.csv"
BANK_ACC = "7018185035"
PRICE_PER_LITRE = 1250
COMPANY_NAME = "Philip's Online Diesel Supply Ltd"


# DATABASE FUNCTIONS
def save_order(data):
    file_exists = os.path.isfile(DB_FILE)
    with open(DB_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys(), quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


# URL ROUTE FOR ADMIN PAGE
query_params = st.query_params
is_admin = query_params.get("view") == "admin"

#   ADMIN / WORKER DASHBOARD
if is_admin:
    st.title(f"📋 {COMPANY_NAME}")
    st.subheader("Logistics Monitor | Internal Operations")

    if os.path.isfile(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE, dtype=str, quoting=csv.QUOTE_ALL)
            st.markdown("### 🚚 Mark Delivery")
            pending_list = df[df['Status'] == 'Pending']['Order_ID'].tolist()

            if pending_list:
                col1, col2 = st.columns([2, 1])
                with col1:
                    to_complete = st.selectbox("Select Order ID to Update", pending_list)
                with col2:
                    st.write(" ")
                    if st.button("Mark as DELIVERED ✅", use_container_width=True):
                        df.loc[df['Order_ID'] == to_complete, 'Status'] = 'Completed'
                        df.to_csv(DB_FILE, index=False, quoting=csv.QUOTE_ALL)
                        st.toast(f"Order {to_complete} completed!", icon="⛽")
                        st.rerun()
            else:
                st.info("No orders are currently pending.")

            st.divider()
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            delivered_vol = df[df['Status'] == 'Completed']['Volume'].sum()

            m1, m2, m3 = st.columns(3)
            m1.metric("Pending Tasks", len(pending_list))
            m2.metric("Total Delivered", f"{delivered_vol:,.0f} L")
            m3.metric("Total Logs", len(df))

            st.dataframe(df.iloc[::-1], use_container_width=True)

        except Exception as e:
            st.error(f"Error loading logs: {e}")
    else:
        st.info("The database is currently empty.")

# --- VIEW 2: CLIENT INTERFACE ---
else:
    st.title(f"⛽ {COMPANY_NAME}")
    st.subheader("Reliable Depot-to-Door Service | Abuja")

    # --- SIDEBAR (Always Visible) ---
    with st.sidebar:
        st.markdown("### 💳 Payment Details")
        st.info(f"**Account:** `{BANK_ACC}`\n\n**Name:** {COMPANY_NAME}")
        st.markdown(f"**Current Rate:** ₦{PRICE_PER_LITRE}/Litre")
        st.divider()
        st.warning("Orders are only processed after payment verification.")

    tab1, tab2, tab3 = st.tabs(["🚀 Place Order", "🔍 Track Order", "❌ Cancel Request"])

    # --- TAB 1: ORDER FORM ---
    with tab1:
        if 'submitted_id' not in st.session_state:
            st.session_state.submitted_id = None

        if st.session_state.submitted_id:
            st.success("✅ ORDER LOGGED SUCCESSFULLY!")
            st.markdown(f"""
            <div style="background-color:#f8f9fa; padding:30px; border-radius:15px; border: 3px solid #ff4b4b; text-align:center; margin-bottom:20px;">
                <h3 style="color:#31333F; margin-bottom:0;">⚠️ IMPORTANT: SCREENSHOT THIS NOW ⚠️</h3>
                <p style="color:#666;">You need this ID to track or cancel your delivery.</p>
                <h1 style="color:#ff4b4b; font-size:80px; margin-top:0; letter-spacing: 5px;">{st.session_state.submitted_id}</h1>
                <p style="color:#31333F; font-weight:bold;">{COMPANY_NAME} will verify payment for Account {BANK_ACC} shortly.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Place Another Order"):
                st.session_state.submitted_id = None
                st.rerun()

        else:
            st.markdown("### 🛒 Order Calculator")
            vol_input = st.number_input("Enter number of Litres", min_value=0, max_value=10000, value=0, step=1)
            calc_total = vol_input * PRICE_PER_LITRE

            st.markdown(f"""
                <div style="background-color:#e1f5fe; padding:20px; border-radius:10px; text-align:center; border: 1px solid #01579b;">
                    <span style="font-size:18px; color:#01579b;">Total Amount to Transfer:</span><br>
                    <span style="font-size:42px; font-weight:bold; color:#d32f2f;">₦{calc_total:,}</span>
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            with st.form("order_form", clear_on_submit=False):
                st.markdown("### 👤 Delivery Details")
                name = st.text_input("Full Name / Company Name")
                phone = st.text_input("Phone Number (11 digits)", placeholder="080...")
                addr = st.text_area("Delivery Address in Abuja")

                submitted = st.form_submit_button("Submit Request & Get Order ID")

                if submitted:
                    if vol_input <= 0:
                        st.error("Please enter a valid amount of litres.")
                    elif not name or not phone or not addr:
                        st.error("Missing information. Please fill all fields.")
                    elif len(phone) != 11 or not phone.isdigit():
                        st.error("Invalid Phone Number. Please enter exactly 11 digits.")
                    else:
                        o_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                        order_data = {
                            "Order_ID": o_id,
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Client_Name": name,
                            "Phone": str(phone),
                            "Address": addr,
                            "Volume": str(vol_input),
                            "Total": str(calc_total),
                            "Status": "Pending"
                        }
                        save_order(order_data)
                        st.session_state.submitted_id = o_id
                        st.rerun()

    # --- TAB 2: TRACKER ---
    with tab2:
        st.markdown(f"### 🔍 Check Status with {COMPANY_NAME}")
        search_id = st.text_input("Enter 5-digit Order ID", key="track_input").strip().upper()
        if st.button("Check Status"):
            if os.path.isfile(DB_FILE):
                df = pd.read_csv(DB_FILE, dtype=str)
                record = df[df['Order_ID'].str.strip().str.upper() == search_id]
                if not record.empty:
                    status = record['Status'].values[0]
                    if status == "Pending":
                        st.info(f"⏳ **PENDING**: Payment verification in progress.")
                    elif status == "Completed":
                        st.success(f"✅ **DELIVERED**: Successfully dropped at {record['Address'].values[0]}.")
                    elif status == "Cancelled":
                        st.error(f"🚫 **CANCELLED**: This order was revoked.")
                    else:
                        st.warning(f"🚫 **STATUS**: {status.upper()}")
                else:
                    st.error("Order ID not found.")

    # --- TAB 3: CANCELLATION ---
    with tab3:
        if 'cancel_success' not in st.session_state:
            st.session_state.cancel_success = False

        if st.session_state.cancel_success:
            st.success("✅ CANCELLATION SUCCESSFUL")
            st.info("The request has been removed from our active delivery list.")
            if st.button("Back to Form"):
                st.session_state.cancel_success = False
                st.rerun()
        else:
            st.markdown("### ❌ Cancel Your Request")
            st.write("Orders can only be cancelled while in 'Pending' status.")
            c_phone = st.text_input("Registered Phone Number", key="can_ph").strip()
            c_id = st.text_input("Order ID", key="can_id").strip().upper()

            if st.button("Confirm Cancellation"):
                if c_phone and c_id:
                    if os.path.isfile(DB_FILE):
                        df = pd.read_csv(DB_FILE, dtype=str)
                        df['Phone'] = df['Phone'].str.strip()
                        df['Order_ID'] = df['Order_ID'].str.strip().str.upper()
                        mask = (df['Phone'] == c_phone) & (df['Order_ID'] == c_id)

                        if mask.any():
                            status_now = df.loc[mask, 'Status'].values[0]
                            if status_now == 'Pending':
                                df.loc[mask, 'Status'] = 'Cancelled'
                                df.to_csv(DB_FILE, index=False, quoting=csv.QUOTE_ALL)
                                st.session_state.cancel_success = True
                                st.rerun()
                            else:
                                st.error(f"🚫 Cannot cancel: Order is already marked as '{status_now}'.")
                        else:
                            st.error("❌ Details do not match our records.")
                    else:
                        st.error("No database found.")
                else:
                    st.warning("Please fill both fields.")