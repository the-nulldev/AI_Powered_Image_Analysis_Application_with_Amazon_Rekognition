import json
import os
import re
import time

import boto3
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# AWS S3 and SQS Configuration
S3_BUCKET = os.getenv('BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Initialize Boto3 session
session = boto3.Session(
    profile_name='Hyperprofile',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=AWS_REGION
)

s3_client = session.client('s3')
sqs_client = session.client('sqs')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def secure_filename(filename):
    """
    Pass it a filename and it will return a secure version of it. This filename
    can then safely be stored on a regular file system and passed to os.path.join.
    """
    filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
    return filename


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        try:
            # Upload to S3
            s3_client.upload_fileobj(file, S3_BUCKET, filename)
        except Exception as e:
            return f"Failed to upload file to S3: {str(e)}", 500

        return "File uploaded successfully. You can now retrieve the analysis results.", 200
    return redirect(url_for('index'))


@app.route('/retrieve', methods=['GET'])
def retrieve_results():
    # Poll the SQS queue to retrieve the analysis results
    analysis_result = None
    for _ in range(10):  # Polling up to 10 times
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
        messages = response.get('Messages', [])
        if messages:
            message = messages[0]
            analysis_result = json.loads(message['Body'])
            sqs_client.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
            break
        time.sleep(1)  # Wait for 1 second before retrying

    if analysis_result:
        return render_template('display.html', analysis_result=analysis_result)
    else:
        return "Analysis results not found. Please try again.", 404


if __name__ == '__main__':
    app.run(debug=True)
