import boto3

dynamodb = boto3.client('dynamodb')

def check_table_exists(table_name):
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except dynamodb.exceptions.ResourceNotFoundException:
        return False
    except Exception as e:
        print(f"Error checking table existence: {str(e)}")
        return False

def create_dynamodb_table():
    table_name = 'UserActivityTable'
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'userId',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'userId',
                    'AttributeType': 'S'  # Changed to String
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'  # Changed to String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully!")
        return response
    except Exception as e:
        print(f"Error creating table: {str(e)}")

# Check if the table exists
table_name = 'UserActivityTable'
if check_table_exists(table_name):
    print(f"Table already exists: {table_name}")
else:
    # Create the new table with string attributes
    create_dynamodb_table()
