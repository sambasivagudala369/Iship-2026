# AWS Automation Project

This project focuses on automating and managing AWS EC2, S3, and RDS services using Python scripts within an AWS Cloud9 environment. The automation is performed using the Boto3 library, which is the official AWS SDK for Python.

## Overview

Managing AWS resources manually can be time-consuming and prone to errors, especially when dealing with multiple instances or services. This project aims to simplify the process by providing Python scripts that automate the creation, management, and termination of AWS EC2 instances, S3 buckets, and RDS databases. By using the Boto3 library within a Cloud9 environment, users can efficiently manage their AWS infrastructure with just a few lines of code.

The scripts are designed to be modular and customizable, allowing you to adjust parameters and settings to fit your specific use case. Whether you're managing a single instance or a complex infrastructure, this project provides a robust solution for AWS automation.


## Features

- **EC2 Management:** 
  - Launch and terminate EC2 instances.
  - Start and stop instances.
  - Retrieve information about instances, including instance IDs, and status.
  
- **S3 Management:**
  - Create and delete S3 buckets.
  - Upload, and delete objects in S3 buckets.
  - List all S3 buckets in your account.
  - Show all objects within a specific S3 bucket.

- **RDS Management:**
  - **Create and Modify RDS Instances:**
    - Create new RDS instances with customizable parameters such as instance class, storage, username, password, database engine and database engine version.
    - Modify existing RDS instances, including changing the instance class, storage capacity, and other configurations.
  - **Manage Databases Using CRUD Operations:**
    - Connect to an RDS database instance and perform Create, Read, Update, and Delete (CRUD) operations on the database.
    - Manage database schemas, tables, and data directly from the scripts.


## How It Works

1. **AWS Cloud9 Environment:**
   - The project runs in an AWS Cloud9 environment, providing a cloud-based IDE with AWS CLI and Python pre-configured.
   - Users can directly interact with AWS services via Boto3 without requiring local setup.

2. **Boto3 Integration:**
   - The scripts leverage Boto3, the AWS SDK for Python, to interact with AWS services programmatically.
   - Each script corresponds to a specific AWS service (EC2, S3, RDS) and includes functions for various operations.

3. **Modular Script Design:**
   - The scripts are modular, meaning you can easily extend or modify them to include additional AWS services or custom functionality.
   - Configuration options are included within the scripts to allow for easy customization of parameters like instance types, S3 bucket names, and RDS configurations.

## Configuring AWS Credentials

To use this script, you need to configure your AWS credentials in the Cloud9 environment. You can do this by creating a file named `~/.aws/credentials` with the following format:

```plaintext
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
