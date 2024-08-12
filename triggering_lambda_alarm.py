import boto3
import time
import json

# Initialize the Lambda and CloudWatch clients
lambda_client = boto3.client('lambda')
cloudwatch = boto3.client('cloudwatch')

def invoke_lambda(function_name, payload):
    """
    Invoke the specified Lambda function with the given payload.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps(payload).encode('utf-8')
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        
        if 'FunctionError' in response:
            print(f"Function {function_name} failed as expected.")
        else:
            print(f"Function {function_name} succeeded. Response: {response_payload}")
        
    except Exception as e:
        print(f"Error invoking Lambda function {function_name}: {str(e)}")

def check_alarm_state(alarm_name):
    """
    Check the state of the specified CloudWatch alarm.
    """
    try:
        response = cloudwatch.describe_alarms(AlarmNames=[alarm_name])
        if response['MetricAlarms']:
            alarm_state = response['MetricAlarms'][0]['StateValue']
            print(f"Alarm '{alarm_name}' is in state: {alarm_state}")
        else:
            print(f"No alarm found with the name '{alarm_name}'")
    except Exception as e:
        print(f"Error retrieving alarm state: {str(e)}")

if __name__ == "__main__":
    # List of Lambda functions to test
    lambda_functions = ['UserActivityCollector', 'UserActivityProcessingFunction']

    # Payload designed to intentionally cause the UserActivityProcessingFunction to fail
    error_payload = {
        "invalid_key": "This should cause the function to fail"  # Adjust according to your function's expected input
    }

    # Invoke the UserActivityCollector function normally
    invoke_lambda('UserActivityCollector', {})  # Invoke with valid data

    # Invoke the UserActivityProcessingFunction to trigger an error
    invoke_lambda('UserActivityProcessingFunction', error_payload)

    # Wait longer for CloudWatch to process the errors and update the alarms
    print("Waiting for CloudWatch to update the alarm state...")
    time.sleep(180)  # Wait for 3 minutes

    # Check the state of the alarms
    for function_name in lambda_functions:
        alarm_name = f"{function_name}-Errors"
        check_alarm_state(alarm_name)
