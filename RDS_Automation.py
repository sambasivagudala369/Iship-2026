import boto3
import botocore
import pymysql  # Use pymysql for MySQL

# Create an RDS client
rds = boto3.client('rds')

# Connect to the RDS MySQL instance
def connect_to_rds(host, user, password, db_name):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

# Create a database within the RDS instance
def create_database(connection, db_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        connection.commit()
        print(f"Database {db_name} created successfully.")
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()




# Create the student table if it doesn't exist
def create_student_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            rollno VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            college VARCHAR(255) NOT NULL,
            branch VARCHAR(255) NOT NULL,
            age INT NOT NULL
        );
    """)
    connection.commit()
    cursor.close()

# Add a student record
def add_student(connection, rollno, name, college, branch, age):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO students (rollno, name, college, branch, age)
        VALUES (%s, %s, %s, %s, %s);
    """, (rollno, name, college, branch, age))
    connection.commit()
    cursor.close()

# Get all student records
def get_students(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT rollno, name, college, branch, age FROM students;")
    students = cursor.fetchall()
    cursor.close()
    return students

# Update a student record
def update_student(connection, rollno, name=None, college=None, branch=None, age=None):
    cursor = connection.cursor()
    query = "UPDATE students SET "
    params = []
    
    if name:
        query += "name = %s, "
        params.append(name)
    if college:
        query += "college = %s, "
        params.append(college)
    if branch:
        query += "branch = %s, "
        params.append(branch)
    if age is not None:
        query += "age = %s, "
        params.append(age)
    
    query = query.rstrip(', ')  # Remove trailing comma
    query += " WHERE rollno = %s;"
    params.append(rollno)
    
    cursor.execute(query, tuple(params))
    connection.commit()
    cursor.close()

# Delete a student record
def delete_student(connection, rollno):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE rollno = %s;", (rollno,))
    connection.commit()
    cursor.close()

# Display the current student records
def display_students(connection):
    print("\nStudent Records:")
    students = get_students(connection)
    for student in students:
        print(f"Roll No: {student[0]}, Name: {student[1]}, College: {student[2]}, Branch: {student[3]}, Age: {student[4]}")

# List RDS instances
def list_instances():
    try:
        response = rds.describe_db_instances()
        instances = response['DBInstances']
        if not instances:
            print("No RDS instances found.")
        else:
            for instance in instances:
                print(f"Instance ID: {instance['DBInstanceIdentifier']}, Status: {instance['DBInstanceStatus']}")
    except botocore.exceptions.ClientError as e:
        print(f"Error listing instances: {e}")

def create_instance(instance_id, db_instance_class, engine, engine_version, master_username, master_password):
    try:
        response = rds.create_db_instance(
            DBInstanceIdentifier=instance_id,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            EngineVersion=engine_version,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            AllocatedStorage=20  # Example storage size, you can change as needed
        )
        print(f"Creating RDS instance {instance_id}. Status: {response['DBInstance']['DBInstanceStatus']}")
    except botocore.exceptions.ClientError as e:
        print(f"Error creating instance: {e}")


# Modify an RDS instance
def modify_instance(instance_id, new_db_instance_class):
    try:
        response = rds.modify_db_instance(
            DBInstanceIdentifier=instance_id,
            DBInstanceClass=new_db_instance_class,
            ApplyImmediately=True
        )
        print(f"Modifying RDS instance {instance_id}. Status: {response['DBInstance']['DBInstanceStatus']}")
    except botocore.exceptions.ClientError as e:
        print(f"Error modifying instance: {e}")

# Delete an RDS instance
def delete_instance(instance_id):
    try:
        response = rds.delete_db_instance(
            DBInstanceIdentifier=instance_id,
            SkipFinalSnapshot=True  # Change to False if you want a final snapshot
        )
        print(f"Deleting RDS instance {instance_id}. Status: {response['DBInstance']['DBInstanceStatus']}")
    except botocore.exceptions.ClientError as e:
        print(f"Error deleting instance: {e}")

# Main function to manage RDS instances and student records
def main():
    while True:
        print("\nChoose an option:")
        print("1. List RDS instances")
        print("2. Create an RDS instance")
        print("3. Modify an RDS instance")
        print("4. Delete an RDS instance")
        print("5. Manage student records")
        print("6. Create a database in an RDS instance")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_instances()
        elif choice == '2':
            instance_id = input("Enter the instance ID to create: ")
            db_instance_class = input("Enter the DB instance class (e.g., db.t2.micro): ")
            engine = input("Enter the database engine (e.g., mysql): ")
            engine_version = input("Enter the database engine version (e.g., 8.0.35): ")
            master_username = input("Enter the master username: ")
            master_password = input("Enter the master password: ")
            create_instance(instance_id, db_instance_class, engine, engine_version, master_username, master_password)
        elif choice == '3':
            instance_id = input("Enter the instance ID to modify: ")
            new_db_instance_class = input("Enter the new DB instance class: ")
            modify_instance(instance_id, new_db_instance_class)
        elif choice == '4':
            instance_id = input("Enter the instance ID to delete: ")
            delete_instance(instance_id)
        elif choice == '5':
            host = input("Enter the database endpoint (host): ")
            user = input("Enter the master username: ")
            password = input("Enter the master password: ")
            db_name = input("Enter the database name: ")
            conn = connect_to_rds(host, user, password, db_name)
            create_student_table(conn)
            
            while True:
                print("\nStudent Records Management:")
                print("1. Add Student")
                print("2. Update Student Record")
                print("3. Delete Student")
                print("4. Display Students")
                print("5. Back to Main Menu")
                
                student_choice = input("Choose an option: ")
                
                if student_choice == '1':
                    rollno = input("Enter roll number: ")
                    name = input("Enter name: ")
                    college = input("Enter college: ")
                    branch = input("Enter branch: ")
                    age = int(input("Enter age: "))
                    add_student(conn, rollno, name, college, branch, age)
                elif student_choice == '2':
                    rollno = input("Enter roll number to update: ")
                    name = input("Enter new name (leave blank to keep current): ") or None
                    college = input("Enter new college (leave blank to keep current): ") or None
                    branch = input("Enter new branch (leave blank to keep current): ") or None
                    age = input("Enter new age (leave blank to keep current): ")
                    age = int(age) if age else None
                    update_student(conn, rollno, name, college, branch, age)
                elif student_choice == '3':
                    rollno = input("Enter roll number to delete: ")
                    delete_student(conn, rollno)
                elif student_choice == '4':
                    display_students(conn)
                elif student_choice == '5':
                    conn.close()
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '6':
            host = input("Enter the database endpoint (host): ")
            user = input("Enter the master username: ")
            password = input("Enter the master password: ")
            db_name = input("Enter the name of the database to create: ")
            conn = connect_to_rds(host, user, password, None)  # Connect without a specific database
            create_database(conn, db_name)
            conn.close()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
