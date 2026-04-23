# Personal Introduction Program
# This program collects user details and displays a welcome message

# Taking user input
name = input("What is your name? ")
age = input("How old are you? ")
hobby = input("What is your favorite hobby? ")

# Displaying formatted output
print("\n Welcome {}!".format(name))
print(f"You are {age} years old and love {hobby}.")