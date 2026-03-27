# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie !
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
# Display the smoothiefroot nutrition information, using the APIs
import requests  
# Code that failed: That is Markdown link syntax, not a raw URL.
# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# requests.get() expects a plain URL like:
url = "https://my.smoothiefroot.com/api/fruit/watermelon"
try:
    smoothiefroot_response = requests.get(url, timeout=10)
    smoothiefroot_response.raise_for_status()

    data = smoothiefroot_response.json()
    st.dataframe(data=data, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f"API request failed: {e}")
