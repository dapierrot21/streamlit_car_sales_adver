# Car Sales Advertisement Analysis

## Overview

This project is a data analysis tool for exploring a car sales advertisement dataset. The goal is to perform exploratory data analysis (EDA) and generate visualizations to gain insights into the dataset.

## Description

The project utilizes the Streamlit framework in Python to create an interactive web application. Users can explore various aspects of the car sales dataset, including the distribution of car age, price, and relationships between different features.

## Features

- Distribution of Car Age by Car Type
- Distribution of Car Prices
- Price vs. Odometer Relationship
- Scatter Plot of Odometer Values by Car Type
- Type vs. Days Listed Relationship
- Top 20 Shortest Listed vs. Top 20 Longest Listed
- The Average Car Posted Each Month

## Libraries Used

- Streamlit
- Pandas
- Plotly Express
- Altair

## How to Run Locally

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/dapierrot21/streamlit_car_sales_adver.git
   cd streamlit_car_sales_adver

   ```

2. Create a Virtual Environment

   ```bash
   python -m venv venv

   ```

3. Activate the Virtual Environment

   Windows:

   ```bash
   venv\Scripts\activate

   ```

   On manOS/Linux:

   ```bash
   source venv/bin/activate

   ```

4. Install Dependencies:

   ```bash
   pip install -r requirements.txt

   ```

5. Run the Streamlit App
   ```bash
   streamlit run app.py
   ```

Open your web browser and go to https://car-sale-web-app.onrender.com to view the Streamlit app.

## Project Structure

- app.py: Main Streamlit application file.
- requirements.txt: List of Python dependencies for the project.
- notebooks/: juypter notebook
- vehicles_us.csv: dataset
- .streamlit/: Streamlit config file
