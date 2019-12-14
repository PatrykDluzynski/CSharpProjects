from cs50 import get_int

x = -1

while x < 0:
    x = get_int("Number: ")

original = str(x)
todouble = []
others = []

for i in range(len(original)):
    if i % 2 == 0:
        others.append(int(original[len(original) - 1 - i]))
    if i % 2 == 1:
        todouble.append(original[len(original) - 1 - i])


doubled = []
for i in range(len(todouble)):
    d = int(todouble[i]) * 2
    if d > 9:
        tmp = str(d)
        tmp1 = tmp[0]
        tmp2 = tmp[1]
        doubled.append(int(tmp1) + int(tmp2))
    else:
        doubled.append(d)

summed = 0

for i in range(len(doubled)):
    summed += doubled[i]

for i in range(len(others)):
    summed += others[i]

if summed % 10 == 0:
    firstnum = original[0] + original[1]
    if len(original) == 15 and ((firstnum == "34") or (firstnum == "37")):
        print("AMEX")
    elif (len(original) == 13 or len(original) == 16) and original[0] == "4":
        print("VISA")
    elif len(original) == 16 and (firstnum =="51" or firstnum == "52" or firstnum == "53" or firstnum == "54" or firstnum == "55"):
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")
