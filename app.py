import random
import databutton as db
import streamlit as st
from twilio.rest import Client

TARGET_DATAFRAME_KEY = "registrations"

# Twilio account details
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

with st.form("register_form"):
    st.header("Register")
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
            from_='your_twilio_number',
            to=mobile_number
        )
        st.success("OTP sent to your mobile number")

    # OTP input field
    otp_input = st.text_input("Enter OTP")

    # Verify OTP button
    if st.button("Verify OTP"):
        # Check if the OTP matches the input
        if str(otp) == otp_input:
            st.success("OTP verified")
        else:
            st.error("Invalid OTP")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Registration successful! Welcome, {first_name}!")

        db.storage.dataframes.add(
            key="form-input",
            entry={
                "first_name": first_name,
                "email": email,
                "mobile_number": mobile_number,
                "timestamp": datetime.now(),
            },
        )```

In this example, the `twilio` package is used to send the OTP to the provided mobile number. You will need to replace the `account_sid`, `auth_token`, and `from_` values with your own Twilio account details.

