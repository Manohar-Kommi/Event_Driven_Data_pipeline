import boto3
import json

# Initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch')

def create_lambda_alarm(function_name):
    alarm_name = f"{function_name}-Errors"
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName='Errors',
        Namespace='AWS/Lambda',
        Statistic='Sum',
        Period=60,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanThreshold',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': function_name
            },
        ],
        ActionsEnabled=True,
        AlarmActions=[
            # Specify the SNS Topic ARN for notifications
            "arn:aws:sns:us-east-1:211125559197:UserActivityAlerts"
        ],
        AlarmDescription='Alarm when the function exceeds 1 error in a minute',
        Unit='Count'
    )
    print(f"Created alarm: {alarm_name}")

def create_step_function_alarm(state_machine_name):
    alarm_name = f"{state_machine_name}-FailedExecutions"
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName='ExecutionsFailed',
        Namespace='AWS/States',
        Statistic='Sum',
        Period=60,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanThreshold',
        Dimensions=[
            {
                'Name': 'StateMachineName',
                'Value': state_machine_name
            },
        ],
        ActionsEnabled=True,
        AlarmActions=[
            # Specify the SNS Topic ARN for notifications
            "arn:aws:sns:us-east-1:211125559197:UserActivityAlerts"
        ],
        AlarmDescription='Alarm when the Step Function fails',
        Unit='Count'
    )
    print(f"Created alarm: {alarm_name}")

def create_dashboard():
    dashboard_name = 'UserActivityTrackingDashboard'
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "Errors", "FunctionName", "UserActivityCollector"],
                        ["AWS/Lambda", "Errors", "FunctionName", "UserActivityProcessingFunction"]
                    ],
                    "period": 300,
                    "stat": "Sum",
                    "region": "us-east-1",  # Specify your AWS region
                    "title": "Lambda Errors",
                    "annotations": {
                        "horizontal": [
                            {
                                "label": "Error Threshold",
                                "value": 0,
                            }
                        ]
                    }
                }
            },
            {
                "type": "metric",
                "x": 6,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/States", "ExecutionsFailed", "StateMachineName", "UserActivityTrackingStateMachine"]
                    ],
                    "period": 300,
                    "stat": "Sum",
                    "region": "us-east-1",  # Specify your AWS region
                    "title": "Step Function Failures",
                    "annotations": {
                        "horizontal": [
                            {
                                "label": "Failure Threshold",
                                "value": 0,
                            }
                        ]
                    }
                }
            }
        ]
    }

    # Create or update the dashboard
    response = cloudwatch.put_dashboard(
        DashboardName=dashboard_name,
        DashboardBody=json.dumps(dashboard_body)
    )
    print(f"Created dashboard: {dashboard_name}")

if __name__ == "__main__":
    # Create alarms for the specified Lambda functions
    lambda_functions = ['UserActivityCollector', 'UserActivityProcessingFunction']
    for function in lambda_functions:
        create_lambda_alarm(function)

    # Create alarm for the Step Function
    create_step_function_alarm('UserActivityTrackingStateMachine')

    # Create CloudWatch dashboard
    create_dashboard()
