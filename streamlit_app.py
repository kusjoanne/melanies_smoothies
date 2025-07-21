# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!:
  """
)

name = st.text_input("Your Name:")
st.write("The name to call for your smoothie is: ", name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients:
    ingredients_string = ''

    for fruit in ingredients:
        ingredients_string += fruit + ' '
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name + """', '""" + ingredients_string + """')"""

    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name + '!', icon="✅")
