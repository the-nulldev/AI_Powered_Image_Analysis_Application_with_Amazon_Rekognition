"""
Please provide the JSON reply you received from the commands between the triple quotes below.
Do not change the variable name or the triple quotes surrounding the JSON replies
"""

function_json = """
[
    "ImageAnalysisFunction",
    "python3.12",
    "arn:aws:iam::123456789012:role/RekognitionAccessRole",
    "lambda_function.lambda_handler",
    60,
    128
]
"""

logs_json = """
[
    {
        "logStreamName": "2024/06/24/[$LATEST]5036a4537dd94f1fb0075a35dae7067a",
        "creationTime": 1719272659358
    },
    {
        "logStreamName": "2024/06/24/[$LATEST]6f522c00c2634b478b73a808bd8acf1d",
        "creationTime": 1719273333398
    },
    {
        "logStreamName": "2024/06/24/[$LATEST]97455da4557a47c19448513de74ed138",
        "creationTime": 1719272670608
    },
    {
        "logStreamName": "2024/06/25/[$LATEST]1b1e679b79fc458baa328f6b5aa89967",
        "creationTime": 1719274237523
    },
    {
        "logStreamName": "2024/06/25/[$LATEST]8caf517d49794a6f9b128e1f4fbc0dc9",
        "creationTime": 1719274613319
    }
]
"""