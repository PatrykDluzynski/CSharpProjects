from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Splits input based on \n (new line) and creates a set
    # Sets can only have unique values in them so duplicates will get discarded automatically
    lista = set(a.split('\n'))
    listb = set(b.split('\n'))
    # Create a new set based on the common values in both sets
    listc = lista.intersection(listb)
    # Iterate over each common value and return it
    return [line for line in listc]


# The next two functions work on a similar principle to the first
def sentences(a, b):
    """Return sentences in both a and b"""

    lista = set(sent_tokenize(a, language='english'))
    listb = set(sent_tokenize(b, language='english'))
    listc = lista.intersection(listb)
    return [line for line in listc]


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    lista = set()
    # The range is set to the length of the input string
    for i in range(len(a)):
        # If the character position + the specified desired length would go past the end of the string, break the loop
        if i + n > len(a):
            break
        # Else add the substring consisting of the current character position up to the current position + specified length
        else:
            lista.add(a[i:i + n])

    listb = set()
    for i in range(len(b)):
        if i + n > len(b):
            break
        else:
            listb.add(b[i:i + n])

    listc = lista.intersection(listb)
    return [line for line in listc]