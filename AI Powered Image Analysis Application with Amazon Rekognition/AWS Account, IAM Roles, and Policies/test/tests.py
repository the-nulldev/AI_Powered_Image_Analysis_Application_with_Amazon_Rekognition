import json

from hstest import StageTest, CheckResult, dynamic_test


def import_json(variable_name):
    if variable_name == 'user_json':
        try:
            from main import user_json
            return user_json
        except ImportError:
            return None
    elif variable_name == 'role_json':
        try:
            from main import role_json
            return role_json
        except ImportError:
            return None
    elif variable_name == 'user_policy_json':
        try:
            from main import user_policy_json
            return user_policy_json
        except ImportError:
            return None
    elif variable_name == 'lambda_policy_json':
        try:
            from main import lambda_policy_json
            return lambda_policy_json
        except ImportError:
            return None
    elif variable_name == 'user_policy_entities_json':
        try:
            from main import user_policy_entities_json
            return user_policy_entities_json
        except ImportError:
            return None
    elif variable_name == 'lambda_policy_entities_json':
        try:
            from main import lambda_policy_entities_json
            return lambda_policy_entities_json
        except ImportError:
            return None
    return None


class Test(StageTest):

    @dynamic_test
    def test(self):

        user_json = import_json('user_json')
        role_json = import_json('role_json')
        user_policy_json = import_json('user_policy_json')
        lambda_policy_json = import_json('lambda_policy_json')
        user_policy_entities_json = import_json('user_policy_entities_json')
        lambda_policy_entities_json = import_json('lambda_policy_entities_json')

        # Check if all variables exist
        variables = {
            'user_json': user_json,
            'role_json': role_json,
            'user_policy_json': user_policy_json,
            'lambda_policy_json': lambda_policy_json,
            'user_policy_entities_json': user_policy_entities_json,
            'lambda_policy_entities_json': lambda_policy_entities_json
        }
        for var_name, var_value in variables.items():
            if var_value is None:
                return CheckResult.wrong(f"The variable '{var_name}' doesn't exist. Did you change or remove it?")

        # Attempt to parse the JSON replies
        try:
            user_response = json.loads(user_json)
            role_response = json.loads(role_json)
            user_policy_response = json.loads(user_policy_json)
            lambda_policy_response = json.loads(lambda_policy_json)
            user_policy_entities_response = json.loads(user_policy_entities_json)
            lambda_policy_entities_response = json.loads(lambda_policy_entities_json)
        except json.JSONDecodeError:
            return CheckResult.wrong("One of the JSON replies is not valid. Please ensure the JSON reply for all variables is correct.")

        # Check if the necessary keys are present in the JSON response for user
        user_required_keys = ["UserName", "CreateDate"]
        for key in user_required_keys:
            if key not in user_response:
                return CheckResult.wrong(f"The User JSON reply is missing the key: {key}. Ensure the user was created correctly.")

        # Check if the necessary keys are present in the JSON response for role
        role_required_keys = ["RoleName", "CreateDate"]

        for key in role_required_keys:
            if key not in role_response:
                return CheckResult.wrong(f"The Role JSON reply is missing the key: {key}. Ensure the role was created correctly.")

        # Check if the necessary keys are present in the JSON response for user policy
        policy_required_keys = ["PolicyName", "CreateDate"]
        for key in policy_required_keys:
            if key not in user_policy_response:
                return CheckResult.wrong(f"The User Policy JSON reply is missing the key: {key}. Ensure the policy was created correctly.")

        # Check if the necessary keys are present in the JSON response for lambda policy
        for key in policy_required_keys:
            if key not in lambda_policy_response:
                return CheckResult.wrong(f"The Lambda Policy JSON reply is missing the key: {key}. Ensure the policy was created correctly.")

        # Check if the necessary keys are present in the JSON response for user policy entities
        entity_required_keys = ["Users", "Roles", "Groups"]
        user_policy_entities = user_policy_entities_response.get("UserAccessPolicy", {}).get("AttachedEntities", {})
        for key in entity_required_keys:
            if key not in user_policy_entities:
                return CheckResult.wrong(f"The User Policy Entities JSON reply is missing the key: {key}. Ensure the entities were listed correctly.")

        # Check if the necessary keys are present in the JSON response for lambda policy entities
        lambda_policy_entities = lambda_policy_entities_response.get("LambdaAccessPolicy", {}).get("AttachedEntities", {})
        for key in entity_required_keys:
            if key not in lambda_policy_entities:
                return CheckResult.wrong(f"The Lambda Policy Entities JSON reply is missing the key: {key}. Ensure the entities were listed correctly.")

        # Verify that the UserAccessPolicy is attached to the username RekognitionAppUser
        if "RekognitionAppUser" not in user_policy_entities.get("Users", []):
            return CheckResult.wrong("The policy UserAccessPolicy is not attached to the expected user. Ensure the policy is correctly attached to the user.")

        # Verify that the LambdaAccessPolicy is attached to the role LambdaPermissionsRole
        if "LambdaPermissionsRole" not in lambda_policy_entities.get("Roles", []):
            return CheckResult.wrong("The policy LambdaAccessPolicy is not attached to the expected role. Ensure the policy is correctly attached to the role.")

        # If all checks passed
        return CheckResult.correct()
