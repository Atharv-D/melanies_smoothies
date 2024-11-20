# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("  :cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


Name_on_order=st.text_input('Name on smoothies')
st.write('The name of your smoothie will be',Name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
   

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        st.subheader(fruit_chosen +  'Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothieFroot.com/api/fruit/" + fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)



    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" +Name_on_order+"""')"""

    st.write(my_insert_stmt)
   
   
    time_to_insert=st.button('Sumbit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {Name_on_order}!', icon="✅")
     
smoothiefroot_response = requests.get("https://my.smoothieFroot.com/api/fruit/watermelon")
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


