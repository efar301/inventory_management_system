import streamlit as st
import hmac

st.set_page_config(
    page_title='Login',
    page_icon='🔒',
    layout='centered'
)

def check_password():
    # returns `True` if the user had a correct password.

    def login_form():
        # rorm with widgets to collect user information
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            
            col0, col1, col2, col3 = st.columns(4)
            with col1:
                st.form_submit_button("Login", on_click=password_entered)
            with col2:  
                st.form_submit_button("Login as Guest", on_click=login_as_guest)

    def password_entered():
        # checks whether a password entered by the user is correct.
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(st.session_state["password"], st.secrets.passwords[st.session_state["username"]],):
            st.session_state["password_correct"] = True
            st.session_state['guest_user'] = False
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
            
    def login_as_guest():
        st.session_state["guest_user"] = True
        st.session_state["password_correct"] = True
        return True

    # return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Incorrect Username or Password")
    return False

st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

# wait till password is entered or guest user is selected
if not check_password():
    st.stop()

# switch to the home page     
st.switch_page('pages/home.py')