import json
import re

import boto3
from hstest import StageTest, CheckResult, dynamic_test


def import_queue_url():
    try:
        from main import queue_url
        return queue_url
    except ImportError:
        return None


class Test(StageTest):

    @dynamic_test
    def test_sqs_queue_message(self):
        # Initialize the SQS client with the Hyperprofile profile
        try:
            session = boto3.Session(profile_name='Hyperprofile')
            sqs = session.client('sqs')
        except Exception as e:
            return CheckResult.wrong(f"Could not initialize AWS session. Ensure your AWS CLI profile 'Hyperprofile' is configured correctly. Error: {str(e)}")

        queue_url = import_queue_url()
        if queue_url is None:
            return CheckResult.wrong("The variable 'queue_url' doesn't exist. Did you change or remove it?")

        if not queue_url.strip():
            return CheckResult.wrong("The 'queue_url' variable is empty. Please provide the SQS message queue URL.")

        # Check if the queue URL is in the expected format
        if not re.match(r'https://sqs\.[a-zA-Z0-9.-]+\.amazonaws\.com/[0-9]{12}/[a-zA-Z0-9_-]+', queue_url):
            return CheckResult.wrong("The 'queue_url' is not in the correct format. It should be in the format 'https://sqs.region.amazonaws.com/account-id/queue-name'.")

        # Receive a message from the SQS queue
        try:
            messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
        except Exception as e:
            return CheckResult.wrong(f"An error occurred while receiving messages from the queue. Error: {str(e)}")

        if 'Messages' not in messages or not messages['Messages']:
            return CheckResult.wrong("No messages found in the SQS queue. Ensure the Lambda function is correctly sending messages and they haven't been consumed already.")

        message_body = messages['Messages'][0]['Body']
        try:
            message = json.loads(message_body)
        except json.JSONDecodeError:
            return CheckResult.wrong("The message received from the SQS queue is not a valid JSON. Ensure the Lambda function is sending the correct message format.")

        expected_file_name = "avocado.jpg"
        expected_labels = [
            {"Name": "Food", "Confidence": 99.999},
            {"Name": "Fruit", "Confidence": 99.999},
            {"Name": "Plant", "Confidence": 99.999},
            {"Name": "Produce", "Confidence": 99.999},
            {"Name": "Avocado", "Confidence": 99.996}
        ]

        if message['file_name'] != expected_file_name:
            return CheckResult.wrong("The file name in the message does not match the expected file name. Ensure the correct image is being analyzed.")

        detected_labels = {label['Name']: label['Confidence'] for label in message['labels']}
        expected_labels_dict = {label['Name']: label['Confidence'] for label in expected_labels}

        for label, expected_confidence in expected_labels_dict.items():
            if label not in detected_labels:
                return CheckResult.wrong(f"The label '{label}' was not found in the message. Ensure your Lambda function is analyzing the provided image.")
            detected_confidence = detected_labels[label]
            if abs(detected_confidence - expected_confidence) > 0.01:
                return CheckResult.wrong(f"The confidence value for the label '{label}' is not within the expected range. Ensure your image analysis is accurate.")

        # If all checks passed
        return CheckResult.correct()
