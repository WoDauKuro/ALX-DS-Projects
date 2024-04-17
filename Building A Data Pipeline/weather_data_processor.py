import re
import numpy as np
import pandas as pd
import logging
from data_ingestion import read_from_web_CSV

"""
Module for processing weather-related data.

This module contains a class, `WeatherDataProcessor`, which provides functionalities for processing weather-related data. 
It includes methods for mapping weather station data from a CSV file, extracting measurements from messages using regular expressions, 
processing messages to extract measurements, and calculating mean values of measurements grouped by weather station and measurement type.
"""

class WeatherDataProcessor:
    """
    A class to process weather-related data.

    Attributes:
        weather_station_data (str): The URL to the weather station data CSV file.
        patterns (dict): A dictionary containing regex patterns for message extraction.
        weather_df (DataFrame): DataFrame to store weather data.
    """

    def __init__(self, config_params, logging_level="INFO"):
        """
        Initializes the WeatherDataProcessor class.

        Args:
            config_params (dict): A dictionary containing configuration parameters.
            logging_level (str, optional): The logging level. Defaults to "INFO".
        """
        self.weather_station_data = config_params['weather_csv_path']
        self.patterns = config_params['regex_patterns']
        self.weather_df = None  # Initialize weather_df as None or as an empty DataFrame
        self.initialize_logging(logging_level)

    def initialize_logging(self, logging_level):
        """
        Initializes logging for the class.

        Args:
            logging_level (str): The logging level.
        """
        logger_name = __name__ + ".WeatherDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False  # Prevents log messages from being propagated to the root logger

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def weather_station_mapping(self):
        """
        Maps weather station data from a CSV file.
        """
        self.weather_df = read_from_web_CSV(self.weather_station_data)
        self.logger.info("Successfully loaded weather station data from the web.") 
        # Here, you can apply any initial transformations to self.weather_df if necessary.

    def extract_measurement(self, message):
        """
        Extracts measurement data from a message using regex patterns.

        Args:
            message (str): The message containing measurement data.

        Returns:
            tuple: A tuple containing the measurement type and value.
        """
        for key, pattern in self.patterns.items():
            match = re.search(pattern, message)
            if match:
                self.logger.debug(f"Measurement extracted: {key}")
                return key, float(next((x for x in match.groups() if x is not None)))
        self.logger.debug("No measurement match found.")
        return None, None

    def process_messages(self):
        """
        Processes messages to extract measurements.
        """
        if self.weather_df is not None:
            result = self.weather_df['Message'].apply(self.extract_measurement)
            self.weather_df['Measurement'], self.weather_df['Value'] = zip(*result)
            self.logger.info("Messages processed and measurements extracted.")
        else:
            self.logger.warning("weather_df is not initialized, skipping message processing.")
        return self.weather_df

    def calculate_means(self):
        """
        Calculates the mean values of measurements grouped by weather station and measurement type.
        """
        if self.weather_df is not None:
            means = self.weather_df.groupby(by=['Weather_station_ID', 'Measurement'])['Value'].mean()
            self.logger.info("Mean values calculated.")
            return means.unstack()
        else:
            self.logger.warning("weather_df is not initialized, cannot calculate means.")
            return None
    
    def process(self):
        """
        Processes weather-related data by mapping weather station data, processing messages, and calculating means.
        """
        self.weather_station_mapping()  # Load and assign data to weather_df
        self.process_messages()  # Process messages to extract measurements
        self.logger.info("Data processing completed.")