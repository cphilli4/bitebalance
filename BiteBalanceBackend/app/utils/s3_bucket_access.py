from loguru import logger
from datetime import datetime 

import boto3
from fastapi import FastAPI, UploadFile, File, HTTPException
from botocore.exceptions import ClientError


# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the bucket name, object key (path), and local file path
BUCKET_NAME = 'bitebalances3bucket'
object_key = 'example-folder/specific-object.jpg'  # The specific object path in the policy


def process_upload_time()->str:
    current_time = str(datetime.now()).replace(' ', '-').replace(':', '-')
    current_time = current_time.split('.')
    current_time = current_time[0]
    
    return current_time


async def upload_meal(meal:UploadFile = File(...)) -> str:
    
    uppload_time = process_upload_time()
    # Define the S3 object key (path) where the file will be saved
    object_key = f"uploads/{uppload_time}/{meal.filename}"
    # Read the file contents and upload to S3
    file_content = await meal.read()
    try: 
        s3_client.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=file_content)

        logger.info(
                "--- IMAGE uploaded to {}/{}---".format(BUCKET_NAME, object_key)
            )
    
    except ClientError as e:
        # Handle S3 errors (like permission issues)
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    except Exception as e:
        # Handle general errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    
    return f"{BUCKET_NAME}/{object_key}"
