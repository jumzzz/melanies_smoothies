# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingridient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe, max_selections=5
)


# st.text(smoothiefroot_response.json())
if ingridient_list:
    # st.write(ingridient_list)
    # st.text(ingridient_list)

    ingredients_string = ''

    for fruit_chosen in ingridient_list:
        ingredients_string += fruit_chosen + ' '
        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        search_on = pd_df[pd_df['FRUIT_NAME'] == fruit_chosen]['SEARCH_ON'].tolist()[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')

        main_req_uri = f"https://my.smoothiefroot.com/api/fruit/{search_on.lower()}"
        smoothiefroot_response = requests.get(main_req_uri)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
            VALUES ('{ingredients_string}', '{name_on_order}', FALSE)"""

    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


