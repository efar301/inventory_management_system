import streamlit as st
from database.connection import get_df, display_de, change_box_qty, remove_box_inventory, update_box_data

st.set_page_config(
    page_title='Boxes',
    page_icon='📦',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# home button positioning
col_home, col_title = st.columns([1, 4])
with col_home:
    if st.button('🏠'):
        st.switch_page('pages/home.py')

# title 
st.markdown("<h1 style='text-align: center;'>Box Inventory</h1>", unsafe_allow_html=True)

# display data editor
display_de('boxes')

# popup for adjusting inventory
@st.dialog('Adjust Inventory')
def adj_inv():
    l = st.number_input('Length', min_value=1, step=1)
    w = st.number_input('Width', min_value=1, step=1)
    h = st.number_input('Height', min_value=1, step=1)
    qty = st.number_input('New Quantity', min_value=1, step=1)
    notes = st.text_input('Notes', value=' ')
    
    col0, col1, col2, col3 = st.columns([.5, 1, 1, .5])
    with col1:
        if st.button('Update', key='update_box_qty'):
            change_box_qty(l, w, h, qty, notes)
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button('Remove'):
            remove_box_inventory(l, w, h)
            st.cache_data.clear()
            st.rerun()
        
# buttons for updating and adjusting inventory
col0, col1, col2, col3 = st.columns([.5, 1, 1, .5])
with col1:
    if st.button('Update', key='update_data_editor'):
        edited_rows = st.session_state.get("editor_boxes", {}).get("edited_rows", {})
        update_box_data(get_df('boxes'), edited_rows)
with col2:
    if st.button('Adjust Inventory', key='boxes_adj_inv'):
        adj_inv()
