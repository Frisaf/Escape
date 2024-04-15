# Intro
name = input("Welcome to 'Unnamed'! Please enter your name to get started: ")
print("Great! Welcome", name,"! Let's get started!")

print("You wake up in an empty room. What happened? You don't remember. All you know is that you feel an immense pain in your head.")
print("Current objective: Find a way out of this place")
print("Tip: You will be presented with choices as you progress. Each choice will impact the story and your potential of getting out of this place.")
print()
print("There are three doors in front of you. All of them look identical, but your gut feeling tells you that only one of them will lead to the exit...")
print("Which door do you choose?")
print("All choices will be separated with '/'. Type the choice you want to make in the terminal.\nNOTE: You need to type exactly what it says in order for the game to register the choice as a valid one.")
print("Which door do you choose?\n1/2/3")

choices = input(">")

if choices == "1":
    print("You enter a plain room with the same grey stone walls as the last one. There is a lever at the back of the room. Do you pull it, or do you go back?")
    print("yes/no")
    print("Yes will pull the lever while no will make you go back to the previous room.")
    
    choices = input(">")
    if choices == "yes":
        print("You here the door slam shut behind you and a sound of water slowly filling the room you're currently standing in")