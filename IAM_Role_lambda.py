import json
import boto3
from botocore.exceptions import ClientError

# Initialize the IAM client
iam = boto3.client('iam')

# Define the trust policy for the Lambda and Step Functions role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "states.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# Define role name
role_name = 'LambdaStepFunctionRole'

# Check if the role already exists
try:
    existing_role = iam.get_role(RoleName=role_name)
    print(f"Role '{role_name}' already exists. ARN: {existing_role['Role']['Arn']}")
except iam.exceptions.NoSuchEntityException:
    # Role does not exist, create it
    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='IAM role for Lambda and Step Functions to access S3 and DynamoDB'
        )
        print(f"Role created successfully: {role['Role']['Arn']}")
    except ClientError as e:
        print(f"Error creating role: {e}")

# Attach necessary policies to the role
try:
    # Attach restrictive S3 access policy
    s3_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::user-activity-tracking-prod",
                    "arn:aws:s3:::user-activity-tracking-prod/*"
                ]
            }
        ]
    }
    
    # Create and attach S3 policy
    s3_policy_name = 'LambdaS3AccessPolicy'
    try:
        iam.create_policy(
            PolicyName=s3_policy_name,
            PolicyDocument=json.dumps(s3_policy_document),
            Description='Policy for Lambda functions to access S3'
        )
        print(f"Created policy '{s3_policy_name}' successfully.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Policy '{s3_policy_name}' already exists.")

    iam.attach_role_policy(RoleName=role_name, PolicyArn=f'arn:aws:iam::211125559197:policy/{s3_policy_name}')
    print(f"Attached policy {s3_policy_name} to {role_name} successfully.")

    # Attach restrictive DynamoDB access policy
    dynamodb_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Scan"
                ],
                "Resource": "arn:aws:dynamodb:us-east-1:211125559197:table/UserActivityTable"  # Ensure the correct table name
            }
        ]
    }
    
    # Create and attach DynamoDB policy
    dynamodb_policy_name = 'LambdaDynamoDBAccessPolicy'
    try:
        iam.create_policy(
            PolicyName=dynamodb_policy_name,
            PolicyDocument=json.dumps(dynamodb_policy_document),
            Description='Policy for Lambda functions to access DynamoDB'
        )
        print(f"Created policy '{dynamodb_policy_name}' successfully.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Policy '{dynamodb_policy_name}' already exists.")

    iam.attach_role_policy(RoleName=role_name, PolicyArn=f'arn:aws:iam::211125559197:policy/{dynamodb_policy_name}')
    print(f"Attached policy {dynamodb_policy_name} to {role_name} successfully.")

    # Attach Lambda basic execution policy
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    print(f"Attached policy AWSLambdaBasicExecutionRole to {role_name} successfully.")

    # Attach Step Functions full access policy
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/AWSStepFunctionsFullAccess'
    )
    print(f"Attached policy AWSStepFunctionsFullAccess to {role_name} successfully.")

    # Create a custom policy for invoking Lambda functions
    invoke_policy_name = 'LambdaInvokePolicy'
    invoke_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "lambda:InvokeFunction",
                "Resource": [
                    "arn:aws:lambda:us-east-1:211125559197:function:UserActivityCollector",
                    "arn:aws:lambda:us-east-1:211125559197:function:UserActivityProcessingFunction"
                ]
            }
        ]
    }

    # Check if the invoke policy already exists
    try:
        iam.get_policy(PolicyArn=f'arn:aws:iam::211125559197:policy/{invoke_policy_name}')
        print(f"Policy '{invoke_policy_name}' already exists.")
    except iam.exceptions.NoSuchEntityException:
        # Create the policy if it doesn't exist
        invoke_policy = iam.create_policy(
            PolicyName=invoke_policy_name,
            PolicyDocument=json.dumps(invoke_policy_document),
            Description='Custom policy to allow invoking specific Lambda functions'
        )
        print(f"Created policy '{invoke_policy_name}' successfully.")

    # Attach the custom invoke policy to the role
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=f'arn:aws:iam::211125559197:policy/{invoke_policy_name}'
    )
    print(f"Attached policy {invoke_policy_name} to {role_name} successfully.")

except ClientError as e:
    print(f"Error attaching policies: {e}")
