import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")


def save_data(df_price_coordinates):
    # Convert dataframe to PyArrow Table
    table = pa.Table.from_pandas(df_price_coordinates)

    # Convert the table to bytes
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)
    data = buffer.getvalue().to_pybytes()

    # Connect to S3 using the credentials
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION)

    bucket_name = 'prices-naya-project'
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    source = 'main'
    file_path = f"{today}/{source}/shufersal_prices.parquet"

    # Upload the bytes to S3
    s3.put_object(Bucket=bucket_name, Key=file_path, Body=data)
