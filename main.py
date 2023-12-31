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
Columns: patient_id,name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions

Each data record is associated with a sensitivity level depending on its nature.
Each data record is due to an encounter with a patient.
Hospital staff can read or write data based on account privilege level and sensitivity level of data

*** Privilege_levels ***:
The privilege level of a user is defined as a number.
The user types whose privileges are included in this number have read/write access to the data corresponding to that privilege level.
    privilege_level     user_type
    0:                  patient
    1:                  doctor
    2:                  nurse
    3:                  receptionist
    4:                  pharmacist
    5:                  lab technician

*** Sensitivity_levels ***:
Sensitivity levels for data record creation are hardcoded in the program and they cannot be manually changed. They are as follows.
- Only Patient and Receptionist data type can create/edit personal details data records.
- Only Doctor data type can create/edit sickness details data records.
- Only Pharmacist, and Doctor data can create/edit drug prescription data records.
- Only Lab Technician data types can create/edit lab test prescription data records.

As mentioned above each data record is associated with read and write (i.e. view and edit) sensitivities separately. 
These sensitivities are assigned when a new record is created. 

A patients can only read their own data records.
# It's assumed that all staff types can read all data records for smooth operation of the hospital system.

A sensitivity level is defined as a sequence of numbers. Each number represents a different privilege type. 
The user types whose privileges are included in this number sequence have read/write access to the data corresponding to that sensitivity level. Consider the ordering of the sequence does not matter.

Therefore, sensitivities are as follows according to number sequence representation
Data type               - Read Sensitivity  - Write Sensitivity
Patient ID              - “012345”          - “”
Name                    - “012345”          - “03”
Personal Details	    - “012345”          - “03”
Sickness Details	    - “012345”          - “12”
Drug Prescription	    - “012345”          - “14”
Lab Test Prescription	- “012345”          - “5”

When a certain functionality is trying to read or write data, the system checks the privilege of the user who is trying to perform the execution. If they are not compatible system will send a “not authorized” message and the system will output which user type to contact to complete the operation.

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
        
    # If the registered person was a patient, a new row should be opened int 'patientdata.csv' to store the patient's data
    # When the registration of a patient is done, a new entry will be added to the patientdata.csv file with only the patient ID and the name.
    # Newly registered patient's ID is the will be a string such that, 'P' + the number with a one increment of the previous patient.
    # Example: If the last patient ID is P003, the new patient ID will be P004.
    if user_type == "patient":
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            if len(lines) == 0:
                new_patient_id = 'P001'
            else:
                last_patient_id = lines[-1].split(',')[0]
                new_patient_id = 'P' + str(int(last_patient_id[1:]) + 1).zfill(3)
        with open('patientdata.csv', mode='a') as file:
            # Only the patient ID and the name will be added to the patientdata.csv file and the rest of the fields will be left blank.
            file.write(f"{new_patient_id},{username},,,,\n")

    print("\nRegistration successful.")

    # When the registration is done, the user is automatically logged in to the system.
    if user_type == "patient":
        patient_session(username)
        return
    else:
        staff_session(username, privilage_level)
        return
    
    

''' Returns the privilage level of a given username.'''
def get_privilage_level(username):
    with open('users.csv', mode='r') as file:
        lines = file.readlines()
        for line in lines:
            fields = line.strip().split(',')
            if fields[0] == username:
                privilage_level = fields[3]
                break
        else:
            return -1
        return privilage_level


def edit_personal_details(privilage_level, patient_identifier):
    if privilage_level == '0' or privilage_level == '3':
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_identifier or fields[1] == patient_identifier:
                    personal_details = fields[2]
                    break
            else:
                print("Patient not found. Please check patient ID again.")
                return
        # Edit personal details 
        if personal_details == "":
            print("Current personal details: None")
        else:
            print(f"Current personal details: {personal_details}")
        new_personal_details = input("Enter new personal details: ")
        # Update the relevant row in the patientdata.csv file
        # Add the new personal details to the existing personal details
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            # updated_data is the variable that stores the data to be written to the updated patientdata.csv file
            updated_data = ""
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_identifier or fields[1] == patient_identifier:
                    # fields of patienddata.csv file: patient_id,name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions
                    # fields[2] = personal_details + new_personal_details
                    fields[2] = new_personal_details
                    # Update the data
                    updated_data += ','.join(fields) + '\n'
                    # Todo - Optimize the code to break the loop after the relevant row is found and use the upcoming lines as it is to update.

                else:
                    updated_data += line
        # write the updated data in the patientdat.csv file
        with open('patientdata.csv', mode='w') as file:
            file.write(updated_data)
        print("Personal details updated successfully.")
    else:
        print("Sorry, you are not authorized to edit personal details.")
    return


def edit_sickness_details(privilage_level, patient_id):
    if privilage_level == '1' or privilage_level == '2':
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    sickness_details = fields[3]
                    break
            else:
                print("Patient not found. Please check patient ID again.")
                return
        # Edit sickness details
        if sickness_details == "":
            print("Current sickness details: None")
        else:
            print(f"Current sickness details: {sickness_details}")
        new_sickness_details = input("Enter new sickness details: ")
        # Update the relevant row in the patientdata.csv file
        # Add the new sickness details to the existing sickness details
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            # updated_data is the variable that stores the data to be written to the updated patientdata.csv file
            updated_data = ""
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    # fields of patienddata.csv file: patient_id,name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions
                    # fields[3] = sickness_details + new_sickness_details
                    fields[3] = new_sickness_details
                    # Update the data
                    updated_data += ','.join(fields) + '\n'
                    # Todo - Optimize the code to break the loop after the relevant row is found and use the upcoming lines as it is to update.

                else:
                    updated_data += line

        # write the updated data in the patientdat.csv file
        with open('patientdata.csv', mode='w') as file:
            file.write(updated_data)
        print("Sickness details updated successfully.")
    else:
        print("Sorry, you are not authorized to edit sickness details.")
    return

def edit_drug_prescriptions(privilage_level, patient_id):
    if privilage_level == '1' or privilage_level == '4':
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    drug_prescriptions = fields[4]
                    break
            else:
                print("Patient not found. Please check patient ID again.")
                return
        # Edit drug prescriptions
        if drug_prescriptions == "":
            print("Current drug prescriptions: None")
        else:
            print(f"Current drug prescriptions: {drug_prescriptions}")
        new_drug_prescriptions = input("Enter new drug prescriptions: ")
        # Update the relevant row in the patientdata.csv file
        # Add the new drug prescriptions to the existing drug prescriptions
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            # updated_data is the variable that stores the data to be written to the updated patientdata.csv file
            updated_data = ""
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    # fields of patienddata.csv file: patient_id,name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions
                    # fields[4] = drug_prescriptions + new_drug_prescriptions
                    fields[4] = new_drug_prescriptions
                    # Update the data
                    updated_data += ','.join(fields) + '\n'
                    # Todo - Optimize the code to break the loop after the relevant row is found and use the upcoming lines as it is to update.

                else:
                    updated_data += line
        
        # write the updated data in the patientdat.csv file
        with open('patientdata.csv', mode='w') as file:
            file.write(updated_data)
        print("Drug prescriptions updated successfully.")
    else:
        print("Sorry, you are not authorized to edit drug prescriptions.")
    return

def edit_lab_test_prescriptions(privilage_level, patient_id):
    if privilage_level == '5':
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    lab_test_prescriptions = fields[5]
                    break
            else:
                print("Patient not found. Please check patient ID again.")
                return
        # Edit lab test prescriptions
        if lab_test_prescriptions == "":
            print("Current lab test prescriptions: None")
        else:
            print(f"Current lab test prescriptions: {lab_test_prescriptions}")
        new_lab_test_prescriptions = input("Enter new lab test prescriptions: ")
        # Update the relevant row in the patientdata.csv file
        # Add the new lab test prescriptions to the existing lab test prescriptions
        with open('patientdata.csv', mode='r') as file:
            lines = file.readlines()
            # updated_data is the variable that stores the data to be written to the updated patientdata.csv file
            updated_data = ""
            for line in lines:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    # fields of patienddata.csv file: patient_id,name, personal_details, sickness_details, drug_prescriptions, lab_test_prescriptions
                    # fields[5] = lab_test_prescriptions + new_lab_test_prescriptions
                    fields[5] = new_lab_test_prescriptions
                    # Update the data
                    updated_data += ','.join(fields) + '\n'
                    # Todo - Optimize the code to break the loop after the relevant row is found and use the upcoming lines as it is to update.

                else:
                    updated_data += line

        # write the updated data in the patientdat.csv file
        with open('patientdata.csv', mode='w') as file:
            file.write(updated_data)
        print("Lab test prescriptions updated successfully.")
    else:
        print("Sorry, you are not authorized to edit lab test prescriptions.")
    return

''' 
This is the fuction for view details of a specific patient using the username.
It fetches the data from the patientdata.csv file and prints the relavent data in a report format. 
Identifier can be either the patient ID or the patient name. 
When a patient is requesting his her own report, the identifier will be the username. 
Similarly when a staff is requesting a patient's report, the identifier will be the patient ID.
'''
def view_patient_report(identifier):
    with open('patientdata.csv', mode='r') as file:
        lines = file.readlines()
        for line in lines:
            fields = line.strip().split(',')
            if fields[1] == identifier or fields[0] == identifier:
                username = fields[1]
                personal_details = fields[2]
                sickness_details = fields[3]
                drug_prescriptions = fields[4]
                lab_test_prescriptions = fields[5]
                break
        else:
            print("Patient not found. Please check identifier again.")
            return
        # Generate report
        print("\n### Patient Details ###")
        print(f"Username: {username}")
        print(f"Personal Details: {personal_details}")
        print(f"Sickness Details: {sickness_details}")
        print(f"Drug Prescriptions: {drug_prescriptions}")
        print(f"Lab Test Prescriptions: {lab_test_prescriptions}")
        return
    

def patient_session(username):
    print(f"### Welcome {username}! ###")
    #view_patient_report(username)
    while True:
        print("\nSelect the option related to your functionality:\n1-View my report\n2-Edit personal details\n3-Log out")
        option = input("Your input:")
        if option == '1':
            view_patient_report(username)
        elif option == '2':
            edit_personal_details(get_privilage_level(username), username)
        elif option == '3':
            print("Logging out...\n")
            break



def staff_session(username, privilage_level):
    print(f"### Welcome {username}! ###")
    while True:
        print("\nSelect the option related to your functionality:\n1-View a patient's report\n2-Edit patient's personal details\n3-Edit sickness details\n4-Edit drug prescritions\n5-Edit lab reports\n6-Log out\n")
        option = input("Your input:")
        if option == '1':
            patient_id = input("Enter patient ID:")
            view_patient_report(patient_id)
        elif option == '2':
            patient_id = input("Enter patient ID:")
            edit_personal_details(privilage_level, patient_id)
        elif option == '3':
            patient_id = input("Enter patient ID:")
            edit_sickness_details(privilage_level, patient_id)
        elif option == '4':
            patient_id = input("Enter patient ID:")
            edit_drug_prescriptions(privilage_level, patient_id)
        elif option == '5':
            patient_id = input("Enter patient ID:")
            edit_lab_test_prescriptions(privilage_level, patient_id)
        elif option == '6':
            print("Logging out...\n")
            break
        else:
            print("Wrong input..Please check again and enter the number related to your option\n")



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
                    else:
                        staff_session(username, privilage_level)             
                    return
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
    print("MAIN MENU:\n1-Register\n2-Log in\n3-Exit\n")

    option = input("Your input:")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Wrong input..Please check again and enter the number related to your option\n")