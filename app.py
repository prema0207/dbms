import streamlit as st

st.title("Online Certificate Generator")

name = st.text_input("Enter your Name")
purpose = st.text_input("Enter Purpose of Certificate")

if st.button("Generate Certificate"):
    if name and purpose:
        certificate = f"""
        ---
        🏛️ **Government Authority**

        📄 **Certificate of Purpose**

        This is to certify that **{name}** has applied for **{purpose}**.

        🗓️ Issued on: {st.date_input("Issue Date")}

        ---
        """
        st.markdown(certificate)
    else:
        st.warning("Please enter both name and purpose.")
