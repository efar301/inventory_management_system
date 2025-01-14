import streamlit as st
from streamlit_free_text_select import st_free_text_select
from database.connection import display_de, update_misc_data, get_df, remove_misc_inventory, change_misc_qty


st.set_page_config(
    page_title='Home',
    page_icon='📁',
    layout='centered',
    initial_sidebar_state='collapsed'
) 

# home button positioning
col_home_button, col_title = st.columns([1, 4])
with col_home_button:
    if st.button('🏠'):
        st.switch_page('pages/home.py')
   
# title     
st.markdown("<h1 style='text-align: center;'>Miscellaneous Inventory</h1>", unsafe_allow_html=True)

# display data editor
display_de('misc')

# popup for adjusting inventory 
@st.dialog('Adjust Inventory')
def adj_inv():
    
    item = st_free_text_select('Item', get_df('misc')['item'].tolist())
    notes = st.text_input('Notes', value='')
    qty = st.number_input('New Quantity', min_value=1, step=1)
    
    col0, col1, col2, col3 = st.columns([.5, 2, 2, .5])
    with col1:
        if st.button('Update', key='update_misc_qty'):
            change_misc_qty(item, notes, qty)
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button('Remove Item', key='remove_misc_item'):
            remove_misc_inventory(item)
            st.cache_data.clear()
            st.rerun()

# buttons for updating and adjusting inventory
col0, col1, col2, col3 = st.columns([.5, 1, 1, .5])
with col1:
    if st.button('Update', key='update_data_editor'):
        edited_rows = st.session_state.get("editor_misc", {}).get("edited_rows", {})
        update_misc_data(get_df('misc'), edited_rows)
with col2:
    if st.button('Adjust Inventory', key='misc_adj_inv'):
        adj_inv()
        
