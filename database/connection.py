import streamlit as st
import pandas as pd
from sqlalchemy import text
import datetime

conn = st.connection('mysql', type='sql')

# returns a dataframe of sql table requested
def get_df(table):
    if table not in ['boxes', 'wood', 'misc']:
        return
    
    df = conn.query(f'SELECT * FROM {table}', ttl=0)
    df = df.drop(columns='id', axis=1)
    return df

# displays a dataframe of sql table requested 
def display_df(table):
    df = get_df(table)
    st.dataframe(df, use_container_width=True, hide_index=True, selection_mode='single-row', on_select='ignore')


# displays a data editor for sql table requested     
def display_de(table):
    de = get_df(table)
    
    edit_dict = {'boxes': {'widget_key': 'editor_boxes', 'disabled_rows': ['l', 'w', 'h', 'notes', 'last updated']}, 
                 'wood': {'widget_key': 'editor_wood', 'disabled_rows': ['l', 'w', 'h', 'type', 'last updated']}, 
                 'misc': {'widget_key': 'editor_misc', 'disabled_rows': ['item', 'notes', 'last updated']}
    }
    
    return st.data_editor(de,
                          use_container_width=True, 
                          hide_index=True,
                          key=edit_dict.get(table).get('widget_key'), 
                          disabled=edit_dict.get(table).get('disabled_rows')
                          )
    
# changes the quantity of a box in the inventory
def change_box_qty(l, w, h, qty, notes):
    with conn.session as s:
        check_query = text('SELECT * FROM boxes WHERE l = :l AND w = :w AND h = :h')
        result = s.execute(check_query, {'l': l, 'w': w, 'h': h}).scalar()
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if result:
            update_query = text('UPDATE boxes SET qty = :qty, "last updated" = :date WHERE l = :l AND w = :w AND h = :h')
            s.execute(update_query, {'l': l, 'w': w, 'h': h, 'qty': qty, 'notes': notes, 'date': date}) 
            print('Updated Box Quantity')
        
        else:
            insert_query = text('INSERT INTO boxes (l, w, h, qty, notes, "last updated") VALUES (:l, :w, :h, :qty, :notes, :date);')
            s.execute(insert_query, {'l': l, 'w': w, 'h': h, 'qty': qty, 'notes': notes, 'date': date}) 
            print('Added Box to Inventory')
            
        s.commit()
        
    print('Completed Successfully!')
    print()

# removes a box from the inventory
def remove_box_inventory(l, w, h):
    with conn.session as s:
        query = text('DELETE FROM boxes WHERE l = :l AND w = :w AND h = :h')
        s.execute(query, {'l': l, 'w': w, 'h': h})
        s.commit()
        
    print(f'Removed Box with dimensions {l}x{w}x{h} from Inventory')
    print()

# changes the quantity of wood in the inventory
def change_wood_qty(l, w, h, type, qty):
    with conn.session as s:
        check_query = text('SELECT * FROM wood WHERE l = :l AND w = :w AND h = :h AND type = :type')
        result = s.execute(check_query, {'l': l, 'w': w, 'h': h, 'type': type}).scalar()
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    
        if result:
            update_query = text('UPDATE wood SET qty = :qty, "last updated" = :date WHERE l = :l AND w = :w AND h = :h AND type = :type')
            s.execute(update_query, {'l': l, 'w': w, 'h': h, 'type': type, 'qty': qty, 'date': date})
            print('Added Wood to Inventory')
            
        else:
            insert_query = text('INSERT INTO wood (l, w, h, type, qty, "last updated") VALUES (:l, :w, :h, :type, :qty, :date)')
            s.execute(insert_query, {'l': l, 'w': w, 'h': h, 'type': type, 'qty': qty, 'date': date})
            print('Updated Wood Quantity')
        
        s.commit()
    print('Completed Successfully!')
    print()

# removes wood from the inventory  
def remove_wood_inventory(l, w, h, type):
    with conn.session as s:
        query = text('DELETE FROM wood WHERE l = :l AND w = :w AND h = :h AND type = :type')
        s.execute(query, {'l': l, 'w': w, 'h': h, 'type': type})
        s.commit()
        
    print(f'Removed {type} from Inventory')
    print()
  
# updates the box inventory by processing changes in the box data editor    
def update_box_data(df, edited_rows):
    with conn.session as s:
        for row_idx, changes in edited_rows.items():
            row = df.iloc[row_idx].copy()
            for col_name, new_val in changes.items():
                row[col_name] = new_val  # update local DataFrame row
            
            query = text("""
                UPDATE boxes
                SET qty = :qty, "last updated" = :date
                WHERE l = :l AND w = :w AND h = :h
            """)
            params = {
                "qty":  row["qty"],
                "l":    row["l"],
                "w":    row["w"],
                "h":    row["h"],
                "date": datetime.datetime.now().strftime('%Y-%m-%d')
            }
            s.execute(query, params)
        s.commit()
    print('Updated Box Inventory')
    print()

# updates the misc qty 
def change_misc_qty(item, notes, qty):
    with conn.session as s:
        check_query = text('SELECT * FROM misc WHERE item = :item')
        result = s.execute(check_query, {'item': item}).scalar()
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if result:
            update_query = text('UPDATE misc SET qty = :qty, "last updated" = :date WHERE item = :item')
            s.execute(update_query, {'item': item, 'qty': qty, 'notes': notes, 'date': date}) 
            print('Updated Misc Inventory')
        
        else:
            insert_query = text('INSERT INTO misc (item, qty, notes, "last updated") VALUES (:item, :qty, :notes, :date);')
            s.execute(insert_query, {'item': item, 'qty': qty, 'notes': notes, 'date': date})
            print('Added Item to Inventory')
            
        s.commit()
        print('Completed Successfully!')
        print()

# removes misc from the inventory
def remove_misc_inventory(item):
    with conn.session as s:
        query = text('DELETE FROM misc WHERE item = :item')
        s.execute(query, {'item': item})
        s.commit()
    
    print(f'Removed {item} from Inventory')
    print()
    
# updates the wood inventory by processing changes in the wood data editor
def update_wood_data(df, edited_rows):
    # open a new session
    with conn.session as s:
        for row_idx, changes in edited_rows.items():
            row = df.iloc[row_idx].copy()
            for col_name, new_val in changes.items():
                row[col_name] = new_val  # update local dataframe row

            query = text("""
                UPDATE wood
                SET qty = :qty, "last updated" = :date
                WHERE l = :l AND w = :w AND h = :h AND type = :type
            """)
            params = {
                "qty":  row["qty"],
                "l":    row["l"],
                "w":    row["w"],
                "h":    row["h"],
                "type": row["type"],
                "date": datetime.datetime.now().strftime('%Y-%m-%d')
            }
            s.execute(query, params)
        s.commit()
        
    print('Updated Wood Inventory')
    print()

# updates the misc inventory by processing changes in the misc data editor
def update_misc_data(df, edited_rows):
    # open a new session
    with conn.session as s:
        for row_idx, changes in edited_rows.items():
            row = df.iloc[row_idx].copy()
            for col_name, new_val in changes.items():
                row[col_name] = new_val  # update local dataframe row

            query = text("""
                UPDATE misc
                SET qty = :qty, "last updated" = :date
                WHERE item = :item
            """)
            params = {
                "qty":  row["qty"],
                "item": row["item"],
                "date": datetime.datetime.now().strftime('%Y-%m-%d')
            }
            s.execute(query, params)
        s.commit()
        
    print('Updated Misc Inventory')
    print()   