class Location:
    def __init__(self, name, description, exits):
        self.name = name
        self.description = description
        self.exits = exits

locations = {
    ### STARTER ROOMS ###
    "the Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked.", {"right": "Room one", "left": "Room two"}),
    "Room one": Location("Room one", "From what you can see the room is empty, with black and cold stone walls on all four sides. However, there is a lever on your right side.", {"backwards": "the Door room"}),
    "Room two": Location("Room two", "The room is lit up with a torch and there is a table at the middle of the room. On the table, there is a letter.", {"backwards": "the Door room"}),
    "the second Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked. You also see something right ahead of you that was not there before: an opening in the wall.", {"right": "Room one", "left": "Room two", "forwards": "Hidden room"}),
    "Hidden room": Location("the Hidden room", "The room is dark, and you barely see a thing. From what you can tell, the 'room' consists of a corridor of which you cannot see the end of.", {"forwards": "Corridor", "backwards": "the second Door room"}),
    "Corridor": Location("the corridor", "The corridor is barely lit up and you cannot see much. As you continue walking, you reach a point where the corridor splits in two. One way goes left and the other goes right.", {"backwards": "Hidden room", "right": "Puzzle room", "left": "Wizard room"}),
    "Puzzle room": Location("the Puzzle room", "You turn right and reach a room well lit up with torches on the wall. On the floor, there are tiles in different shapes. The tiles are placed in a six by six grid, and your gut feeling tells you that one step in the wrong direction can lead to death. There is a skeleton at the middle of the room. Right ahead of you is a door, but you need to reach it first.", {"forwards": "Correct tile 1", "backwards": "Corridor"}),
    "Final door": Location("the door", "You successfully finished the puzzle, and managed to not end up like the unlucky guy at the middle of the room.\n\nThe door in front of you is closed.", {"backwards": "Correct tile 16"}),
    "Final door opened": Location("the door, thorugh it and proceed to climb the stairs.", "As you walk, you start to smell the wonderful smell of grass, and forest, and nature. You are only one step from freedom. One more step. Now you are free.\n\nCONGRATULATIONS! You completed the game? Did you know there are more than one ending? Play the game again to find out how it could also have ended...", {}),
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
    "Correct tile 14": Location("a new tile", "", {"forwards": "Correct tile 15", "left": "Death", "backwards": "Correct tile 13"}),
    "Correct tile 15": Location("a new tile", "", {"forwards": "Correct tile 16", "left": "Death", "backwards": "Correct tile 14"}),
    "Correct tile 16": Location("a new tile", "", {"forwards": "Death", "right": "Final door", "left": "Death", "backwards": "Correct tile 15"}),
    ### DEATH ###
    "Death": Location("a new tile", "You hear a sudden click and then a loud bang. Then, everything turns black...\nGAME OVER! Restart the game to try again.", {})
}

class Traveller:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, direction):
        if direction in self.current_location.exits:
            next_location_name = self.current_location.exits[direction]
            next_location = locations[next_location_name]
            self.current_location = next_location
            print(f"You move to {next_location.name}")
        else:
            print("You cannot go that way...")
    
    def interact(self, item_name):
        if item_name == "lever":
            print("You pull the lever and hear a large thud somewhere else...")
            choice = input("What do you want to do? ")
            if choice == "move backwards":
                secret_room()
            else:
                print("You cannot do that...")
        elif item_name == "letter":
            print("You pick up the letter and start to read:\nIt's been weeks, no ages since I last slept. If you read this, you need to leave now. This place is driving me insane. I haven't figured out the way out yet, but I think it has something to do with the lever in the other room...")

        elif item_name == "door":
            print("You carefully turn the door knob and the door opens with a squeeking noise. There is now a long stair case in front of you. As you look at the top, you catch a glimpse of green grass.")
            choice = input("What do you want to do? ")
            if choice == "move forwards":
                ending()
            else:
                print("You cannot do that...")
    
def secret_room():
    player = Traveller(locations["the second Door room"])
    print("You move to the Door room.")

    while True:
        print(player.current_location.description)
        command = input("What do you want to do? ")

        if command.startswith("move"):
            direction = command.split()[1]
            player.move(direction)
        elif command.startswith("interact"):
            item = command.split()[1]
            player.interact(item)
        else:
            print("You cannot do that...")

def ending():
    player = Traveller(locations["Final door"])


def starter():
    player = Traveller(locations["the Door room"])

    user_name = input("Welcome to 'Escape!'! Let's start with your name, traveller.\nWhat's your name? ")
    print(f"Great! Welcome, {user_name}! Before we start the game, there are a few things that you need to know.\nFirst of all, there are two types of commands: interact and move. The interact command will make you interact with things in the room. For example, if you want to interact with the apple you would type 'interact apple' in the terminal and if you want to move right you would type 'move right' in the terminal. Moving backwards will always lead you to the previous room if nothing else is stated.\nBut with that, let's move on with the game, shall we?")
    print("")
    print("You wake up on a dusty room. You don't remember what happened last night. How did you even end up here? All you know is that you have to get out, and that fast.")

    while True:
        print(player.current_location.description)
        command = input("What do you want to do? ")

        if command.startswith("move"):
            direction = command.split()[1]
            player.move(direction)
        elif command.startswith("interact"):
            item = command.split()[1]
            player.interact(item)
        else:
            print("You cannot do that...")

starter()