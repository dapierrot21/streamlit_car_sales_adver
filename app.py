import datetime
import pandas as pd
import plotly.express as px
import altair as alt
from scipy.stats import pearsonr
import streamlit as st


# Reading in csv file.
car_sales_df = pd.read_csv("vehicles_us.csv").dropna()


# EDA
# Check for duplicates in the dataframe
duplicate_rows = car_sales_df.duplicated()

# Display a warning if duplicates are found
if duplicate_rows.any():
    print("Warning: Duplicate rows found in the dataset.")
    print("Number of duplicate rows:", duplicate_rows.sum())
else:
    print("No duplicates found.")


# Fill missing values using groupby with a custom function
def fill_missing_median(group):
    """
    Fill missing values in a pandas DataFrame group with the median of non-null values.

    Parameters:
    - group (pandas.DataFrame): A pandas DataFrame group.

    Returns:
    - pandas.DataFrame: A DataFrame with missing values filled using the median of non-null values.
    """
    non_null_values = group.dropna()
    if non_null_values.empty:
        return group
    else:
        median_value = non_null_values.median()
        return group.fillna(median_value)


car_sales_df["cylinders"] = car_sales_df.groupby(["model", "model_year"])[
    "cylinders"
].transform(fill_missing_median)


# Convert data types
car_sales_df["model_year"] = car_sales_df["model_year"].astype(
    "Int64"
)  # Convert to nullable integer
car_sales_df["odometer"] = car_sales_df["odometer"].astype(
    "Int64"
)  # Convert to nullable integer
car_sales_df["date_posted"] = pd.to_datetime(car_sales_df["date_posted"])


# Replace NaN values in 'is_4wd' column with 0
car_sales_df["is_4wd"].fillna(0, inplace=True)

# Convert the column to integers so '1.0' can to become '1' (integer)
car_sales_df["is_4wd"] = car_sales_df["is_4wd"].astype(int)

# Feature Engineering: Age of car
current_year = datetime.datetime.now().year
car_sales_df["car_age"] = current_year - car_sales_df["model_year"]


# Car Age by type

average_car_age_by_type = car_sales_df.groupby("type")["car_age"].mean().reset_index()


st.header("Distribution of Car Age By Type")


# Plot distribution of car_age by type using Streamlit
fig = px.bar(
    average_car_age_by_type, x="type", y="car_age", title="Average Car Age by Type"
)
fig.update_layout(xaxis_title="Car Type", yaxis_title="Average Age (Years)")

# Add the observation to the Streamlit app
observation = """
**Car Age Distribution:** The bar chart of car ages by type revealed that most cars in the dataset 
fall within a certain age range, with the majority being around 10 to 15 years old.
"""

st.write(observation)

# Use st.plotly_chart to display the Plotly chart in Streamlit
st.plotly_chart(fig)


# Price Distribution

car_sales_df["price_length"] = car_sales_df["price"].astype(str).str.len()

# Filter rows where the length of 'price' is greater than 1
valid_price_data = car_sales_df[car_sales_df["price_length"] > 1]

# Calculate average price for each car type
average_price_by_type = valid_price_data.groupby("type")["price"].mean().reset_index()

st.header("Price Distribution")

fig = px.bar(
    average_price_by_type,
    x="type",
    y="price",
    title="Average Price by Car Type",
    labels={"price": "Average Price", "type": "Car Type"},
)

# Add the observation to the Streamlit app
observation = """
**Average Price by Car Type:** The average prices provide insights into the varying cost structures associated with different car types. Buyers can consider these averages when making decisions based on their budget and preferences.

1. **SUV**: $11,381.50
   - SUVs have an average price of $11,381, making them a relatively affordable choice.
   
2. **Bus**: $17,135.67
   - Buses have a higher average price of $17,135, suggesting they may be more expensive due to their specific functionalities.

3. **Convertible**: $14,944.44
   - Convertibles have an average price of $14,944, reflecting the added cost associated with the convertible feature.

4. **Coupe**: $14,829.93
   - Coupes show a similar average price to convertibles, indicating that the body style may contribute to pricing.

5. **Hatchback**: $6,928.06
   - Hatchbacks have a notably lower average price of $6,928, making them a budget-friendly option.

6. **Mini-van**: $8,207.31
   - Mini-vans have an average price of $8,207, aligning with their family-oriented and practical design.

7. **Offroad**: $14,292.29
   - Offroad vehicles have an average price of $14,292, possibly reflecting the cost of specialized offroad features.

8. **Other**: $11,032.81
   - The 'Other' category has an average price of $11,033, encompassing various types with moderate pricing.

9. **Pickup**: $16,075.81
   - Pickups have a relatively high average price of $16,076, likely due to their versatility and capabilities.

10. **Sedan**: $7,047.10
    - Sedans have a lower average price of $7,047, making them an economical choice for many buyers.

11. **Truck**: $17,132.92
    - Trucks have a higher average price of $17,133, suggesting that their robustness and capabilities contribute to pricing.

12. **Van**: $10,820.42
    - Vans have an average price of $10,820, indicating a moderate price range.

13. **Wagon**: $9,088.13
    - Wagons have an average price of $9,088, falling within a reasonable price range.
"""

st.write(observation)


# Display the plot using st.plotly_chart
st.plotly_chart(fig)


# Price vs. Odometer

st.header("Price vs. Odometer Relationship")

# Enable Altair data transformer
alt.data_transformers.enable("default", max_rows=None)

# Checkbox to select car types
selected_car_types = st.multiselect(
    "Select Car Types",
    car_sales_df["type"].unique(),
    default=car_sales_df["type"].unique(),
)

# Filter data based on selected car types
filtered_data = car_sales_df[car_sales_df["type"].isin(selected_car_types)]

# Price vs. Odometer Relationship
scatterplot = (
    alt.Chart(filtered_data)
    .mark_circle()
    .encode(
        x="odometer:Q",
        y="price:Q",
        tooltip=["odometer:Q", "price:Q", "model:N", "condition:N", "type:N"],
    )
    .properties(title="Price vs. Odometer Relationship", width=600, height=400)
)

# Display the scatter plot
st.altair_chart(scatterplot, use_container_width=True)

# Drop rows with missing values in 'odometer'
selected_df = car_sales_df.dropna(subset=["odometer"])

# Extract 'price' and 'odometer' columns
price = selected_df["price"]
odometer = selected_df["odometer"]

# Calculate the correlation and p-value
correlation, p_value = pearsonr(price, odometer)

# Display the results in Streamlit
st.write(f"Correlation between price and odometer: {correlation}")
st.write(f"P-value: {p_value}")


# Add the observation to the Streamlit app
observation = """
**Price vs. Odometer**
The correlation coefficient between price and odometer is approximately -0.42. A negative correlation suggests that as one variable (odometer) increases, the other variable (price) tends to decrease. This indicates that vehicles with higher mileage (odometer reading) generally have lower prices.

The p-value being 0.0 indicates that the correlation is statistically significant, meaning it's unlikely to have occurred by random chance.
"""

st.write(observation)

# Top 20 shortest listed vs. top 20 longest listed
st.header("Top 20 Shortest Listed vs. Top 20 Longest Listed")
car_sales_df["price_length"] = car_sales_df["price"].astype(str).str.len()

# Filter rows where the length of 'price' is greater than 1
valid_data = car_sales_df[car_sales_df["price_length"] > 1]

# Assuming 'days_listed' is the column representing the number of days a car was listed
top_20_shortest_listed = valid_data.nsmallest(20, "days_listed")


# Display the resulting DataFrame
st.write("Top 20 Shortest Listed Cars:")
st.write(
    top_20_shortest_listed[
        [
            "model",
            "days_listed",
            "price",
            "type",
            "condition",
            "date_posted",
            "odometer",
        ]
    ]
)

# Assuming 'days_listed' is the column representing the number of days a car was listed
top_20_longest_listed = valid_data.nlargest(20, "days_listed")

# Display the resulting DataFrame
st.write("Top 20 Longest Listed Cars:")
st.write(
    top_20_longest_listed[
        [
            "model",
            "days_listed",
            "price",
            "type",
            "condition",
            "date_posted",
            "odometer",
        ]
    ]
)

# Concatenate the top and bottom 20 listed cars
top_and_bottom_cars = pd.concat([top_20_shortest_listed, top_20_longest_listed])

# Convert categorical columns to numerical using one-hot encoding
top_and_bottom_cars_encoded = pd.get_dummies(
    top_and_bottom_cars, columns=["condition", "type"]
)

# Calculate the correlation matrix
correlation_matrix = top_and_bottom_cars_encoded[["price", "days_listed"]].corr()

# Display the correlation matrix
st.write("Correlation Matrix:")
st.write(correlation_matrix)

# Add the observation to the Streamlit app
observation = """
**Top 20 Shortest Listed vs. Top 20 Longest Listed Conclusion**<br>
- The correlation coefficient is approximately -0.024, indicating a very weak negative correlation between the price of a car and the number of days it is listed. In other words, there's a minimal tendency for lower-priced cars to have slightly longer listing durations and higher-priced cars to have slightly shorter listing durations.
"""

st.write(observation)

# Relationship with car type vs odometer values

st.header("Scatter Plot of Odometer Values by Car Type")

type_vs_odometer_df = (
    car_sales_df.dropna(subset=["odometer"])
    .groupby("type")["odometer"]
    .mean()
    .reset_index()
)

# Relationship with car type vs odometer values
fig = px.scatter(
    type_vs_odometer_df,
    x="type",
    y="odometer",
    title="Average Odometer Reading by Car Type",
    labels={"odometer": "Average Odometer Reading", "type": "Car Type"},
    template="plotly_white",
)

# Update the layout for better readability
fig.update_layout(showlegend=False, xaxis={"categoryorder": "total descending"})

# Show the plot using st.plotly_chart
st.plotly_chart(fig)

# Add the observation to the Streamlit app
observation = """
**Conclusion**
- **SUV:** The average odometer reading is relatively high, indicating that SUVs may have covered a significant distance on average.

- **Bus:** Buses also have a high average odometer reading, suggesting that they might be used for longer trips or have been on the road for an extended period.

- **Convertible:** Convertibles show a lower average odometer reading compared to SUVs and buses, indicating potentially less usage or shorter trips.

- **Coupe:** Coupes have a moderate average odometer reading, falling between convertibles and hatchbacks.

- **Hatchback:** Hatchbacks have a relatively high average odometer reading, similar to SUVs, indicating that they might be commonly used for various purposes.

- **Mini-van:** Mini-vans have the highest average odometer reading among all car types, suggesting they are frequently used for family activities or longer journeys.

- **Offroad:** Offroad vehicles have a high average odometer reading, indicating that they might have been used for adventurous activities.

- **Other:** The 'Other' category has a moderate average odometer reading, encompassing various types with varied usage patterns.

- **Pickup:** Pickups show a high average odometer reading, similar to SUVs and trucks, suggesting versatility in usage.

- **Sedan:** Sedans have a moderate average odometer reading, falling between coupes and hatchbacks.

- **Truck:** Trucks have a high average odometer reading, indicating that they might be used for heavy-duty purposes.

- **Van:** Vans have a high average odometer reading, similar to SUVs and trucks, suggesting potential commercial or heavy usage.

- **Wagon:** Wagons have a high average odometer reading, similar to SUVs and trucks, indicating versatile usage.
"""

st.write(observation)

# Type vs Days Listed

type_vs_days_listed_df = car_sales_df.groupby("type")["days_listed"].sum().reset_index()


st.header("Type vs. Days Listed Relationship")
# Relationship with car type vs days listed values
fig = px.scatter(
    type_vs_days_listed_df,
    x="type",
    y="days_listed",
    title="Days Listed by Car Type",
    labels={"days_listed": "Days Listed", "type": "Car Type"},
    template="plotly_white",
)

# Update the layout for better readability
fig.update_layout(showlegend=False, xaxis={"categoryorder": "total descending"})

# Show the plot using st.plotly_chart
st.plotly_chart(fig)

# Add the observation to the Streamlit app
observation = """
**Conclusion**
- Understanding the average days listed for each car type can be useful for sellers and buyers alike. Sellers can adjust their expectations based on the typical duration, while buyers may gauge the availability and demand for specific car types in the market.
    - **SUV, Pickup, Truck:** SUVs, pickups, and trucks have the highest number of days listed. This may suggest that these types of vehicles, often used for various purposes, take longer to find buyers.

    - **Bus, Convertible, Offroad:** Buses, convertibles, and offroad vehicles have relatively lower days listed. Buses may have a niche market, while convertibles and offroad vehicles might attract more specific buyers.

    - **Sedan, Wagon, Hatchback:** Sedans, wagons, and hatchbacks show moderate days listed. These car types are commonly used for daily commuting, potentially leading to a balanced demand and supply.

    - **Coupe:** Coupes have a significant number of days listed, indicating that they might take longer to find buyers compared to other car types.

    - **Van:** Vans have a moderate number of days listed, suggesting a balanced market for this type.

    - **Other:** The 'Other' category has a relatively short duration, indicating that less common car types may find buyers more quickly.
"""

st.write(observation)

# The Average Car posted by month

st.header("The Average Car Posted By Month")

car_sales_df["month_posted"] = car_sales_df["date_posted"].dt.month_name()

# Group by month and type, count the number of postings
monthly_posting_counts = (
    car_sales_df.groupby(["month_posted", "type"]).size().reset_index(name="count")
)

# Find the car type posted the most in each month
most_posted_by_month = monthly_posting_counts.loc[
    monthly_posting_counts.groupby("month_posted")["count"].idxmax()
]

# Create a list of unique car types for the selectbox
car_types = most_posted_by_month["type"].unique().tolist()

# Allow the user to select a car type
selected_car_type = st.selectbox("Select a Car Type", car_types)

# Filter the DataFrame based on the selected car type
filtered_data = most_posted_by_month[most_posted_by_month["type"] == selected_car_type]

# Plot the distribution
fig = px.bar(
    filtered_data,
    x="month_posted",
    y="count",
    color="type",
    labels={"count": "Number of Postings"},
    title=f"Monthly Postings for {selected_car_type}",
)

# Show the plot using st.plotly_chart
st.plotly_chart(fig)


# Add the observation to the Streamlit app
observation = """
**Observations**<br>
- **SUV Dominance:** SUVs appear to be the most posted car type in several months, including April, December, March, May, and November.

- **Truck Dominance:** Trucks dominate in months like August, February, July, and June.

- **Sedan Peaks:** Sedans have a significant presence in months like January, October, and September.
"""

st.write(observation)
