import random

def combat():
        sides = 20
        input("Press enter to roll the die.")
        result = random.randint(1, sides)
        print(result)
        if result < 15:
            print("You sprint quickly towards the man and punch him in the face. He staggers backwards and gives you another oppurtunity to attack.")
        else:
            print("You die...")