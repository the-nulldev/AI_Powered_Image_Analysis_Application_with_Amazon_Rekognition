import json

from hstest import StageTest, CheckResult, dynamic_test


def import_labels_json():
    try:
        from main import labels_json
        return json.loads(labels_json)
    except ImportError:
        return None
    except json.JSONDecodeError:
        return "invalid"


class Test(StageTest):

    @dynamic_test
    def test(self):

        labels_json = import_labels_json()

        if labels_json is None:
            return CheckResult.wrong("The variable 'labels_json' doesn't exist. Did you change or remove it?")

        if labels_json == "invalid":
            return CheckResult.wrong("The 'labels_json' variable is not a valid JSON string. Please ensure it is not empty and is correctly formatted.")

        if not isinstance(labels_json, dict):
            return CheckResult.wrong("The 'labels_json' variable should be a dictionary representing the JSON response.")

        expected_labels = [
            {"Name": "Food", "Confidence": 99.8},
            {"Name": "Plant", "Confidence": 99.8},
            {"Name": "Produce", "Confidence": 99.8},
            {"Name": "Tomato", "Confidence": 99.8},
            {"Name": "Vegetable", "Confidence": 99.8},
            {"Name": "Box", "Confidence": 98.0},
            {"Name": "Fruit", "Confidence": 72.1}
        ]

        detected_labels = labels_json.get("Labels", [])
        if not detected_labels:
            return CheckResult.wrong("The 'labels_json' does not contain any labels. Please ensure the image was analyzed correctly.")

        detected_labels_dict = {label["Name"]: label["Confidence"] for label in detected_labels}

        for expected_label in expected_labels:
            label_name = expected_label["Name"]
            expected_confidence = expected_label["Confidence"]
            detected_confidence = detected_labels_dict.get(label_name, None)

            if detected_confidence is None:
                return CheckResult.wrong(f"The label '{label_name}' was not detected in the image. Ensure the image analysis is correct.")

            if detected_confidence < expected_confidence - 0.1:
                return CheckResult.wrong(f"The confidence level for the label '{label_name}' is too low. Expected at least {expected_confidence} but got {detected_confidence}.")

        # If all checks passed
        return CheckResult.correct()
