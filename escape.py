import random

YELLOW = "\033[33m"
RED    = "\033[31m"
GREEN  = "\033[32m"
RESET  = "\033[0m"

user_name = input(f"{YELLOW}Welcome to 'Escape!'! Let's start with your name, traveller.\nWhat's your name? {RESET}")
print(f"{YELLOW}Great! Welcome, {user_name}! Before we start the game, there are a few things that you need to know.\nFirst of all, there are two types of commands: interact and move. The interact command will make you interact with things in the room. For example, if you want to interact with the apple you would type 'interact apple' in the terminal and if you want to move right you would type 'move right' in the terminal. Moving backwards will always lead you to the previous room if nothing else is stated.\nBut with that, let's move on with the game, shall we?{RESET}")
print("")
print("You wake up on a dusty room. You don't remember what happened last night. How did you even end up here? All you know is that you have to get out, and that fast.")

class Location:
    def __init__(self, name, description, directions):
        self.name = name
        self.description = description
        self.directions = directions

locations = {
    ### STARTER ROOMS ###
    "the Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked.", {"right": "Room one", "left": "Room two"}),
    "Room one": Location("Room one", "From what you can see the room is empty, with black and cold stone walls on all four sides. However, there is a lever on your right side.", {"backwards": "the Door room"}),
    "Room two": Location("Room two", "The room is lit up with a torch and there is a table at the middle of the room. On the table, there is a letter.", {"backwards": "the Door room"}),
    "the second Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked. You also see something right ahead of you that was not there before: an opening in the wall.", {"right": "Room one", "left": "Room two", "forwards": "Hidden room"}),
    "Hidden room": Location("the Hidden room", "The room is dark, and you barely see a thing. From what you can tell, the 'room' consists of a corridor of which you cannot see the end of.", {"forwards": "Corridor", "backwards": "the second Door room"}),
    "Corridor": Location("the corridor", "The corridor is barely lit up and you cannot see much. As you continue walking, you reach a point where the corridor splits in two. One way goes left and the other goes right.", {"backwards": "Hidden room", "right": "Puzzle room", "left": "Wizard room"}),
    "Puzzle room": Location("the Puzzle room", "You turn right and reach a room well lit up with torches on the wall. On the floor, there are tiles in different shapes. The tiles are placed in a six by six grid, and your gut feeling tells you that one step in the wrong direction can lead to death. There is a skeleton at the middle of the room. Right ahead of you is a door, but you need to reach it first. There is also a sheet of paper on the floor.", {"forwards": "Correct tile 1", "backwards": "Corridor"}), # SAVE LOCATION
    "Final door": Location("the door", "You successfully finished the puzzle, and managed to not end up like the unlucky guy at the middle of the room.\n\nThe door in front of you is closed.", {"backwards": "Correct tile 16"}),
    "Final door opened": Location("You walk thorugh the door and proceed to climb the stairs.", f"As you walk, you start to smell the wonderful smell of grass, and forest, and nature. You are only one step from freedom. One more step. Now you are free.\n\n{YELLOW}CONGRATULATIONS {user_name}! You completed the game! Did you know there are more than one ending? Play the game again to find out how it could also have ended...{RESET}", {}),
    ### PUZZLE ROOM ITEMS ###
    "Correct tile 1": Location("a new tile", "", {"forwards": "Correct tile 2", "right": "Death", "left": "Death", "backwards": "Puzzle room"}),
    "Correct tile 2": Location("a new tile", "The skeleton is right in front of you.", {"forwards": "Death", "right": "Death", "left": "Correct tile 3", "backwards": "Correct tile 1"}),
    "Correct tile 3": Location("a new tile", "", {"forwards": "Death", "right": "Correct tile 4", "left": "Death", "backwards": "Correct tile 2"}),
    "Correct tile 4": Location("a new tile", "The skeleton is on your right hand side.", {"forwards": "Correct tile 5", "right": "Death", "left": "Death", "backwards": "Correct tile 3"}),
    "Correct tile 5": Location("a new tile", "", {"forwards": "Death", "right": "Correct tile 6", "left": "Death", "backwards": "Correct tile 4"}),
    "Correct tile 6": Location("a new tile", "The skeleton is on your right hand side.", {"forwards": "Correct tile 7", "right": "Death", "left": "Death", "backwards": "Correct tile 5"}),
    "Correct tile 7": Location("a new tile", "", {"forwards": "Death", "right": "Correct tile 8", "left": "Death", "backwards": "Correct tile 6"}),
    "Correct tile 8": Location("a new tile", "", {"forwards": "Death", "right": "Death", "left": "Correct tile 9", "backwards": "Correct tile 7"}),
    "Correct tile 9": Location("a new tile", "", {"forwards": "Correct tile 10", "right": "Death", "left": "Death", "backwards": "Correct tile 8"}),
    "Correct tile 10": Location("a new tile", "", {"right": "Death", "left": "Correct tile 11", "backwards": "Correct tile 9"}),
    "Correct tile 11": Location("a new tile", "", {"forwards": "Correct tile 12", "left": "Death", "backwards": "Correct tile 10"}),
    "Correct tile 12": Location("a new tile", "", {"forwards": "Death", "left": "Correct tile 13", "backwards": "Correct tile 11"}),
    "Correct tile 13": Location("a new tile", "", {"forwards": "Death", "right": "Correct tile 14", "left": "Death", "backwards": "Correct tile 12"}),
    "Correct tile 14": Location("a new tile", "", {"forwards": "Death", "left": "Correct tile 15", "backwards": "Correct tile 13"}),
    "Correct tile 15": Location("a new tile", "", {"forwards": "Correct tile 16", "left": "Death", "backwards": "Correct tile 14"}),
    "Correct tile 16": Location("a new tile", "", {"forwards": "Death", "right": "Final door", "left": "Death", "backwards": "Correct tile 15"}),
    ### WIZARD ROOM ITEMS ###
    "Wizard room": Location("the left", f"As you continue to walk in that direction, you eventually reach a small but well lit room. There are vials and papers spread all around the tables that stand alongside the walls, and in the middle stands a tall man with a long gray beard. He is wearing a long purple robe that almost touches the ground and there is a tall, cone shaped hat on his head.\n'Oh great', the man says. 'I've waited for someone new to step into my dungeon... Or I mean, you want to get out of here, don't you?'\n\n{RED}NARRATOR:{RESET} {YELLOW}You have two choices here: yes or no. Type 'interact yes' or 'interact no' in your terminal to continue. If you don't want to encounter this man just yet, you can type 'move backwards' to go back to the crossroad.{RESET}", {"yes": "Answer yes", "no": "Answer no", "backwards": "Corridor"}),
    ### DEATH ###
    "Death": Location("a new tile", f"You hear a sudden click and then a loud bang. Then, everything turns black...\n{YELLOW}GAME OVER! Type 'move backwards' to restart from the last save location.{RESET}", {"backwards": "Puzzle room"})
}

class Traveller:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, direction):
        if direction in self.current_location.directions:
            next_location_name = self.current_location.directions[direction]
            next_location = locations[next_location_name]
            self.current_location = next_location
            print(f"You walk to {next_location.name}")
        else:
            print("You cannot go that way...")
    
    def interact(self, item_name):
        if item_name == "lever":
            while True:
                print("You pull the lever and hear a large thud somewhere else...")
                choice = input("What do you want to do? ")
                if choice == "move backwards":
                    secret_room()
                    break
                else:
                    print("You cannot do that...")
        elif item_name == "letter":
            print("You pick up the letter and start to read:\nIt's been weeks, no ages since I last slept. If you read this, you need to leave now. This place is driving me insane. I haven't figured out the way out yet, but I think it has something to do with the lever in the other room...")

        elif item_name == "door":
            while True:
                print("You carefully turn the door knob and the door opens with a squeeking noise. There is now a long stair case in front of you. As you look at the top, you catch a glimpse of green grass.")
                choice = input("What do you want to do? ")
                if choice == "move forwards":
                    good_end()
                    break
                else:
                    print("You cannot do that...")
        
        elif item_name == "paper":
            print("You pick up the paper, and you see that it seems to contain a map of some sort.")
            print(f"""\
                  {RED}
            |---|---|---|---|---|---|
            |   |   |   |   |   |   |
            |---|---|---|---|---|---|
            |   | x | x | x |   |   |
            |---|---|---|---|---|---|
       -->  | x | x | O | x |   | x | -->
            |---|---|---|---|---|---|
            |   |   | x | x |   | x |
            |---|---|---|---|---|---|
            |   |   | x |   | x | x |
            |---|---|---|---|---|---|
            |   |   | x | x | x |   |
            |---|---|---|---|---|---|
                {RESET}
                """)
            
        elif item_name == "yes":
            while True:
                print("You walk to the man and say:\n'Yes, I really want to get out of here. Do you know where the exit is?'\nThe man looks at you, and it looks like he is on the verge to laughing.\n'You fool!' he says. 'Did you really think I, the great wizard Magico would let such a precious human escape? No, you came here for a reason, and that reason is to serve me forever!'\n\nThe Wizard initiates a fight! You will go through five rounds where you roll a d20. Every round will become progressively harder. If you lose more than two rounds in a row you are dead!")
                combat()

        elif item_name == "no":
            death_end()

def good_end():
    player = Traveller(locations["Final door opened"])
    print(player.current_location.name)
    print(player.current_location.description)

def death_end():
    print(f"You walk to the man and say:\n'No, I would like to stay here and explore a little more. This dungeon was actually pretty interesting.'\nThe man looks at you, and he seems happy with your answer. He chuckles.\n'Good. Why don't you stay forever then?'\nBefore you know it, the man has cast a spell upon you, and everything after that is incredibly foggy...\n\n{RED}YOU COMPLETED THE GAME!{YELLOW} Good job, {user_name}, you completed the game. But to what cost? Did you know that there are several endings. Play again to find out what the other ones are...{RESET}")
    
def secret_room():
    player = Traveller(locations["the second Door room"])
    print("You walk to the Door room.")

    while True:
        print(player.current_location.description)
        command = input("What do you want to do? ")

        if command.startswith("move"):
            try:
                direction = command.split()[1]
                player.move(direction)
            except IndexError:
                print("That is not a valid command. Did you perhaps have a typo?")
        elif command.startswith("interact"):
            try:
                item = command.split()[1]
                player.interact(item)
            except IndexError:
                print("That is not a valid command. Did you perhaps have a typo?")
        else:
            print("You cannot do that...")

def starter():
    player = Traveller(locations["the Door room"])

    while True:
        print(player.current_location.description)
        command = input("What do you want to do? ")

        if command.startswith("move"):
            try:
                direction = command.split()[1]
                player.move(direction)
            except IndexError:
                print("That is not a valid command. Did you perhaps have a typo?")
        elif command.startswith("interact"):
            try:
                item = command.split()[1]
                player.interact(item)
            except IndexError:
                print("That is not a valid command. Did you perhaps have a typo?")
        else:
            print("You cannot do that...")

def combat():
    while True:
        sides = 20
        input(f"{YELLOW}Press enter to roll the die. You need to roll lower than 15 (d20).{RESET}")
        result = random.randint(1, sides)
        print(f"{YELLOW}You rolled a {result}{RESET}")
        if result < 15:
            print("You sprint quickly towards the man and punch him in the face. He staggers backwards and gives you another oppurtunity to attack.")
            combat_r2win()
        else:
            print("The man sees you hesitating and casts a spell on you! Watch out, one more fail and you will have zero to no chance to get out of here!")
            combat_r2lose()

def combat_r2win():
    while True:
        sides = 20
        input(f"{YELLOW}Press enter to roll the die. You need to roll lower than 10 (d20).{RESET}")
        result = random.randint(1, sides)
        print(f"{YELLOW}You rolled a {result}{RESET}")
        if result < 10:
            print(f"You kick the man in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious blue mist flows out of his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in green grass and you can feel the hot sun shine on your face.\n\n{YELLOW}CONGRATS! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            break
        else:
            print("The man sees you hesitating and casts a spell on you! Watch out, one more fail and you will have zero to no chance to get out of here!")
            combat_r3()

def combat_r2lose():
    while True:
        sides = 20
        input(f"{YELLOW}Press enter to roll the die. You need to roll lower than 10 (d20).{RESET}")
        result = random.randint(1, sides)
        print(f"{YELLOW}You rolled a {result}{RESET}")
        if result < 10:
            print("You manage to bend his hands backwards and you hear him scream in agony, and then a crackling sound. The man, who you assume is a wizard, looks angrily at you. Prepare your next attack!")
            combat_r3()
        else:
            print(f"The man sees you hesitating and casts a spell on you! That's the last thing you remember. Everything else is foggy, and you feel like your body is not really under your command. You have become the wizard's slave.\n\n{YELLOW}YOU COMPLETED THE GAME! But to what cost?\nDid you know that there is more than one ending? Play the game again to find out...{RESET}")
            False

def combat_r3():
    while True:
        sides = 20
        input("Press enter to roll the die. You need to roll lower than a 5 (d20).")
        result = random.randint(1, sides)
        print(f"You rolled a {result}")
        if result < 5:
            print(f"You kick the man in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious blue mist flows out of his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in green grass and you can feel the hot sun shine on your face.\n\n{YELLOW}CONGRATS! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            False
        else:
            print(f"The man sees you hesitating and casts a spell on you! That's the last thing you remember. Everything else is foggy, and you feel like your body is not really under your command. You have become the wizard's slave.\n\n{YELLOW}YOU COMPLETED THE GAME! But to what cost?\nDid you know that there is more than one ending? Play the game again to find out...{RESET}")
            False
    
starter()