Here's an expanded and detailed version of the README file, suitable for uploading to GitHub:

---

# Event Driven Data Pipeline Project

This project implements a real-time user data processing pipeline using various AWS services, including Lambda, S3, DynamoDB, Step Functions, IAM roles, and CloudWatch. This README will guide you through the steps needed to set up, deploy, and manage the pipeline.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup and Deployment Instructions](#setup-and-deployment-instructions)
  - [1. Setting AWS Environment](#1-Setting-AWS-Environment)
  - [2. Create S3 Buckets](#1-create-s3-buckets)
  - [3. Create IAM Roles](#2-create-iam-roles)
  - [4. Deploy Lambda Functions](#3-deploy-lambda-functions)
  - [5. Create DynamoDB Tables](#4-create-dynamodb-tables)
  - [6. Deploy Processing_lambda](#3-deploy-processing-lambda)
  - [7. Create and Configure Step Functions](#5-create-and-configure-step-functions)
  - [8. Setup CloudWatch Alarms](#6-setup-cloudwatch-alarms)
  - [9. Trigger the Step Function and lambda function](#7-trigger-the-step-function-and-lambda-function)
- [Conclusion](#conclusion)

## Introduction

This project is designed to demonstrate the integration of various AWS services to process real-time data streams. It includes the deployment of Lambda functions, creation of DynamoDB tables, configuration of Step Functions, and setting up monitoring with CloudWatch. The pipeline is designed to be scalable, fault-tolerant, and easy to manage.

## Prerequisites

Before proceeding with the setup, ensure you have the following:

- *AWS CLI*: Configured with appropriate permissions to manage AWS services.
- *Python 3.x*: Installed on your local machine.
- *Boto3*: AWS SDK for Python, installed via pip (pip install boto3).
- *IAM Role*: Created with the necessary permissions to execute Lambda functions, manage DynamoDB, S3, Step Functions, and CloudWatch.

## Project Structure

Here’s a breakdown of the project structure and the purpose of each file:

- aws_script.py: General setup tasks for AWS resources.
- create_step_function.py: Script to create and configure AWS Step Functions, defining the workflow of your processing pipeline.
- Creation_dynamodb_table.py: Script to create and configure DynamoDB tables required for storing processed data.
- deploy_processing_lambda.py: Script to package, deploy, and configure AWS Lambda functions that process s3 data to Dynamodb.
- deploy_lambda_function.py: Script to package, deploy and configure AWS Lambda function that process raw JSON data to s3.
- lambda_function.py: Entry point for the Lambda function to store data to s3.
- lambda_processing.py: Processing Logic to Handle the transfering of data from s3 to Dynamodb.
- payload.json: Sample payload to simulate triggering of the Step Function and Lambda Processing Function.
- sample_user_action_data.json: Sample data representing user actions, used for testing the pipeline.
- trigger_step_function.py: Script to manually trigger the Step Function using the sample payload.
- trigger_lambda_alarm.py: Script to set up CloudWatch alarms for monitoring Lambda functions and triggering notifications on errors or performance issues.

## Setup and Deployment Instructions

### 1. Setting AWS Environment

The first step is to create aws environment in the working machine. Setup a user in the IAM and get the user Access key and Security Key 

Run The Following Command :

 python3 aws_script.py        

 This will makesure that you have created AWS work ready environment and tells that you can succesfully access s3 bucket.

### 2. Create S3 Buckets

The next step is to create S3 buckets where data and Lambda deployment packages will be stored. Use the AWS CLI to create a new bucket:

Run The Following Command :

python3 Creation_of_s3.py


Replace your-bucket-name with a unique name for your bucket. S3 will be used for storing data input/output and Lambda deployment artifacts.

### 3. Create IAM Roles

AWS Lambda functions and Step Functions require IAM roles with specific permissions. Create a role with the following policies:

- *AWSLambdaBasicExecutionRole*: Allows Lambda functions to write logs to CloudWatch.
- *AmazonS3FullAccess*: Allows the Lambda functions to interact with S3.
- *DynamoDBFullAccess*: Allows Lambda to interact with DynamoDB tables.
- *StepFunctionsFullAccess*: Allows Lambda and Step Functions to execute workflows.

  Run The Following Command:

  python3 IAM_roles_lambda.py

Attach these policies to the IAM role, and note the ARN of the role, as it will be needed in the deployment scripts.

### 4. Deploy Lambda Functions for UserActivityControl

Use the deploy_lambda_function.py script to package and deploy your Lambda functions. This script will:

- Package the Lambda function code and dependencies.
- Upload the package to S3.
- Deploy the Lambda function and associate it with the created IAM role.

Run the following command:

bash
python deploy_lambda_function.py

Ensure that the S3 bucket name and IAM role ARN are correctly specified in the script.

After running the command use the below command to invoke the lambda function this will ensure to invoke the lambda function

aws lambda invoke --function-name UserActivityCollector output.txt (you can able to change function name and output will be seen in text format in same folder)

### 5. Create DynamoDB Tables

DynamoDB is used to store the processed data from the Lambda functions. Run the Creation_dynamodb_table.py script to create the necessary tables.

bash
python Creation_dynamodb_table.py


The script will define the schema for your tables, including the primary key and any secondary indexes required for querying.


### 6. Deploy Lambda Functions for UserActivityProcessingFunction

Use the deploy_processing_lambda.py script to package and deploy your Lambda functions. This script will:

- Package the Lambda function code and dependencies.
- Upload the data from  S3 to Dynamodb.
- Deploy the Lambda function and associate it with the created IAM role.

Run the following command:

bash
python deploy_processing_lambda.py

Ensure that the S3 bucket name and IAM role ARN are correctly specified in the script.

After running the command use the below command to invoke the lambda function this will ensure to invoke the lambda function
aws lambda invoke \                             
    --function-name UserActivityProcessingFunction \
    --payload file://payload.json \
    output.txt \
    --cli-binary-format raw-in-base64-out  ( the payload file will be used as triggering file for the lambda and output will be stored in text file)

### 7. Create and Configure Step Functions

Step Functions manage the workflow of your data processing pipeline. Run the create_step_function.py script to create and configure the state machine that orchestrates the Lambda functions.

bash
python create_step_function.py


This script will define the states, transitions, and error handling mechanisms for the pipeline. Ensure the Lambda function ARNs are correctly referenced in the state machine definition.

Below command used to start the step function and can able to monitor the funciton

aws stepfunctions start-execution \   
    --state-machine-arn arn:aws:states:us-east-1:211125559197:stateMachine:UserActivityTrackingStateMachine \
    --input file://payload.json

    aws stepfunctions describe-execution \
    --execution-arn  “( you can write execution arn number here)”

### 8. Setup CloudWatch Alarms

Monitoring is critical to ensure the smooth operation of your pipeline. The trigger_lambda_alarm.py script sets up CloudWatch alarms for your Lambda functions. These alarms monitor:

- Function execution errors.
- Execution duration exceeding a specified threshold.
- Invocation count anomalies.

Run the script as follows:
python3 create_lambda_alarms.py
python3 create_step_function_alarms.py
python3 create_cloud_dashboard.py
python3 create_cloud_monitor.py

these will create the lambda alarms and stepfunction alarms also it will create the cloud dashboard and monitor 

### 9. Trigger the Step Function and lambda functions

After setting up the infrastructure, you can trigger the Step Function manually or through an automated process. Use the trigger_step_function.py, triggering_lambda_alarms.py  script to trigger the Step Function and lambda function using a sample payload:

python3 trigger_step_function.py
python3 triggering_lambda_alarms.py

You can modify the payload.json file to simulate different scenarios and inputs for testing.

## Conclusion

This project demonstrates the setup of a real-time data processing pipeline using AWS services. By following the instructions provided, you should be able to deploy, monitor, and manage the pipeline effectively. The project can be extended by integrating more AWS services, adding error-handling mechanisms, or optimizing the Lambda functions for performance and cost.
