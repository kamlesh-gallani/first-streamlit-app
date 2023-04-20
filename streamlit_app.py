
import streamlit as st
import pandas
import requests
import snowflake.connector 
from urllib.error import URLError

st.title("My parent's new healthy diner")

st.header('Breakfast Favorites')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# st.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

# Function to get fruity vide data
def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

def add_fruit_to_the_list(fruit_choice):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" +  fruit_choice + "')")
        return "Thanks for adding " + fruit_choice

# Section to display fruity vice api response
st.header("View our Fruit List - Add your favorites!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:
        response = get_fruityvice_data(fruit_choice)
        st.dataframe(response)
        
except URLError as e:
    st.error()

if st.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)


second_fruit_choice = st.text_input('Which fruit you would like to add?')
if st.button('Add ' + second_fruit_choice + ' to the list'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   response = add_fruit_to_the_list(second_fruit_choice) 
   st.text(response)

st.stop()

