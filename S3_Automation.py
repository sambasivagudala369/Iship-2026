import boto3
import os
import botocore

# Create an S3 client
s3 = boto3.client('s3')

# List S3 buckets
def list_buckets():
    response = s3.list_buckets()
    buckets = response['Buckets']
    if len(buckets) == 0:
        print("No buckets are available.")
    else:
        print("Existing buckets:")
        for bucket in buckets:
            print(f"  {bucket['Name']}")

# Create an S3 bucket
def create_bucket(bucket_name, region=None):
    # Create S3 client with the specified region
    if region is None:
        s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', region_name=region)
    
    try:
        if region is None or region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket {bucket_name} created successfully.")
    except botocore.exceptions.ClientError as e:
        print(f"Error creating bucket: {e}")

# Upload a file to an S3 bucket
def upload_file(bucket_name, file_path):
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, file_name)
    print(f"File {file_path} uploaded to bucket {bucket_name} as {file_name}")


# Delete a file from an S3 bucket
def delete_file(bucket_name, file_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"File {file_name} deleted from bucket {bucket_name}")
    except botocore.exceptions.ClientError as e:
        print(f"Error deleting file: {e}")


# Delete an S3 bucket
def delete_bucket(bucket_name):
    s3.delete_bucket(Bucket=bucket_name)
    print(f"Bucket {bucket_name} deleted")
# Main function to manage S3 buckets
def main():
    while True:
        print("\nChoose an option:")
        print("1. List buckets")
        print("2. Create a bucket")
        print("3. Upload a file")
        print("4. Delete a file")
        print("5. Delete a bucket")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_buckets()
        elif choice == '2':
            bucket_name = input("Enter the name of the bucket to create: ")
            region = input("Enter the AWS region (leave blank for us-east-1): ").strip() or None
            create_bucket(bucket_name, region)
        elif choice == '3':
            bucket_name = input("Enter the name of the bucket to upload to: ")
            file_path = input("Enter the path of the file to upload: ")
            upload_file(bucket_name, file_path)
        elif choice == '4':
            bucket_name = input("Enter the name of the bucket to delete from: ")
            file_name = input("Enter the name of the file to delete: ")
            delete_file(bucket_name, file_name)
        elif choice == '5':
            bucket_name = input("Enter the name of the bucket to delete: ")
            delete_bucket(bucket_name)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
