import random

while True:
    sides = 20
    input("Type roll to roll the die!")
    result = random.randint(1, sides)
    print(result)