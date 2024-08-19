import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Describe EC2 instances
def describe_instances():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
            
            
# Create an EC2 instance
def create_instance():
    # Adjust the parameters as needed
    instance = ec2.run_instances(
        ImageId='ami-0427090fd1714168b',  # Use an appropriate AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='ec2-33'  # Replace with your key pair name
    )
    instance_id = instance['Instances'][0]['InstanceId']
    print(f"Created instance {instance_id}")
    

# Start an EC2 instance
def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}")
    

# Stop an EC2 instance
def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}")


# Main function to manage EC2 instances
def main():
    while True:
        print("\nChoose an option:")
        print("1. Describe instances")
        print("2. Create an instance")
        print("3. Stop an instance")
        print("4. Start an instance")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            describe_instances()
        elif choice == '2':
            create_instance()
        elif choice == '3':
            instance_id = input("Enter the Instance ID to stop: ")
            stop_instance(instance_id)
        elif choice == '4':
            instance_id = input("Enter the Instance ID to start: ")
            start_instance(instance_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
