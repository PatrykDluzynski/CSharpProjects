from cs50 import get_string
from sys import argv, exit


def main():
    # Check if the correct amount of args is used
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # Open the txt file and iterate over every word adding it to the set with \n stripped away
    with open(argv[1], 'r') as file:
        bannedlist = {word.strip('\n') for word in file}

    # Get the message and split it into individual words
    tocensor = get_string(f"What message would you like to censor?\n")
    wordlist = tocensor.split()

    # Iterate over the words
    for word in wordlist:
        # Turn it to lowercase and check if it's in the list
        if word.lower() not in bannedlist:
            # Print if not in list
            print(word, end=" ")
        elif word.lower() in bannedlist:
            for c in word:
                # Turn to * if in list and add a space after it
                print("*", end="")
            print(" ", end="")
    print("")


if __name__ == "__main__":
    main()
