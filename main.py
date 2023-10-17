import hashlib
import getpass

# Hash passwords using MD5
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

''' 
config file: users.csv
Columns: username, password_hash, user_type, privilege_level

user_type: patient, doctor, nurse, receptionist, pharmacist, lab technician
privilage_level: 
    patient: 0
    doctor: 1
    nurse: 2
    receptionist: 3
    pharmacist: 4
    lab technician: 5
'''
'''
config file: patientdata.csv
Columns: name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions

Each data record is associated with a sensitivity level depending on its nature.

'''
def register():
    print("\n#### Registration section ####")
    username = input("Username: ").strip()

    # Todo - Check whether username already exists 


    print("\nSelect the user type:\n1-Patient\n2-Hospital staff\n")
    user_type = input("Your type:")

    if user_type == "1":
        user_type = "patient"
        privilage_level = "0"
    
    elif user_type == "2":
        # Varification codes for staff types has been used for improved security.
        varification_codes = { "1": "doc111", 
                              "2": "nur222", 
                              "3": "rec333", 
                              "4": "pha444", 
                              "5": "lab555" }
        
        print("\nSelect staff type:\n1-Doctor\n2-Nurse\n3-Receptionist\n4-Pharmacist\n5-Lab technician\n")
        staff_type = input("Your type:").strip()
        code = input("\nEnter the varification code:")

        
        if code == varification_codes[staff_type]:
                if staff_type == "1":
                    user_type = "doctor"
                    privilage_level = "1"
                elif staff_type == "2":
                    user_type = "nurse"
                    privilage_level = "2"
                elif staff_type == "3":
                    user_type = "receptionist"
                    privilage_level = "3"
                elif staff_type == "4":
                    user_type = "pharmacist"
                    privilage_level = "4"
                elif staff_type == "5":
                    user_type = "lab technician"
                    privilage_level = "5"
                else:
                    print("Invalid input for the staff type. Please check again.")
                    return
        else: 
            print("Varification code is worng. Please check again.")
            return
    else:
        print("Invalid input for the user type. Please check again.")
        return
        
    # Password configuration
    while True:
        # password = input("\nPassword: ").strip()
        # Password that user input will be hidden using the getpass library for improved secriuty.
        password = getpass.getpass("\nPassword: ")

        # Password should be at least 8 characters for enhanced security.
        if len(password) < 8:
            print("Password should be at least 8 characters. Re-enter password.")
        else:
            # confirm_password = input("Confirm password: ").strip()
            # Password that user input will be hidden using the getpass library for improved secriuty.
            confirm_password = getpass.getpass("Confirm password: ")

            if password != confirm_password:
                print("Passwords do not match. Re-enter password.")
            else:
                break

    # Write user data to configuration file
    with open('users.csv', mode='a') as file:
        file.write(f"{username},{hash_password(password)},{user_type},{privilage_level}\n")

    print("\nRegistration successful.")

def patient_session(username):
    print(f"### Welcome {username}! ###")
    while True:
        print("\nSelect the option related to your functionality:\n1-View personal details\n2-View sickness details\n3-View drug prescriptions\n4-View lab test prescriptions\n5-Log out\n")
        option = input("Your input:")
        if option == '1':
            print("Personal details")
        elif option == '2':
            print("Sickness details")
        elif option == '3':
            print("Drug prescriptions")
        elif option == '4':
            print("Lab test prescriptions")
        elif option == '5':
            print("Logging out...")
            break


def login():
    while True:
        print("\n#### Login Section ####")
        
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        # Read user data from configuration file
        with open('users.csv', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                # test: print (fields)
                if fields[0] == username and fields[1] == hash_password(password):
                    print("Login successful.\n")
                    user_type = fields[2]
                    privilage_level = fields[3]     

                    if user_type == "patient":
                        patient_session(username)               
                    break
            else:
                print("Login failed. Please check username and password.")
    


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
    print("Please select the option related to your functionality:\n1-Register\n2-Log in\n3-Log out\n")

    option = input("Your input:")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Wrong input..Please check again and enter the number related to your option")