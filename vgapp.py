import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_excel('vgsales.xlsx', engine='openpyxl')

# Clean data
df = df.dropna(subset=['Year', 'Global_Sales'])
df['Year'] = df['Year'].astype(int)

# App title
st.title("🎮 Video Game Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
years = sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + years)
selected_genres = st.sidebar.multiselect("Select Genre", options=df['Genre'].unique())
selected_platforms = st.sidebar.multiselect("Select Platform", options=df['Platform'].unique())

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
if selected_platforms:
    filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platforms)]

# Top 10 Games by Global Sales
st.subheader("Top 10 Games by Global Sales")
top_games = filtered_df.sort_values(by='Global_Sales', ascending=False).head(10)
fig1 = px.bar(top_games, x='Name', y='Global_Sales', color='Platform', title='Top 10 Games')
st.plotly_chart(fig1)

# Sales by Genre
st.subheader("Sales by Genre")
genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum().reset_index()
fig2 = px.pie(genre_sales, names='Genre', values='Global_Sales', title='Sales Distribution by Genre')
st.plotly_chart(fig2)

# Platform Trends Over Time
st.subheader("Platform Trends Over Time")
platform_trends = df.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
fig3 = px.line(platform_trends, x='Year', y='Global_Sales', color='Platform', title='Platform Sales Over Time')
st.plotly_chart(fig3)

# Regional Sales Comparison
st.subheader("Regional Sales Comparison")
regional_sales = filtered_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
regional_sales.columns = ['Region', 'Sales']
fig4 = px.bar(regional_sales, x='Region', y='Sales', title='Regional Sales Comparison')
st.plotly_chart(fig4)


# 5. Bubble Chart: Global Sales vs Year by Genre
st.subheader("Bubble Chart: Global Sales vs Year by Genre")
fig5 = px.scatter(filtered_df, x='Year', y='Global_Sales', size='Global_Sales', color='Genre',
                  hover_name='Name', title='Bubble Chart: Global Sales vs Year')
st.plotly_chart(fig5)

# 6. Scatter Plot: NA Sales vs EU Sales by Genre
st.subheader("Scatter Plot: NA Sales vs EU Sales by Genre")
fig6 = px.scatter(filtered_df, x='NA_Sales', y='EU_Sales', color='Genre', hover_name='Name',
                  size='Global_Sales', title='Scatter Plot: NA vs EU Sales')
st.plotly_chart(fig6)


# 7. Histogram: Distribution of Global Sales
st.subheader("Histogram: Distribution of Global Sales")
fig7 = px.histogram(filtered_df, x='Global_Sales', nbins=30, title='Distribution of Global Sales')
st.plotly_chart(fig7)

# 9. Heatmap: Correlation between Regional Sales
st.subheader("Heatmap: Correlation between Regional Sales")
corr = filtered_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].corr()
fig8 = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
st.plotly_chart(fig8)



# Footer
st.markdown("---")

