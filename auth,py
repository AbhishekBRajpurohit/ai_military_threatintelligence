import streamlit as st


def check_password():
    """
    Returns True if the user is authenticated.
    Set APP_PASSWORD in .streamlit/secrets.toml — never hardcode it here.
    """

    def password_entered():
        if st.session_state.get("password") == st.secrets.get("APP_PASSWORD"):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if st.session_state.get("authenticated"):
        return True

    st.title("🔒 Login Required")
    st.text_input("Password", type="password", key="password", on_change=password_entered)

    if "authenticated" in st.session_state and not st.session_state["authenticated"]:
        st.error("Incorrect password.")

    return False