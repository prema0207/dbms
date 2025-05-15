import streamlit as st
from db import get_connection
from pdf_gen import generate_pdf

st.set_page_config(page_title="Certificate Generator", layout="centered")

st.title("🎓 Online Certificate Generator")

menu = st.sidebar.selectbox("Menu", ["Apply", "Admin"])

# User Form
if menu == "Apply":
    st.header("Apply for a Certificate")
    name = st.text_input("Full Name")
    cert_type = st.selectbox("Certificate Type", ["Income", "Community"])
    details = st.text_area("Certificate Details")

    if st.button("Submit Application"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO applications (user_id, certificate_type, details) VALUES (%s, %s, %s)",
                       (1, cert_type.lower(), details))
        conn.commit()
        conn.close()
        st.success("Application submitted successfully!")

# Admin Panel
if menu == "Admin":
    st.header("Admin Panel")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications WHERE status='pending'")
    rows = cursor.fetchall()

    for row in rows:
        with st.expander(f"{row['certificate_type'].title()} Request - ID: {row['id']}"):
            st.write(f"Name: {row['user_id']} (User ID)")
            st.write(f"Details: {row['details']}")

            if st.button(f"Approve ID {row['id']}"):
                # For simplicity, fake user name
                filename = generate_pdf("User" + str(row['user_id']), row['certificate_type'], row['details'])

                cursor.execute("UPDATE applications SET status='approved', certificate_file=%s WHERE id=%s",
                               (filename, row['id']))
                conn.commit()
                st.success(f"Approved and generated certificate for ID {row['id']}")

    conn.close()
