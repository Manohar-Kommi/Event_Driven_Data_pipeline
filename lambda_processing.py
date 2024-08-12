import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = 'UserActivityTable'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            print(f"Bucket: {bucket}, Key: {key}")

            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=bucket, Key=key)
            json_data = response['Body'].read().decode('utf-8')
            user_activities = json.loads(json_data)

            for activity in user_activities:
                # Check if all required keys are present
                required_keys = ['UserId', 'ActivityId', 'ActivityType', 'Timestamp', 'ActivityData']  # Use UserId with uppercase U
                if all(key in activity for key in required_keys):
                    table.put_item(
                        Item={
                            'userId': activity['UserId'],   # Ensure this matches your DynamoDB schema
                            'id': activity['ActivityId'],    # Assuming this is your sort key
                            'ActivityType': activity['ActivityType'],
                            'Timestamp': activity['Timestamp'],
                            'ActivityData': activity['ActivityData']
                        }
                    )
                else:
                    print(f"Error: Missing one or more required keys in activity: {activity}")
                    missing_keys = [key for key in required_keys if key not in activity]
                    print(f"Missing keys: {missing_keys}")

        return {
            'statusCode': 200,
            'body': json.dumps('User activities successfully stored in DynamoDB')
        }
    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to store user activities in DynamoDB')
        }
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred')
        }
