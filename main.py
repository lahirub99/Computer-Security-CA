print("Select the number related to the functionality")
while True:
    print("1-register\n2-login\n3-exit")
    option = input("Your input:")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Wrong input..Please check again")