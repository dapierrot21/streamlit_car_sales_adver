import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt


# Reading in csv file.
car_sales_df = pd.read_csv("vehicles_us.csv").dropna()

st.header("Distribution of Car Age")

# Display checkbox to toggle the plot
show_car_age_plot = st.checkbox("Show Distribution of Car Age")

# Plot distribution of car_age using Streamlit
if show_car_age_plot:
    st.plotly_chart(
        px.histogram(
            car_sales_df,
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
            car_sales_df,
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

# Display checkbox to toggle the plot
show_odometer_by_type_plot = st.checkbox("Show Scatter Plot of Odometer by Car Type")

# Plot scatter plot of odometer by car type using Streamlit
if show_odometer_by_type_plot:
    st.plotly_chart(
        px.scatter(
            car_sales_df,
            x="odometer",
            y="type",
            title="Scatter Plot of Odometer Values by Car Type",
            height=600,
            opacity=0.5,
        ).update_layout(xaxis_title="Odometer", yaxis_title="Car Type"),
        use_container_width=True,
    )


st.header("Scatter Plot of Odometer Values by Car Type")

# Relationship with car type vs odometer values
scatter_data = car_sales_df[
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
    alt.Chart(car_sales_df)
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
