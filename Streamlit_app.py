import streamlit as st
import snowflake.connector
import pandas

st.title("Zena's Athleisure")

#connect to snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"]) 
my_cur = my_cnx.cursor() 

# run a snowflake query and put it all in a var called my_catalog 
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") 
my_catalog = my_cur.fetchall()
#my_data_row = my_cur.fetchone() 

# put the dafta into a dataframe
df = pandas.DataFrame(my_catalog) 

# temp write the dataframe to the page so I Can see what I am working with 
# streamlit.write(df) 

# put the first column into a list 
color_list = df[0].values.tolist() 
# print(color_list)

# Let's put a pick list here so they can pick the color 
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))


# We'll build the image caption now, since we can 
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!' 
# use the option selected to go back and get all the info from the database


my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';") 
df2 = my_cur.fetchone() 
st.image( df2[0], width=400, caption= product_caption ) 
st.write('Price: ', df2[1]) 
st.write('Sizes Available: ',df2[2]) 
st.write(df2[3])
