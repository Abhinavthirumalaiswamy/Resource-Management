import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Configuration & Data Setup
st.set_page_config(layout="wide", page_title="Resource Dashboard 2026")

data = {
    'Tamil Nadu': [1886, 4379, 1422, 7808, 2849],
    'Kerala': [4231, 740, 1154, 2379, 1846],
    'Karnataka': [8076, 3420, 1537, 13321, 2512],
    'Maharastra': [16441, 3737, 2094, 9639, 2262],
    'Gujarat': [1396, 1546, 431, 3193, 300]
}

state_coords = {
    'Tamil Nadu': [11.1271, 78.6569],
    'Kerala': [10.8505, 76.2711],
    'Karnataka': [15.3173, 75.7139],
    'Maharastra': [19.7515, 75.7139],
    'Gujarat': [22.2587, 71.1924]
}

labels = ['furniture', 'dairy products', 'bakery products', 'wooden containers', 'cement']
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0']

st.title("Resource Management Dashboard (2026)")

# 2. State & Chart Selection
state_choice = st.selectbox("Select a State", list(data.keys()))
values = data[state_choice]
chart_choice = st.radio("Select Chart Type", ["Bar Chart", "Pie Chart", "Donut Chart", "Show All"], horizontal=True)

# 3. Chart Logic Functions
def plot_bar():
    st.subheader(f"Bar Chart: {state_choice}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(labels, values, color=colors)
    ax.set_ylabel('Workers Count')
    st.pyplot(fig)

def plot_pie(is_donut=False):
    title = "Donut" if is_donut else "Pie"
    st.subheader(f"{title} Chart: {state_choice}")
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', 
           wedgeprops={'width': 0.5} if is_donut else None, startangle=140)
    st.pyplot(fig)

# 4. Display Logic
if chart_choice == "Bar Chart":
    plot_bar()
elif chart_choice == "Pie Chart":
    plot_pie(is_donut=False)
elif chart_choice == "Donut Chart":
    plot_pie(is_donut=True)
else: # Show All
    plot_bar()
    col1, col2 = st.columns(2)
    with col1: plot_pie(is_donut=False)
    with col2: plot_pie(is_donut=True)

# 5. Map & Heatmap Data Processing
st.divider()
map_data_list = []
for state, counts in data.items():
    lat, lon = state_coords[state]
    for i, product in enumerate(labels):
        map_data_list.append({
            'State': state, 'Product': product, 
            'Workers': counts[i], 'lat': lat, 'lon': lon
        })
df_final = pd.DataFrame(map_data_list)

# 6. Map Visualizations (Plotly 2026 Standard)
tab1, tab2 = st.tabs(["Distribution Map", "Intensity Heatmap"])

with tab1:
    st.subheader("Geospatial Worker Distribution")
    fig_map = px.scatter_map(
        df_final, lat="lat", lon="lon", size="Workers", color="Product",
        hover_name="State", zoom=3, map_style="open-street-map", height=600
    )
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.subheader("Resource Intensity Heatmap")
    fig_heat = px.density_map(
        df_final, lat="lat", lon="lon", z="Workers", radius=40,
        center=dict(lat=20, lon=78), zoom=3,
        map_style="open-street-map", color_continuous_scale="Viridis", height=600
    )
    st.plotly_chart(fig_heat, use_container_width=True)