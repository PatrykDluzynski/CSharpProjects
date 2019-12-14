from sys import argv, exit
from cs50 import get_string

# Check if input is letters only, and check amount of args
if (argv[1].isalpha() == False) or len(argv) != 2:
    print("Usage: python vigenere.py k")
    exit(1)
# If everything is fine, assign argv[1] to key, and take the input from the user
else:
    original = get_string("plaintext: ")
    key = argv[1]
    # Also assign a variable to keep track of position in key
    keypos = 0
    print("ciphertext: ", end="")
    for c in original:
        # If a character is not a letter, just print it
        if c.isalpha() == False:
            print(c, end="")
        else:
            # Check if the position along the key matches the length of the key, and reset it if need be
            if keypos == len(key):
                keypos = 0
            # Get the lowercase version of the character and the letter in the key, subtracting 'a' to standardise the values
            # Add them together and take the mod
            # Add the 'a' back in to bring back the correct ascii value
            # Turn the result back into a character
            lowerc = ord(c.lower()) - ord('a')
            lowerkey = ord(key[keypos].lower()) - ord('a')
            char = chr(((lowerc + lowerkey) % 26) + ord('a'))
            # Move position along key to the next value
            keypos += 1
            # If c was uppercase, print it in uppercase and vice versa
            if c.isupper():
                print(char.upper(), end="")
            else:
                print(char.lower(), end="")
    # Print an empty space to move to next line
    print("")