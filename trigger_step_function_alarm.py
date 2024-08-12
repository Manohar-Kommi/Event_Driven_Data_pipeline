import boto3
import json
import time

# Initialize the Step Functions client
step_functions = boto3.client('stepfunctions')

# Function to trigger the Step Function with input that will cause a failure
def trigger_failure():
    input_data = {
        "trigger_error": True  # This should trigger an error in your Lambda function
    }

    try:
        # Start execution of the Step Function with input that causes an error
        response = step_functions.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:211125559197:stateMachine:UserActivityTrackingStateMachine',
            input=json.dumps(input_data)
        )
        execution_arn = response['executionArn']
        print(f'Started execution: {execution_arn}')
        return execution_arn
    except Exception as e:
        print(f'Error starting execution: {str(e)}')
        return None

# Function to wait for the execution to fail
def wait_for_failure(execution_arn):
    while True:
        response = step_functions.describe_execution(executionArn=execution_arn)
        status = response['status']
        print(f'Execution status: {status}')
        
        if status in ['FAILED', 'TIMED_OUT', 'ABORTED']:
            print(f'Execution failed as expected: {execution_arn}')
            break
        elif status == 'SUCCEEDED':
            print('Execution succeeded unexpectedly.')
            break
        
        time.sleep(5)  # Wait for 5 seconds before checking again

# Function to check the state of the CloudWatch alarm
def check_alarm_state():
    cloudwatch = boto3.client('cloudwatch')
    alarm_name = 'UserActivityTrackingStateMachine-FailedExecutions'
    
    try:
        response = cloudwatch.describe_alarms(AlarmNames=[alarm_name])
        alarm_state = response['MetricAlarms'][0]['StateValue']
        print(f"Alarm '{alarm_name}' is in state: {alarm_state}")
    except Exception as e:
        print(f'Error checking alarm state: {str(e)}')

if __name__ == "__main__":
    # Trigger the Step Function failure
    execution_arn = trigger_failure()
    
    if execution_arn:
        # Wait for the execution to fail
        wait_for_failure(execution_arn)
        
        # Give CloudWatch some time to update the alarm state
        print("Waiting for CloudWatch to update the alarm state...")
        time.sleep(120)  # Wait for 2 minutes
        
        # Check the state of the CloudWatch alarm
        check_alarm_state()
