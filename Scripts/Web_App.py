import streamlit as st
import psycopg2
import sys 
sys.path.extend([r'C:\Users\Usuario\OneDrive\Desktop\Learning-Testing\PyStrava',
                 r'C:\Users\Usuario\OneDrive\Desktop\Learning-Testing\PyStrava\Scripts'])
from Functions import *
from StravaCredentials import *

# Establishing connection to PyStrava database
conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

# Creating a cursor and also quering the database to get the current list of workouts from activity table
cur = conn.cursor()
query = "select activity_id from activity limit 10"

# Executing cursor 
cur.execute(query)

# Fetching the column names
column_names = [desc[0] for desc in cur.description]

data = cur.fetchall()

st.title('PyStrava')
st.sidebar.success('Workouts')

df = pd.DataFrame(data, columns = column_names)
st.dataframe(df)

st.set_page_config(page_title="PyStrava", page_icon="", layout="centered", menu_items=None)