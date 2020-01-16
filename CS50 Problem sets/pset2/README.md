## Problem Set 2

Problem Set 2 included "caesar", "vigenere" and "crack"

Caesar is a program that takes a number as input that serves as a "key". It then takes text as another input and shifts each letter in the text according to the number specified by the key.

Vigenere builds upon caesar and takes text as a "key". Each letter in the key is then turned into a number according to its space in the alphabet.
The program then takes text as input, and shifts each letter by the number specified by the key. The first letter is shifted by the first number, the second letter by the second number etc.
The numbers in the key loop around if the text is longer than the key.

Crack was a program that was designed to crack passwords by "brute force". The hashes of passwords were provided, along with the function that hashed them.
The passwords had a max length of 6 characters.
