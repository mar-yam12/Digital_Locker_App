import streamlit as st
import os, json
from locker import DigitalLocker
from hashlib import sha256

USER_FILE = "users.json"
DATA_FOLDER = "data"
def load_custom_css(file_path="style.css"):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Ensure data folder exists


# Load or create user file
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)


# Title and Description
st.set_page_config(page_title="Digital Locker", page_icon="🔐")
st.title("🔐 Digital Locker")
st.markdown("Securely store and manage your files with encryption.")
load_custom_css()

# Session Init
if "user" not in st.session_state:
    st.session_state.user = None
if "locker" not in st.session_state:
    st.session_state.locker = None

# Load users
with open(USER_FILE, "r") as f:
    users = json.load(f)

# Set Username and Password
with st.expander("🆕 Set Username and Password"):
    new_user = st.text_input("Username")
    new_pwd = st.text_input("Password", type="password")
    if st.button("🆕 Set Password"):
        if new_user in users:
            st.error("Username already exists!")
        else:
            users[new_user] = sha256(new_pwd.encode()).hexdigest()
            with open(USER_FILE, "w") as f:
                json.dump(users, f)
            st.success("User Registered! 🤝")

# Unlock

with st.expander("🔑 Unlock Your Locker"):
   if not st.session_state.user:
    user = st.text_input("👤 Username", key="login_user")
    pwd = st.text_input("🔒 Password", type="password", key="login_pwd")
    if st.button("Unlock Locker 🔓"):
        if user in users and users[user] == sha256(pwd.encode()).hexdigest():
            st.session_state.user = user
            st.session_state.locker = DigitalLocker(user, pwd)
            st.success(f"Welcome, {user}! 👋")
        else:
            st.error("Invalid credentials.")
    

# Locker Interface
if st.session_state.user:
    st.subheader(f"Welcome, {st.session_state.user} 👋")

    tab1, tab2 = st.tabs(["📤 Upload Documents", "📑 Locker Contents"])

    with tab1:
        file = st.file_uploader("📤 Upload Documents", type=["pdf", "txt", "jpg", "png"])
        if st.button("Upload"):
            if file:
                st.session_state.locker.add_item(file.name, file.read())
                st.success(f"{file.name} uploaded!")

    with tab2:
        files = st.session_state.locker.list_items()
        if files:
            for f in files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"📄 {f}")
                with col2:
                    decrypted = st.session_state.locker.get_item(f)
                    st.download_button("⬇️ Download", decrypted, file_name=f)
                with col3:
                    if st.button("🗑️ Delete", key=f):
                        st.session_state.locker.delete_item(f)
                        st.success(f"{f} deleted.")
                        st.rerun()
        else:
            st.info("No files uploaded yet.")

    if st.button("🚪 Lock Again..!!"):
        st.session_state.user = None
        st.session_state.locker = None
        st.rerun()
