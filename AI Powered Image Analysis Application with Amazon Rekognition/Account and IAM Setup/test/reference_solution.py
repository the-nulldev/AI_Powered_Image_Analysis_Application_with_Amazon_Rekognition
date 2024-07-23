"""
Please provide the JSON reply you received from the command between the triple quotes below.
Do not change the variable name or the triple quotes surrounding the JSON reply.
"""
user_json = """
{
    "UserName": "RekognitionAppUser",
    "CreateDate": "2024-06-27T16:17:35+00:00"
}
"""

role_json = """
{
    "RoleName": "LambdaPermissionsRole",
    "CreateDate": "2024-06-27T16:31:48+00:00"
}
"""

user_policy_json = """
{
    "PolicyName": "UserAccessPolicy",
    "PolicyId": "ANPARWU276MGGOILKWYBV",
    "CreateDate": "2024-06-27T17:55:07+00:00"
}
"""

lambda_policy_json = """
{
    "PolicyName": "LambdaAccessPolicy",
    "PolicyId": "ANPARWU276MGG2ASQZV3V",
    "CreateDate": "2024-06-27T16:10:31+00:00"
}
"""

user_policy_entities_json = """
{
    "UserAccessPolicy": {
        "AttachedEntities": {
            "Users": [
                "RekognitionAppUser"
            ],
            "Roles": [],
            "Groups": []
        }
    }
}
"""

lambda_policy_entities_json = """
{
    "LambdaAccessPolicy": {
        "AttachedEntities": {
            "Users": [],
            "Roles": [
                "LambdaPermissionsRole"
            ],
            "Groups": []
        }
    }
}
"""
