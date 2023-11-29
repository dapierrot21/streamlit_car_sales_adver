import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import datetime


# Reading in csv file.
car_sales_df = pd.read_csv("vehicles_us.csv").dropna()

# EDA
car_sales_df["model_year"] = car_sales_df["model_year"].astype(
    "Int64"
)  # Convert to nullable integer
car_sales_df["cylinders"] = car_sales_df["cylinders"].astype(
    "Int64"
)  # Convert to nullable integer
car_sales_df["odometer"] = car_sales_df["odometer"].astype(
    "Int64"
)  # Convert to nullable integer
car_sales_df["date_posted"] = pd.to_datetime(car_sales_df["date_posted"])

new_car_sales_df = car_sales_df.dropna(
    subset=["model_year", "cylinders", "odometer", "paint_color", "is_4wd"]
).copy()

# Feature Engineering: Age of car
current_year = datetime.datetime.now().year
new_car_sales_df["car_age"] = current_year - new_car_sales_df["model_year"]

# Display the first few rows to confirm the changes
new_car_sales_df[["model_year", "car_age"]].head(10)

st.header("Distribution of Car Age")

# Display checkbox to toggle the plot
show_car_age_plot = st.checkbox("Show Distribution of Car Age")

# Plot distribution of car_age using Streamlit
if show_car_age_plot:
    st.plotly_chart(
        px.histogram(
            new_car_sales_df,
            x="car_age",
            nbins=20,
            title="Distribution of Car Age",
        ).update_layout(
            xaxis_title="Car Age (Years)",
            yaxis_title="Frequency",
            width=600,
            height=400,
        ),
        use_container_width=True,
    )


st.header("Price Distribution")

# Display checkbox to toggle the plot
show_car_price_plot = st.checkbox("Show Distribution of Car Prices")

# Plot distribution of car prices using Streamlit
if show_car_price_plot:
    st.plotly_chart(
        px.histogram(
            new_car_sales_df,
            x="price",
            title="Distribution of Car Prices",
            nbins=50,
        ).update_layout(
            xaxis_title="Car Price",
            yaxis_title="Frequency",
            width=600,
            height=400,
        ),
        use_container_width=True,
    )

st.header("Price vs. Odometer Relationship")

# Enable Altair data transformer
alt.data_transformers.enable("default", max_rows=None)

# Checkbox to select car types
selected_car_types = st.multiselect(
    "Select Car Types",
    new_car_sales_df["type"].unique(),
    default=new_car_sales_df["type"].unique(),
)

# Filter data based on selected car types
filtered_data = new_car_sales_df[new_car_sales_df["type"].isin(selected_car_types)]

# Price vs. Odometer Relationship
scatterplot = (
    alt.Chart(filtered_data)
    .mark_circle()
    .encode(
        x="odometer:Q",
        y="price:Q",
        tooltip=["odometer:Q", "price:Q", "model:N", "condition:N"],
    )
    .properties(title="Price vs. Odometer Relationship", width=600, height=400)
)

# Display the scatter plot
st.altair_chart(scatterplot, use_container_width=True)


st.header("Scatter Plot of Odometer Values by Car Type")

# Relationship with car type vs odometer values
scatter_data = new_car_sales_df[
    ["type", "odometer"]
].dropna()  # Remove rows with missing values

# Create a scatter plot using Streamlit
st.plotly_chart(
    px.scatter(
        scatter_data,
        x="odometer",
        y="type",
        title="Scatter Plot of Odometer Values by Car Type",
        height=600,
        opacity=0.5,
    ).update_layout(xaxis_title="Odometer", yaxis_title="Car Type"),
    use_container_width=True,
)

st.header("Type vs. Days Listed Relationship")
# Enable Altair data transformer
alt.data_transformers.enable("default", max_rows=None)

# Type vs. Days Listed Relationship
scatterplot = (
    alt.Chart(new_car_sales_df)
    .mark_circle()
    .encode(
        x="type",
        y="days_listed",
        tooltip=["model", "days_listed", "model_year", "condition", "price"],
    )
    .properties(title="Type vs. Days Listed Relationship", width=800, height=400)
)

# Display the Altair chart in Streamlit
st.altair_chart(scatterplot.interactive(), use_container_width=True)
