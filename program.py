import hashlib

# Hash passwords using MD5
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Write user data to configuration file
def write_config_file(users):
    with open('userdata.csv', mode='w') as file:
        file.write('username,password_hash,user_type,privilege_level\n')
        for user in users:
            file.write(f"{user['username']},{hash_password(user['password'])},{user['user_type']},{user['privilege_level']}\n")
    print('Configuration file written successfully.')

# Read user data from configuration file
def read_config_file():
    users = []
    with open('userdata.csv', mode='r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            fields = line.strip().split(',')
            user = {}
            user['username'] = fields[0]
            user['password'] = fields[1]
            user['user_type'] = fields[2]
            user['privilege_level'] = fields[3]
            users.append(user)
    return users

# sample user data
users = [
    {'username': 'john', 'password': 'password123', 'user_type': 'patient', 'privilege_level': '1'},
    {'username': 'jane', 'password': 'password456', 'user_type': 'staff', 'privilege_level': '2'}
]

# write user data to configuration file
write_config_file(users)

# read user data from configuration file
users = read_config_file()
print(users)