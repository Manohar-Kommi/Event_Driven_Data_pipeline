import boto3

# Initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch')

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

if __name__ == "__main__":
    state_machine_name = 'UserActivityTrackingStateMachine'
    create_step_function_alarm(state_machine_name)
