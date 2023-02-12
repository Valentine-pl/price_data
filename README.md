# Data Pipeline for Fetching, Processing, Adding Geospatial Data and Saving to S3 Bucket

This repository contains code for a data pipeline that fetches data from a website, processes it, adds geospatial data to it, and then saves it to an S3 bucket. 

## Code Description

The `fetch_data` function in `fetch_data.py` uses the `requests` library to fetch data from a website and the `BeautifulSoup` library to parse the HTML. It then extracts data from the website and stores it in a pandas data frame.

The `process_data` function in `process_data.py` takes the data frame created in `fetch_data` and processes it to keep only the relevant columns.

The `add_coordinates` function in `add_coordinates.py` adds latitude and longitude coordinates to the data frame by using the `geopy` library and the `get_coordinates` function from `get_coordinates.py`.

The, the `save_data` function in `save_data.py` saves the processed data frame to an S3 bucket using the `boto3` library and the `pyarrow` library to convert the data frame to a Parquet format.

Finally `main` function in `main.py` ties everything together and runs the pipeline by calling the functions in the correct order.
