import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title = 'Price Predictor',
)
with open('datasets/df.pkl', 'rb') as f:
    df = pickle.load(f)
with open('datasets/pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)
st.header('Enter You Inputs')

# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# bedroom
bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

#bathroom
bathrooms = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

#balcony
balcony = st.selectbox('Number of Balcony', sorted(df['balcony'].unique().tolist()))

#age possession
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

#built_up_area
built_up_area = float(st.number_input('Built Up Area'))

#servant room
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

#store room
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# furnishing type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# luxury_category
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    # form a dataframe
    data = [[property_type, sector, bedrooms, bathrooms,balcony, property_age, built_up_area,
             servant_room,store_room, furnishing_type, luxury_category, floor_category
             ]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)
    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = round(base_price-0.22, 2)
    high = round(base_price+0.22, 2)

    # display
    st.text("The price of the flat is between {} Cr and {} CR".format(low, high))
