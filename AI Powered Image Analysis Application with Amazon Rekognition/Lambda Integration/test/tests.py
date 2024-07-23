import json

from hstest import StageTest, CheckResult, dynamic_test

def import_function_json():
    try:
        from main import function_json
        return json.loads(function_json)
    except ImportError:
        return None
    except json.JSONDecodeError:
        return "invalid"


def import_logs_json():
    try:
        from main import logs_json
        return json.loads(logs_json)
    except ImportError:
        return None
    except json.JSONDecodeError:
        return "invalid"


class Test(StageTest):

    @dynamic_test
    def test_function_json(self):
        function_json = import_function_json()

        if function_json is None:
            return CheckResult.wrong("The variable 'function_json' doesn't exist. Did you change or remove it?")

        if function_json == "invalid":
            return CheckResult.wrong("The 'function_json' variable is not a valid JSON string. Please ensure it is not empty and is correctly formatted.")

        expected_function_json = [
            "ImageAnalysisFunction",
            "python3.12",
            "arn:aws:iam::123456789012:role/RekognitionAccessRole",
            "lambda_function.lambda_handler",
            60,
            128
        ]

        if function_json != expected_function_json:
            return CheckResult.wrong(f"The 'function_json' is incorrect. Got '{function_json}' which is not the expected value. Verify that the function configuration is correct.")

        return CheckResult.correct()

    @dynamic_test
    def test_logs_json(self):
        logs_json = import_logs_json()

        if logs_json is None:
            return CheckResult.wrong("The variable 'logs_json' doesn't exist. Did you change or remove it?")

        if logs_json == "invalid":
            return CheckResult.wrong("The 'logs_json' variable is not a valid JSON string. Please ensure it is not empty and is correctly formatted.")

        if not isinstance(logs_json, list):
            return CheckResult.wrong("The 'logs_json' variable should be a list of log stream dictionaries.")

        if len(logs_json) == 0:
            return CheckResult.wrong("The 'logs_json' list is empty. Ensure that there are log streams available.")

        for log in logs_json:
            if "logStreamName" not in log or "creationTime" not in log:
                return CheckResult.wrong("Each log stream should have 'logStreamName' and 'creationTime' fields.")

        return CheckResult.correct()
