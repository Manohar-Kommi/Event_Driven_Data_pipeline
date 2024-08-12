import json
import boto3
import os

# Initialize the S3 client
s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']  # Retrieve the bucket name from environment variables

def lambda_handler(event, context):
    try:
        # Read the local JSON file
        file_path = 'sample_user_activity_data.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Store data in S3
        s3.put_object(
            Bucket=bucket_name,
            Key='user_activity.json',  # Define the file name in S3
            Body=json.dumps(data)  # Convert the data to JSON format
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Data collected and stored in S3!')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error occurred: {str(e)}')
        }
