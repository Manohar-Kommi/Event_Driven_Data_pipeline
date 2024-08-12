import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
bucket_name = 'user-activity-tracking-prod'

try:
    # Create the S3 bucket
    s3.create_bucket(Bucket=bucket_name)
    print(f'Successfully created the bucket: {bucket_name}')
except ClientError as e:
    print(f'Error creating bucket: {e}')

# List objects in the specified S3 bucket
response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])  # Print the name of each object
else:
    print('No objects found in the bucket.')
