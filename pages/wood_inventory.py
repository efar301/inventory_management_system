import streamlit as st
from streamlit_free_text_select import st_free_text_select
from database.connection import get_df, display_de, change_wood_qty, remove_wood_inventory, update_wood_data

st.set_page_config(
    page_title='Home',
    page_icon=':wood:',
    layout='centered',
    initial_sidebar_state='collapsed'
) 

wood_dict = {
        '1/2 baltic birch plywood': {'l': 96, 'w': 48, 'h': .5},
        '3/16ths unfin bottom': {'l': 96, 'w': 48, 'h': .1875},
        '3/16ths fin bottom': {'l': 96, 'w': 48, 'h': .1875},
        '1/8th baltic birch plywood': {'l': 60, 'w': 60, 'h': .125},
        '1/2 plywood drawer bottom': {'l': 96, 'w': 48, 'h': .5}
}

# home button positioning
col_home, col_title = st.columns([1, 4])
with col_home:
    if st.button('🏠'):
        st.switch_page('pages/home.py')

# title
st.markdown("<h1 style='text-align: center;'>Wood Inventory</h1>", unsafe_allow_html=True)

# display data editor
display_de('wood')

# popup for adjusting inventory
@st.dialog('Adjust Inventory')
def adj_inv():
    
    # get options
    df = get_df('wood')
    options = df['type'].tolist()
    extras = ['1/2 baltic birch plywood', '3/16ths unfin bottom', '3/16ths fin bottom', '1/8th baltic birch plywood', '1/2 plywood drawer bottom']
    
    # if options not availible add extra default ones
    for i in range(len(extras)):
        if extras[i] not in options:
            options.append(extras[i])
    
    type = st_free_text_select('Type', options)
    
    l = st.number_input('Length', min_value=1, step=1, value=wood_dict.get(type, {}).get('l', 1))
    w = st.number_input('Width', min_value=1, step=1, value=wood_dict.get(type, {}).get('w', 1))
    h = st.number_input('Height', min_value=0.0, step=.01, value=wood_dict.get(type, {}).get('h', 0.0), format='%0.4f')
    qty = st.number_input('New Quantity', min_value=1, step=1)
    
    col0, col1, col2, col3 = st.columns([.5, 2, 2, .5])
    with col1:
        if st.button('Update', key='update_wood_qty'):
            change_wood_qty(l, w, h, type, qty),
            st.cache_data.clear()
            st.rerun()
            
    with col2:
        if st.button('Remove Wood Type', key='remove_wood_type'):
            remove_wood_inventory(l, w, h, type)
            st.cache_data.clear()
            st.rerun()

# remove wood popup
@st.dialog('Remove Wood Type')
def remove_wood():
    df = get_df('wood')
    options = df['type'].tolist()
    
    type = st_free_text_select('Type', options)
    
    l = st.number_input('Length', min_value=1, step=1, value=wood_dict.get(type, {}).get('l', 1))
    w = st.number_input('Width', min_value=1, step=1, value=wood_dict.get(type, {}).get('w', 1))
    h = st.number_input('Height', min_value=0.0, step=.01, value=wood_dict.get(type, {}).get('h', 0.0), format='%0.4f')
    
    if st.button('Remove'):
        remove_wood_inventory(l, w, h, type)
        st.cache_data.clear()
        st.rerun()
            
# buttons for updating and adjusting inventory   
col0, col1, col2, col3 = st.columns([.5, 1, 1, .5])
with col1:
    if st.button('Update', key='update_wood_data_editor'):
        edited_rows = st.session_state.get("editor_wood", {}).get("edited_rows", {})
        update_wood_data(get_df('wood'), edited_rows)
with col2:
    if st.button('Adjust Inventory', key='wood_ajd_inv'):
        adj_inv()
