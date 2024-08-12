import boto3

# Replace these values with your actual AWS credentials
aws_access_key_id = 'xxxxxxx'
aws_secret_access_key = 'xxxxxxxxxxx'
region_name = 'us-east-1'  # Replace with your preferred region

# Initialize a session using your credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create an S3 client
s3 = session.client('s3')

# Print a message indicating the AWS environment is ready to use
print('AWS environment is ready to use!')

# Optionally, you can still check if S3 is accessible (without printing buckets)
try:
    response = s3.list_buckets()
    print('Successfully accessed S3 service.')
except Exception as e:
    print(f'Error accessing S3: {str(e)}')
