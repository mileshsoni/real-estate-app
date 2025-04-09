import streamlit as st
import pickle
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Recommend Apartments",
)
location_df = pd.read_csv('datasets/location_df.csv', index_col = 'PropertyName')
cosine_sim1 = np.load('datasets/cosine_sim1.npy')
cosine_sim2 = np.load('datasets/cosine_sim2.npy')
cosine_sim3 = np.load('datasets/cosine_sim3.npy')
st.title('Select Location and Radius')
def recommend_properties_with_scores(property_name, top_n = 247):
  cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
  sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
  sorted_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
  top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
  top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
  top_properties = location_df.index[top_indices].tolist()
  return pd.DataFrame({'PropertyName': top_properties, 'SimilarityScore': top_scores})

property_name = st.selectbox('Location', sorted(location_df.columns.tolist()))
distance = st.number_input('Radius in Kms')
if st.button('Search'):
    nearby_properties = location_df[location_df[property_name] < distance*1000][property_name].sort_values()
    if len(nearby_properties) == 0:
        st.text('There are no properties nearby')

    for key, value in nearby_properties.items():
        st.text(str(key) +" -> "+ str(round(value/1000)) + " kms")

st.header('Recommend Apartments')
selected_apartment = st.selectbox('Select an apartment', sorted(location_df.index))
if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)
    st.dataframe(recommendation_df)