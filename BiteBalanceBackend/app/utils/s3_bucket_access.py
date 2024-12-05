from loguru import logger
from datetime import datetime

import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException
from botocore.exceptions import ClientError

# Refactor this to a class and create object for each needing routes

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the bucket name, object key (path), and local file path
BUCKET_NAME = 'bitebalances3bucket'


def process_upload_time()->str:
    # Smelly code, needs refactoring
    today = datetime.today()
    current_time = f"{today.year}-{today.month}-{today.day}-{today.hour}-{today.minute}-{today.second}"
    return current_time


async def upload_meal(meal, filename) -> str:
    
    uppload_time = process_upload_time()
    # Define the S3 object key (path) where the file will be saved
    object_key = f"uploads/{uppload_time}/{filename}"
    # Read the file contents and upload to S3
    
    try: 
        s3_client.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=meal)

        return object_key
    
    except ClientError as e:
        # Handle S3 errors (like permission issues)
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    except Exception as e:
        # Handle general errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    


async def pre_signed_image_url(image_key: str):
    try:
        # Generate a pre-signed URL for the image
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': image_key},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return str(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")