import json
import re
import boto3
from hstest import StageTest, CheckResult, dynamic_test

class Test(StageTest):

    @dynamic_test
    def test_latest_sqs_message(self):
        # Initialize the session and clients
        try:
            session = boto3.Session(profile_name='Hyperprofile')
            sqs = session.client('sqs')
        except Exception as e:
            return CheckResult.wrong(f"Could not initialize AWS session. Ensure your AWS CLI profile 'Hyperprofile' is configured correctly. Error: {str(e)}")

        # Import queue URL
        try:
            from main import queue_url
        except ImportError:
            return CheckResult.wrong("Ensure that 'SQS_QUEUE_URL' variable is set in your app.py file.")

        if not queue_url.strip():
            return CheckResult.wrong("The 'queue_url' variable is empty. Please provide the SQS message queue URL.")

        # Check if the queue URL is in the expected format
        if not re.match(r'https://sqs\.[a-zA-Z0-9.-]+\.amazonaws\.com/[0-9]{12}/[a-zA-Z0-9_-]+', queue_url):
            return CheckResult.wrong("The 'SQS_QUEUE_URL' is not in the correct format. It should be in the format 'https://sqs.region.amazonaws.com/account-id/queue-name'.")

        # Define the expected file name and labels
        expected_file_name = "avocado.jpg"
        expected_labels = [
            {"Name": "Food", "Confidence": 99.999},
            {"Name": "Fruit", "Confidence": 99.999},
            {"Name": "Plant", "Confidence": 99.999},
            {"Name": "Produce", "Confidence": 99.999},
            {"Name": "Avocado", "Confidence":99.996}
        ]

        # Step 1: Verify the SQS message content
        try:
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,  # Receive up to 10 messages
                WaitTimeSeconds=10,
                AttributeNames=['SentTimestamp']
            )
        except Exception as e:
            return CheckResult.wrong(f"An error occurred while receiving messages from the queue. Error: {str(e)}")

        if 'Messages' not in messages or not messages['Messages']:
            return CheckResult.wrong("No messages found in the SQS queue. Ensure the Lambda function is correctly sending messages and they haven't been consumed already.")

        # Find the latest message based on the SentTimestamp attribute
        latest_message = max(messages['Messages'], key=lambda msg: int(msg['Attributes']['SentTimestamp']))

        message_body = latest_message['Body']
        try:
            message = json.loads(message_body)
        except json.JSONDecodeError:
            return CheckResult.wrong("The message received from the SQS queue is not a valid JSON. Ensure the Lambda function is sending the correct message format.")

        if message['file_name'] != expected_file_name:
            return CheckResult.wrong(f"The file name in the message does not match the expected file name. Found: {message['file_name']}, Expected: {expected_file_name}")

        detected_labels = {label['Name']: label['Confidence'] for label in message['labels']}
        expected_labels_dict = {label['Name']: label['Confidence'] for label in expected_labels}

        for label, expected_confidence in expected_labels_dict.items():
            if label not in detected_labels:
                return CheckResult.wrong(f"The label '{label}' was not found in the message. Ensure your Lambda function is analyzing the provided image.")
            detected_confidence = detected_labels[label]
            if abs(detected_confidence - expected_confidence) > 0.01:
                return CheckResult.wrong(f"The confidence value for the label '{label}' is not within the expected range. Ensure you uploaded the right image.")

        # If all checks passed
        return CheckResult.correct()
