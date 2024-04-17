import re
import numpy as np
import pandas as pd
from field_data_processor import FieldDataProcessor
from weather_data_processor import WeatherDataProcessor
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config_params = {
    "sql_query": """
        SELECT *
        FROM geographic_features
        LEFT JOIN weather_features USING (Field_ID)
        LEFT JOIN soil_and_crop_features USING (Field_ID)
        LEFT JOIN farm_management_features USING (Field_ID)
    """,
    "db_path": 'sqlite:///Maji_Ndogo_farm_survey_small.db',
    "columns_to_rename": {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},  
    "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea', 'tea ': 'tea', 'wheat ': 'wheat', 'cassava ': 'cassava'},
    "weather_mapping_csv": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
    "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
    "regex_patterns": {
        'Rainfall': r'(\d+(\.\d+)?)\s?mm',
        'Temperature': r'(\d+(\.\d+)?)\s?C',
        'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
    }
}

field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df

weather_processor = WeatherDataProcessor(config_params)
weather_processor.process()
weather_df = weather_processor.weather_df


# Function to read weather DataFrame and check its shape
def test_read_weather_DataFrame_shape():
    weather_df = weather_processor.weather_df
    assert weather_df.shape == (1843, 4), "Weather DataFrame shape is incorrect"

# Function to read field DataFrame and check its shape
def test_read_field_DataFrame_shape():
    field_df = field_processor.df
    assert field_df.shape == (5654, 19), "Field DataFrame shape is incorrect"

# Function to check weather DataFrame columns
def test_weather_DataFrame_columns():
    weather_df = pd.read_csv('sampled_weather_df.csv')
    expected_columns = ['Measurement', 'Value']
    assert all(col in weather_df.columns for col in expected_columns), "Weather DataFrame columns are incorrect"

# Function to check field DataFrame columns
def test_field_DataFrame_columns():
    field_df = pd.read_csv('sampled_field_df.csv')
    expected_columns = ['Field_ID', 'Crop_type', 'Elevation']
    assert all(col in field_df.columns for col in expected_columns), "Field DataFrame columns are incorrect"

# Function to check if elevation values in field DataFrame are non-negative
def test_field_DataFrame_non_negative_elevation():
    field_df = pd.read_csv('sampled_field_df.csv')
    assert (field_df['Elevation'] >= 0).all(), "Some elevation values in Field DataFrame are negative"

# Function to check if crop types in field DataFrame are valid
def test_crop_types_are_valid():
    field_df = field_processor.df
    valid_crop_types = ['cassava', 'wheat', 'tea', 'banana', 'potato', 'rice', 'coffee', 'maize']  # Define valid crop types
    assert field_df['Crop_type'].isin(valid_crop_types).all(), "Some crop types in Field DataFrame are invalid"

# Function to check if rainfall values in weather DataFrame are positive
def test_positive_rainfall_values():
    weather_df = weather_processor.weather_df
    # Filter the DataFrame to include only rows where the 'Measurement' column is 'Rainfall'
    rainfall_df = weather_df[weather_df['Measurement'] == 'Rainfall']
    # Check if all values in the 'Value' column (related to 'Rainfall' only) of the DataFrame are greater than 0
    assert (rainfall_df['Value'] > 0).all(), "Some rainfall values in Weather DataFrame are negative"