class Room:
    def __init__(self, name, description, exits):
        self.name = name
        self.description = description
        self.exits = exits

rooms = {
    "the Door room": Room("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked.", {"right": "Room one", "left": "Room two"}),
    "Room one": Room("Room one", "From what you can see the room is empty, with black and cold stone walls on all four sides. However, there is a lever on your right side.", {"backwards": "the Door room"}),
    "Room two": Room("Room two", "The room is lit up with a torch and there is a table at the middle of the room. On the table, there is a letter.", {"backwards": "the Door room"}),
    "the second Door room": Room("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked.", {"right": "Room one", "left": "Room two", "forwards": "Hidden room"}),
    "Hidden room": Room("Hidden room", "The room is dark, and you barely see a thing. From what you can tell, the 'room' consists of a corridor to which you cannot see the end of.", {"forwards:": "Puzzle room", "backwards": "the second Door room"})
}

class Player:
    def __init__(self, current_room):
        self.current_room = current_room

    def move(self, direction):
        if direction in self.current_room.exits:
            next_room_name = self.current_room.exits[direction]
            next_room = rooms[next_room_name]
            self.current_room = next_room
            print(f"You move to {next_room.name}")
        else:
            print("You cannot go that way...")
    
    def interact(self, item_name):
        if item_name == "lever":
            print("You pull the lever and hear a large thud somewhere else...")
            choice = input("What do you do? ")
            if choice == "move backwards":
                secret_room()
            else:
                print("You cannot do that...")
        elif item_name == "letter":
            print("You pick up the letter and start to read:\nIt's been weeks, no ages since I last slept. If you read this, you need to leave now. This place is driving me insane. I haven't figured out the way out yet, but I think it has something to do with the lever in the other room...")
    
def secret_room(self):
    print("You move to the Door room.")
    player = Player(rooms["the second Door room"])
    print("You also see something right ahead of you that was not there before: an opening in the wall.")
    command = input("What do you want to do? ")

    while True:
        direction = command.split()[1]

        if command.startswith("move"):
            player.move(direction)
        elif command.startswith("interact"):
            item = command.split()[1]
            player.interact(item)
        else:
            print("You cannot do that...")


def main():
    player = Player(rooms["the Door room"])

    user_name = input("Welcome to 'Escape!'! Let's start with your name, traveller.\nWhat's your name? ")
    print(f"Great! Welcome, {user_name}! Before we start the game, there are a few things that you need to know.\nFirst of all, there are two types of commands: interact and move. The interact command will make you interact with things in the room. For example, if you want to interact with the apple you would type 'interact apple' in the terminal and if you want to move right you would type 'move right' in the terminal. Moving backwards will always lead you to the previous room if nothing else is stated.\nBut with that, let's move on with the game, shall we?")
    print("")
    print("You wake up on a dusty room. You don't remember what happened last night. How did you even end up here? All you know is that you have to get out, and that fast.")

    while True:
        print(player.current_room.description)
        command = input("What do you want to do? ")

        if command.startswith("move"):
            direction = command.split()[1]
            player.move(direction)
        elif command.startswith("interact"):
            item = command.split()[1]
            player.interact(item)
        else:
            print("You cannot do that...")

main()