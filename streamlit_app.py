#SiS Zena's Web Catalog Prototype
#Import python packages

import streamlit as st 
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" Zena's Amazing Athleisure Catalog ")
# st.write(
  # """Pick a sweatsuit color or style
  # """
# )


cnx=st.connection("snowflake")
session= cnx.session()

my_dataframe = session.table("zenas_athleisure_db.products.catalog_for_website").select(col('COLOR_OR_STYLE'),col('price'), col('file_name'), col('file_url'), col('size_list'), col('upsell_product_desc'))
zenas_list = st.multiselect('Pick a sweatsuit color or style'
    ,my_dataframe
    ,max_selections=1
)
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_string=''

if zenas_list:
  
  for color_or_size in zenas_list:
    #ingredients_string += color_or_size + ' '

    search_on=pd_df.loc[pd_df['COLOR_OR_STYLE'] == color_or_size, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', color_or_size,' is ', search_on, '.')

    st.stop()
    
    st.subheader(color_or_size+'Information')
    smoothiefroot_response = requests.get(f"https://www.smoothiefroot.com/api/fruit/{search_on}")
    sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

st.write(ingredients_string)

name_on_order = title
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

st.write(my_insert_stmt)

time_to_insert =st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+ name_on_order +'!', icon="✅")
