import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import ast
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import seaborn as sns
st.set_page_config(
    page_title = "Analytics",
)
def sort_key(s):
    match = re.match(r"sector (\d+)", s.lower())
    if match:
        return (0, int(match.group(1)))  # prioritize numbered sectors
    else:
        return (1, s.lower())  # then sort the rest alphabetically
wordcloud_df = pd.read_csv('datasets/wordcloud.csv')
new_df = pd.read_csv('datasets/data_viz1.csv')
sector_options = sorted(new_df['sector'].unique().tolist(), key=sort_key)
sector_options.insert(0, 'overall')
def plot_word_cloud_for_sector(sector_name) :
  main = []
  temp_df = wordcloud_df
  if sector_name != 'overall' :
    temp_df = wordcloud_df[wordcloud_df['sector'] == sector_name]
  for item in  temp_df['features'].dropna().apply(ast.literal_eval):
    main.extend(item)
  feature_text = ' '.join(temp_df['features'].dropna())
  plt.rcParams['font.family'] = 'Arial'
  wordcloud = WordCloud(width=600, height=600, background_color='black',
                      stopwords=set(['s']),
                      min_font_size=10,
                      ).generate(feature_text)
  plt.figure(figsize = (8,8), facecolor = None)
  plt.imshow(wordcloud, interpolation = 'bilinear')
  plt.axis('off')
  plt.tight_layout(pad = 0)
  st.pyplot(plt)
st.title("Analytics")

group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
fig = px.scatter_mapbox(
    group_df,
    lat='latitude',
    lon='longitude',
    hover_name='sector',
    color='price_per_sqft',
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style='open-street-map',
    text='sector',
    height=700,
    width=1200
)
st.header('Distribution of price per sqft across sectors')
st.plotly_chart(fig)

# amenities
st.header('Amenities Word Cloud')
sector_info = st.selectbox('Select Sector',sector_options, key='amenities')
plot_word_cloud_for_sector(sector_info)

# scatter plot between area and price
st.header('Area Vs Price')
property_type = st.selectbox('Select Property Type', ['flat', 'house'])
fig = px.scatter(new_df[new_df['property_type'] == property_type], x = 'built_up_area', y = 'price', color = 'bedRoom').update_layout(
    xaxis_title="Area", yaxis_title="Price"
)
st.plotly_chart(fig, user_container_width=True)

# pie chart
st.header('BHK Pie Chart')
selected_sector = st.selectbox('Select Sector', sector_options, key='sector_pie')
if selected_sector == 'overall':
    fig = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig, user_container_width=True)
else :
    fig = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig, user_container_width=True)

# box plot
st.header('Side by Side BHK price comparison')
temp_df = new_df[new_df['bedRoom'] <= 4]
fig = px.box(temp_df, x = 'bedRoom', y = 'price').update_layout(
    xaxis_title="BHK", yaxis_title="Price in Cr"
)
st.plotly_chart(fig, user_container_width=True)

# distribution plot
st.header('Side by Side Distribution Plot for Property Type')
sns.set_style("dark")

# Set dark background
plt.style.use("dark_background")

# Create the plot
fig = plt.figure(figsize=(10, 8))

# Plot histogram + KDE for house
sns.histplot(data=new_df[new_df['property_type'] == 'house'], x='price', kde=True, label='House', color='#FF6B6B', stat='density', element='step')

# Plot histogram + KDE for flat
sns.histplot(data=new_df[new_df['property_type'] == 'flat'], x='price', kde=True, label='Flat',color = '#1DD3B0' , stat='density', element='step')
plt.legend()
st.pyplot(fig)
