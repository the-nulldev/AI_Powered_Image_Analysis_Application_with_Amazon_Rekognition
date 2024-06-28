import json
import logging
import time

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda function to handle events and perform image recognition.

    This function is triggered by an event, extracts the bucket name and file name from the event,
    calls AWS Rekognition to detect labels in the image, and prints the labels with a minimum confidence of 98%
    to CloudWatch logs.

    Parameters:
    event (dict): The event triggering the function, containing the S3 bucket and file information.
    context (obj): The AWS Lambda context object, not used in this function.

    Returns:
    dict: A response object containing the status code and a message.
    """

    start_time = time.time()

    # Initialize Rekognition client
    rekognition_client = boto3.client('rekognition')

    logger.info("Initialized Rekognition client")

    try:
        # Extract bucket name and file name from the event
        records = event.get('Records', [])
        if not records:
            raise ValueError("No records found in the event")

        s3_info = records[0].get('s3', {})
        bucket_name = s3_info.get('bucket', {}).get('name')
        file_name = s3_info.get('object', {}).get('key')

        if not bucket_name or not file_name:
            raise ValueError("Bucket name or file name is missing in the event")

        logger.info(f"Processing file {file_name} from bucket {bucket_name}")

        # Call Rekognition to detect labels in the image
        rekognition_start = time.time()
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_name
                }
            },
            MaxLabels=10
        )
        rekognition_end = time.time()
        logger.info(f"Rekognition call took {rekognition_end - rekognition_start} seconds")

        # Extract labels and confidence scores with a minimum confidence of 98%
        labels = response['Labels']
        filtered_labels = [
            {'Name': label['Name'], 'Confidence': label['Confidence']}
            for label in labels if label['Confidence'] >= 98.0
        ]

        # Create a response object
        result = {
            'file_name': file_name,
            'labels': filtered_labels
        }

        # Print the result to CloudWatch logs
        logger.info(json.dumps(result))

        end_time = time.time()
        logger.info(f"Lambda function completed in {end_time - start_time} seconds")

        # Return the result
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image analysis completed and results logged.'})
        }

    except Exception as e:
        error_message = str(e)
        logger.error(f"Error: {error_message}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
