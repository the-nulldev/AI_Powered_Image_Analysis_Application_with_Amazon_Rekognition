import re

import requests
from hstest import StageTest, CheckResult, dynamic_test


def import_object_url():
    try:
        from main import object_url as object_url
        return object_url
    except ImportError:
        return None


class Test(StageTest):

    @dynamic_test
    def test(self):

        object_url = import_object_url()

        if object_url is None:
            return CheckResult.wrong("The variable 'object_url' doesn't exist. Did you change or remove it?")

        if not object_url.strip():
            return CheckResult.wrong("The 'object_url' variable is empty. Please provide the S3 object URL.")

        # Check if the bucket URL is in the expected format
        if not re.match(r'https://[a-zA-Z0-9.-]+\.s3\.amazonaws\.com/?', object_url):
            return CheckResult.wrong("The 'object_url' is not in the correct format. It should be in the format 'https://your-unique-bucket-name.s3.amazonaws.com'.")

        try:
            response = requests.get(object_url)
        except requests.RequestException as e:
            return CheckResult.wrong(f"Failed to send GET request to the URL. Error: {e}")
        #
        # # Check if the response status code is 200 (OK)
        # if response.status_code != 200:
        #     return CheckResult.wrong(f"The GET request to the URL did not return a 200 status code. Status code: {response.status_code}")

        if response.status_code == 403:
            return CheckResult.wrong("The bucket could not be accessed. Please ensure the bucket exists and is public.")
        # Check if the response content type indicates an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return CheckResult.wrong(f"The response does not contain an image. Content-Type: {content_type}")

        # Check if the response headers indicate that the site is hosted by Amazon
        server_header = response.headers.get('Server', '')
        if 'AmazonS3' not in server_header:
            return CheckResult.wrong(f"The site does not appear to be hosted by Amazon S3. Server header: {server_header}")

        # If all checks passed
        return CheckResult.correct()

