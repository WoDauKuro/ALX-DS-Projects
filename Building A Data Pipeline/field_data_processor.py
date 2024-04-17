import logging
import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV

"""
Module for processing field-related data.

This module contains a class, `FieldDataProcessor`, which provides functionalities for processing field-related data. 
It includes methods for ingesting data from a SQL database, renaming columns, applying corrections, and mapping weather 
station data.
"""

class FieldDataProcessor:
    """
    A class to process field-related data.

    Attributes:
        db_path (str): The path to the database.
        sql_query (str): The SQL query to retrieve data from the database.
        columns_to_rename (dict): A dictionary of columns to rename.
        values_to_rename (dict): A dictionary of values to rename in a specific column.
        weather_map_data (str): The URL to the weather mapping CSV file.
    """

    def __init__(self, config_params, logging_level="INFO"):
        """
        Initializes the FieldDataProcessor class.

        Args:
            config_params (dict): A dictionary containing configuration parameters.
            logging_level (str, optional): The logging level. Defaults to "INFO".
        """
        self.db_path = config_params['db_path']
        self.sql_query = config_params['sql_query']
        self.columns_to_rename = config_params['columns_to_rename']
        self.values_to_rename = config_params['values_to_rename']
        self.weather_map_data = config_params['weather_mapping_csv']  
        self.weather_csv_path = config_params['weather_csv_path']   
        # Add the rest of your class code here
        
        self.initialize_logging(logging_level)

        # We create empty objects to store the DataFrame and engine in
        self.df = None
        self.engine = None
        
    def initialize_logging(self, logging_level):
        """
        Initializes logging for the class.

        Args:
            logging_level (str): The logging level.
        """
        logger_name = __name__ + ".FieldDataProcessor"
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

        # Use self.logger.info(), self.logger.debug(), etc.


    def ingest_sql_data(self):
        """
        Ingests data from a SQL database using the provided SQL query.
        """
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)    
        self.logger.info("Sucessfully loaded data.")
        return self.df
    
    def rename_columns(self):
        """
        Renames columns in the DataFrame according to the provided dictionary.
        """
        column1, column2 = list(self.columns_to_rename.keys())[0], list(self.columns_to_rename.values())[0]

        # Temporarily rename one of the columns to avoid a naming conflict
        temp_name = "__temp_name_for_swap__"
        while temp_name in self.df.columns:
            temp_name += "_"

        # Perform the swap
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})

        self.logger.info(f"Swapped columns: {column1} with {column2}")
    
    def apply_corrections(self, column_name='Crop_type', abs_column='Elevation'):
        """
        Applies corrections to the DataFrame, such as absolute values and value replacements.
        """
        self.df[abs_column] = self.df[abs_column].abs()
        self.df[column_name] = self.df[column_name].apply(lambda crop: self.values_to_rename.get(crop, crop))
    
    def weather_station_mapping(self):
        """
        Maps weather station data to the DataFrame based on a provided CSV file.
        """
        weather_station_df = read_from_web_CSV(self.weather_map_data)

        # Merge the two DataFrames using 'Field_ID'
        self.df = pd.merge(self.df, weather_station_df[['Field_ID', 'Weather_station']], on='Field_ID', how='left')

        # Return the 'self.df' DataFrame containing the 'Weather_station' column
        return read_from_web_CSV(self.weather_map_data)
    
    def process(self):
        """
        Processes the field-related data by ingesting SQL data, renaming columns, applying corrections, and mapping weather station data.
        """
        self.ingest_sql_data()
        self.rename_columns()
        self.apply_corrections()
        self.weather_station_mapping()
        return self.df