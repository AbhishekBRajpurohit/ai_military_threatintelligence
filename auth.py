import streamlit as st
import time

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60

def _inject_login_css():
    st.markdown("""
        <style>
        .login-wrapper {
            max-width: 420px;
            margin: 8vh auto 0 auto;
            padding: 2.5rem 2.5rem 2rem 2.5rem;
            background: linear-gradient(180deg, rgba(30,32,40,0.9) 0%, rgba(20,22,28,0.9) 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            text-align: center;
        }
        .login-icon {
            font-size: 42px;
            margin-bottom: 0.5rem;
        }
        .login-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: #f0f0f0;
        }
        .login-subtitle {
            font-size: 0.9rem;
            color: #9a9a9a;
            margin-bottom: 1.75rem;
        }
        .login-footer {
            margin-top: 1.5rem;
            font-size: 0.75rem;
            color: #666;
        }
        div[data-testid="stTextInput"] input {
            border-radius: 8px !important;
        }
        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 0;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
def check_password():
    """
    Returns True if the user is authenticated.
    Set APP_PASSWORD in .streamlit/secrets.toml — never hardcode it here.
    Includes a simple attempt counter with a temporary lockout after
    repeated failed tries.
    """
    if st.session_state.get("authenticated"):
        return True

    st.session_state.setdefault("login_attempts", 0)
    st.session_state.setdefault("lockout_until", 0)

    _inject_login_css()

    now = time.time()
    locked_out = now < st.session_state["lockout_until"]

    left, center, right = st.columns([1, 1.4, 1])
    with center:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="login-icon">🛡️</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">GTD Analytics Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Enter your password to continue</div>', unsafe_allow_html=True)
if locked_out:
            remaining = int(st.session_state["lockout_until"] - now)
            st.error(f"🔒 Too many failed attempts. Try again in {remaining}s.")
        else:
            with st.form("login_form", clear_on_submit=False):
                password = st.text_input("Password", type="password", label_visibility="collapsed",
                                          placeholder="Password")
                submitted = st.form_submit_button("🔓 Log In")

            if submitted:
                correct = st.secrets.get("APP_PASSWORD")
                if correct is None:
                    st.error("No APP_PASSWORD configured in .streamlit/secrets.toml")
                elif password == correct:
                    st.session_state["authenticated"] = True
                    st.session_state["login_attempts"] = 0
                    st.rerun()
                else:
                    st.session_state["login_attempts"] += 1
                    remaining_tries = MAX_ATTEMPTS - st.session_state["login_attempts"]

                    if remaining_tries <= 0:
                        st.session_state["lockout_until"] = now + LOCKOUT_SECONDS
                        st.session_state["login_attempts"] = 0
                        st.error(f"🔒 Too many failed attempts. Locked for {LOCKOUT_SECONDS}s.")
                    else:
                        st.error(f"❌ Incorrect password. {remaining_trst.markdown(
            '<div class="login-footer">GTD Analytics · Research & Educational Use Only</div>',
            unsafe_allow_html=True
        )st.markdown('</div>', unsafe_allow_html=True)

    return False