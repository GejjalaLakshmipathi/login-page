import random
from datetime import datetime

import databutton as db
import streamlit as st
from twilio.rest import Client

TARGET_DATAFRAME_KEY = "registrations"

# Twilio account details
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_number = 'your_twilio_number'
client = Client(account_sid, auth_token)

@st.cache_data()
def get_data():
    return {}

def register_form():
    data = get_data()
    first_name = st.text_input("First Name")
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    # Generate OTP button
    if st.button("Generate OTP"):
        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)

        # Send the OTP to the provided mobile number using Twilio
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=twilio_number,
            to=mobile_number
        )
        st.success("OTP sent to your mobile number")

        data["otp"] = otp
        data["mobile_number"] = mobile_number

    # OTP input field
    otp_input = st.text_input("Enter OTP")

    # Verify OTP button
    if st.button("Verify OTP"):
        # Check if the OTP matches the input
        if str(data.get("otp")) == otp_input:
            st.success("OTP verified")
            data["verified"] = True
        else:
            st.error("Invalid OTP")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted and data.get("verified"):
        st.success(f"Registration successful! Welcome, {first_name}!")

        db.storage.dataframes.add(
            key="form-input",
            entry={
                "first_name": first_name,
                "email": email,
                "mobile_number": mobile_number,
                "timestamp": datetime.now(),
            },
        )

def main():
    st.header("Register")
    register_form()

if __name__ == "__main__":
    main()
