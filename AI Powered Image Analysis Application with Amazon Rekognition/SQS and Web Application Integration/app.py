import json
import os
import re
import dotenv
import time

import boto3
from flask import Flask, request, redirect, url_for, render_template_string

dotenv.load_dotenv()

app = Flask(__name__)

# Configuration
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# AWS S3 and SQS Configuration
S3_BUCKET = "<your-s3-bucket-name>"
SQS_QUEUE_URL = "<your-sqs-queue-url>"

# Validate S3 bucket name
if not S3_BUCKET or not re.match(r'^[a-zA-Z0-9.\-_]{1,255}$', S3_BUCKET):
    raise ValueError("Invalid S3 bucket name. Ensure the S3_BUCKET variable is set correctly.")

# Initialize Boto3 session
session = boto3.Session(
    profile_name='Hyperprofile',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1"
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
    upload_form = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Upload Image</title>
    </head>
    <body>
    <h1>Upload Image</h1>
    <form action="{{ url_for('upload_file') }}" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit="Upload">
    </form>
    <br>
    <h1>Retrieve Analysis Results</h1>
    <form action="{{ url_for('retrieve_results') }}" method="get">
        <input type="submit" value="Retrieve">
    </form>
    </body>
    </html>
    '''
    return render_template_string(upload_form)


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
            s3_client.upload_fileobj(file, S3_BUCKET, filename)
        except Exception as e:
            return f"Failed to upload file to S3: {str(e)}", 500

        return "File uploaded successfully. You can now retrieve the analysis results.", 200
    return redirect(url_for('index'))


@app.route('/retrieve', methods=['GET'])
def retrieve_results():
    # Poll the SQS queue to retrieve the analysis results
    analysis_result = None
    for _ in range(5):  # Polling up to 5 times
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,  # Receive multiple messages
            WaitTimeSeconds=5,
            AttributeNames=['SentTimestamp']
        )
        messages = response.get('Messages', [])
        if messages:
            # Find the latest message based on the SentTimestamp attribute
            latest_message = max(messages, key=lambda msg: int(msg['Attributes']['SentTimestamp']))
            analysis_result = json.loads(latest_message['Body'])
            sqs_client.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=latest_message['ReceiptHandle']
            )
            break
        time.sleep(1)  # Wait for 1 second before retrying

    if analysis_result:
        display_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Analysis Results</title>
        </head>
        <body>
        <h1>Analysis Results</h1>
        <pre>{{ analysis_result | tojson(indent=2) }}</pre>
        </body>
        </html>
        '''
        return render_template_string(display_template, analysis_result=analysis_result)
    else:
        return "Analysis results not found. Please try again.", 404


if __name__ == '__main__':
    app.run(debug=True)
