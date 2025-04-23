import streamlit as st
from locker import DigitalLocker

# Add background CSS
def add_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Setup
st.set_page_config("🔐 Digital Locker App")
add_background("https://www.shutterstock.com/image-vector/cyber-security-information-network-protection-600nw-653839552.jpg")
st.title("📂 Digital Locker")
st.markdown("Securely upload and manage your documents.")

# Session locker init
if "locker" not in st.session_state:
    st.session_state.locker = None
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "password_set" not in st.session_state:
    st.session_state.password_set = False

# 🔑 Set Password
if not st.session_state.password_set:
    with st.form("set_password_form"):
        st.subheader("🔑 Set Your Locker Password")
        new_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.form_submit_button("Set Password"):
            if new_password and new_password == confirm_password:
                st.session_state.locker = DigitalLocker(password=new_password)
                st.session_state.password_set = True
                st.success("Password set successfully! You can now unlock your locker.")
            else:
                st.error("Passwords do not match or are empty. Please try again.")

# 🔑 Unlock Locker
if st.session_state.password_set and not st.session_state.unlocked:
    with st.form("unlock_form"):
        st.subheader("🔐 Enter Locker Password")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Unlock"):
            if st.session_state.locker.check_password(pwd):
                st.success("Locker Unlocked ✅")
                st.session_state.unlocked = True
            else:
                st.error("Incorrect Password ❌")

# 📁 If Unlocked
if st.session_state.unlocked:
    tab1, tab2 = st.tabs(["📤 Upload Documents", "📑 Locker Contents"])

    with tab1:
        st.subheader("📤 Upload Document")
        with st.form("upload_form"):
            uploaded_file = st.file_uploader("Upload a file", type=["pdf", "png", "jpg", "jpeg", "txt"])
            if st.form_submit_button("Upload"):
                if uploaded_file:
                    with st.spinner("Uploading..."):
                        st.session_state.locker.add_item(uploaded_file.name, uploaded_file.getvalue())
                        st.success(f"{uploaded_file.name} added to locker!")

    with tab2:
        st.subheader("📑 Locker Contents")
        items = st.session_state.locker.list_items()
        if items:
            for item in items:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**📄 {item.filename}**")
                with col2:
                    decrypted_data = st.session_state.locker.decrypt_data(item.filedata)
                    st.download_button("⬇️ Download", decrypted_data, file_name=item.filename)
                with col3:
                    if st.button(f"🗑️ Delete", key=item.filename):
                        confirm = st.confirm(f"Are you sure you want to delete {item.filename}?")
                        if confirm:
                            st.session_state.locker.delete_item(item.filename)
                            st.experimental_rerun()
        else:
            st.info("No documents stored yet.")

    # 🔒 Lock Again
    if st.button("🔒 Lock Again"):
        st.session_state.unlocked = False
        st.rerun()
