import streamlit as st

st.set_page_config(
    page_title='Home',
    page_icon='📦',
    layout='centered',
    initial_sidebar_state='collapsed'
) 

# true if checkbox is checked for 'show low inventory'
st.session_state['show_low_inv'] = False

from database.connection import display_df, get_df

# buttons for login and show low inventory
col_home_button, col_title, col_low_inv_button = st.columns([1, 4, 1])
with col_home_button:
    if st.button('Login'):
        st.session_state['password_correct'] = False
        st.switch_page('pages/login.py')
        
with col_low_inv_button:
    if st.checkbox('Show Low Inventory'):
        st.session_state['show_low_inv'] = True
        
# main title
st.markdown("<h1 style='text-align: center;'>Inventory Management</h1>", unsafe_allow_html=True)


# navigation buttons for pages
col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 1])
with col1:
    if st.button('Box Inventory') and st.session_state['guest_user'] == False:
        st.switch_page("pages/box_inventory.py")
with col2:
    if st.button('Wood Inventory') and st.session_state['guest_user'] == False:
        st.switch_page("pages/wood_inventory.py")
with col3:
    if st.button('Misc Inventory') and st.session_state['guest_user'] == False:
        st.switch_page("pages/misc_inventory.py")
        

# get low inventory data 
low_box_inv = get_df('boxes')
low_box_inv = low_box_inv[low_box_inv['qty'] <= 5]

low_wood_inv = get_df('wood')
low_wood_inv = low_wood_inv[low_wood_inv['qty'] <= 2]

low_misc_inv = get_df('misc')        
low_misc_inv = low_misc_inv[low_misc_inv['qty'] <= 2]

if st.session_state['show_low_inv']:
    
    if low_box_inv.empty and low_wood_inv.empty and low_misc_inv.empty:
        st.markdown("<h3 style='text-align: center;'>No Low Inventory</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='text-align: center;'>Low Inventory</h3>", unsafe_allow_html=True)
        st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)
    


    # display Boxes if there is data
    if not low_box_inv.empty:
        st.markdown("<h3 style='text-align: center;'>Boxes</h3>", unsafe_allow_html=True)
        st.dataframe(low_box_inv, use_container_width=True, hide_index=True)
        st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)

    # display Wood if there is data
    if not low_wood_inv.empty:
        st.markdown("<h3 style='text-align: center;'>Wood</h3>", unsafe_allow_html=True)
        st.dataframe(low_wood_inv, use_container_width=True, hide_index=True)
        st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)

    # display Misc if there is data
    if not low_misc_inv.empty:
        st.markdown("<h3 style='text-align: center;'>Misc</h3>", unsafe_allow_html=True)
        st.dataframe(low_misc_inv, use_container_width=True, hide_index=True)
        st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)
        
# quick look at box inventory
st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Current Box Inventory</h3>", unsafe_allow_html=True)
display_df('boxes')

# quick look at wood inventory
st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Current Wood Inventory</h3>", unsafe_allow_html=True)
display_df('wood')

# quick look at misc inventory
st.markdown('<hr style="border:2px solid white;">', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Current Misc Inventory</h3>", unsafe_allow_html=True)
display_df('misc')