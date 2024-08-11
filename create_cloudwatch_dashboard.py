import boto3
import json

def create_dashboard():
    cloudwatch = boto3.client('cloudwatch')

    dashboard_name = 'UserActivityDashboard'
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 24,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/Lambda", "Errors", "FunctionName", "UserActivityCollector"],
                        ["AWS/Lambda", "Errors", "FunctionName", "UserActivityProcessingFunction"]
                    ],
                    "region": "us-east-1",  # Specify your AWS region
                    "title": "Lambda Errors",
                    "annotations": {
                        "horizontal": [
                            {
                                "label": "Error Threshold",
                                "value": 0,
                                "color": "#FF0000"
                            }
                        ]
                    }
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 24,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/StepFunctions", "ExecutionsFailed", "StateMachineArn", "arn:aws:states:us-east-1:211125559197:stateMachine:UserActivityTrackingStateMachine"],
                    ],
                    "region": "us-east-1",  # Specify your AWS region
                    "title": "Step Function Failures",
                    "annotations": {
                        "horizontal": [
                            {
                                "label": "Failure Threshold",
                                "value": 0,
                                "color": "#FF0000"
                            }
                        ]
                    }
                }
            }
        ]
    }

    try:
        response = cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        print('Dashboard created successfully:', response)
    except Exception as e:
        print('Error creating dashboard:', e)

if __name__ == "__main__":
    create_dashboard()
