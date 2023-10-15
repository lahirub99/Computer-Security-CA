import hashlib

# Hash passwords using MD5
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

''' 
config file: users.csv
Columns: username, password_hash, user_type, privilege_level
'''
'''
config file: patientdata.csv
Columns: name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions
'''
def register():
    print("\n#### Registration section ####")
    username = input("Username: ").strip()

    print("\nSelect the user type:\n1-Patient\n2-Hospital staff\n")
    user_type = input("Your type:")

    if user_type == "1":
        user_type = "patient"
        privilage_level = "0"
    
    # Password configuration
    while True:
        password = input("Password: ").strip()
        # Password should be at least 8 characters for enhanced security.
        if len(password) < 8:
            print("Password should be at least 8 characters. Re-enter password.")
        else:
            confirm_password = input("Confirm password: ").strip()
            if password != confirm_password:
                print("Passwords do not match. Re-enter password.")
            else:
                break

    # Write user data to configuration file
    with open('users.csv', mode='a') as file:
        file.write(f"{username},{hash_password(password)},{user_type},{privilage_level}\n")

    print("\nRegistration successful.")




def login():
    username = input("Username: ")
    password = input("Password: ")

    # if authenticate_user(username, password, users):
    #     print(f"Welcome, {username}!")
    #     privilege_level = users[username]["privilege_level"]

    #     if users[username]["user_type"] == "patient":
    #         print("You are a patient and can view your data.")
    #         data_records = read_data_records(data_filename, username, privilege_level)
    #         for record in data_records:
    #             print(", ".join(record))
    #     else:
    #         print("You are a hospital staff member.")
    #         if privilege_level == "high":
    #             print("You have high privileges and can read/write all data.")
    #         else:
    #             print("You have limited privileges and can read data for patients.")

    #         action = input("Do you want to write data? (yes/no): ")
    #         if action.lower() == "yes":
    #             personal_details = input("Enter personal details: ")
    #             sickness_details = input("Enter sickness details: ")
    #             drug_prescriptions = input("Enter drug prescriptions: ")
    #             lab_test_prescriptions = input("Enter lab test prescriptions: ")
    #             write_data_record(data_filename, username, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions)
    #             print("Data written successfully.")

    # else:
    #     print("Authentication failed. Please check your username and password.")



''' There are two main user types such as patients and hospital staff.  
Each user has three functionalities. (Assumed that patients can register themselves without going to the registration desk.)
1. Register
2. Log in
3. Log out
'''
print("*** Welcome! ***")
while True:
    # user_type = input("Please select the user type (patient/staff):").strip().lower()
    # if user_type == "patient":
    print("\nPlease select the option related to your functionality:\n1-Register\n2-Log in\n3-Log out\n")

    option = input("Your input:")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Wrong input..Please check again and enter the number related to your option")