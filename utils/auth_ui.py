import streamlit as st
from auth import check_password, logout_button


def require_login():
    """
    Call this as the first line of logic in any page.
    Stops execution if not authenticated, otherwise shows a
    logout button in the sidebar and lets the page continue.
    """
    if not check_password():
        st.stop()
    logout_button()