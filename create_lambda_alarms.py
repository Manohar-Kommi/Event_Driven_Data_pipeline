import boto3

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

if __name__ == "__main__":
    lambda_functions = ['UserActivityCollector', 'UserActivityProcessingFunction']
    for function in lambda_functions:
        create_lambda_alarm(function)
