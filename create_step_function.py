import boto3
import json

# Initialize the Step Functions client
client = boto3.client('stepfunctions')

# Define the state machine
state_machine_definition = {
    "Comment": "A simple AWS Step Functions state machine that collects user activity, processes it, and stores it in DynamoDB.",
    "StartAt": "ProcessUserActivity",
    "States": {
        "ProcessUserActivity": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:211125559197:function:UserActivityProcessingFunction",
            "End": True,
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "ResultPath": "$.error-info",
                    "Next": "ErrorHandler"
                }
            ]
        },
        "ErrorHandler": {
            "Type": "Fail",
            "Error": "Error in State Machine",
            "Cause": "$.error-info"
        }
    }
}

# Create or update the state machine
try:
    response = client.create_state_machine(
        name='UserActivityTrackingStateMachine',
        definition=json.dumps(state_machine_definition),
        roleArn='arn:aws:iam::211125559197:role/LambdaStepFunctionRole'  # Ensure this role has necessary permissions
    )
    print('Step Function created:', response['stateMachineArn'])
except client.exceptions.StateMachineAlreadyExists:
    # Update the state machine if it already exists
    response = client.update_state_machine(
        stateMachineArn='arn:aws:states:us-east-1:211125559197:stateMachine:UserActivityTrackingStateMachine',
        definition=json.dumps(state_machine_definition)
    )
    print('Step Function updated:', response['updateDate'])
except Exception as e:
    print("Error creating or updating state machine:", e)
