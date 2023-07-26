#this file was used to test smaller blocks of code to later be implemented into the larger project
print("Enter the message that you would like to send")
message_check = True
while (message_check):
    message = input("> ")
    print("the message is: " + message)
    print("is the message correct? (Y/N)") #if !N continue
    message_confirm = input("> ")
    print(message_confirm)
    if message_confirm == 'N' or message_confirm == 'n':
        print("if 1")
        print("please re-enter your message")
    elif message_confirm == 'n':
        print("if 2")
        print("please re-enter your message")
    else:
        print("else")
        message_check = False
