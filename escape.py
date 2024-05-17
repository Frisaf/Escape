import random
import time
import textwrap
import ctypes
import escape_se
import escape_de

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
CYAN = "\033[36m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
PURPLE = "\033[35m"
INDENT = " "*20
BLUE   = "\033[34m"

def wprint(text, width = 80):
    newlines = text.split("\n")
    for newlines in newlines:
        wrapped = textwrap.wrap(newlines, width = width)
        for wrapped in wrapped:
            print(" "*20, wrapped)

def intro():
    global user_name
    user_name = input(f"{INDENT}{RED}NARRATOR:{YELLOW} Welcome to 'Escape!'! Let's start with your name, traveller.\n{INDENT}What's your name?{RESET} ")
    wprint(f"{RED}NARRATOR: {RESET}{YELLOW}Great! Welcome, {GREEN}{user_name}{YELLOW}! Before we start the game, there are a few things that you need to know.\nFirst of all, there are two types of commands: {GREEN}interact/i{YELLOW} and {GREEN}move/m{YELLOW}. The interact command will make you interact with things in the room. For example, if you want to interact with the apple you would type {GREEN}'interact apple'{YELLOW} in the terminal and if you want to move right you would type {GREEN}'move right'{YELLOW} or {GREEN} m right {YELLOW}in the terminal. Moving backwards will always lead you to the previous room if nothing else is stated. Available directions: {GREEN}right (r), left (l), forwards (f), backwards (b)\n{YELLOW} Items that you can interact with are written in {CYAN}cyan{YELLOW}.\nBut with that, let's move on with the game, shall we?{RESET}")
    wprint("")
    wprint("You wake up on a dusty room. You don't remember what happened last night. How did you even end up here? All you know is that you have to get out, and that fast.")
    starter()

def pick_language():
    gb = "\U0001F1EC\U0001F1E7"
    se = "\U0001F1F8\U0001F1EA"
    de = "\U0001F1E9\U0001F1EA"
    wprint(f"{YELLOW}Pick your preferred language:{RESET}\n"+ gb + f" {GREEN}English{RESET}\n" + se + f" {GREEN}Svenska{RESET}\n" + de + f" {GREEN}Deutsch{RESET}\n" + f"{ITALIC}{YELLOW}You can always change language during scenes when you can move freely by typing {GREEN}'language'{YELLOW} (it also works with the word for language in all available languages) in the terminal. {BLUE}Please note that changing language in the middle of the game will reset your progress.{RESET}")
    while True:
        picked_language = input(f"{INDENT}> ").lower()
        if picked_language == "english" or picked_language == "en":
            intro()
            break
        elif picked_language == "svenska" or picked_language == "se":
            escape_se.intro()
            break
        elif picked_language == "deutsch" or picked_language == "de":
            escape_de.intro()
            break
        else:
            wprint(f"{RED}Please pick an available language.{RESET}")

class Location:
    def __init__(self, name, description, directions):
        self.name = name
        self.description = description
        self.directions = directions

dir_aliases = {
    "right": "r",
    "left": "l",
    "forwards": "f",
    "backwards": "b"
}

def alt_directions(direction):
    for main_dir, aliases in dir_aliases.items():
        if direction in aliases:
            return main_dir
    return None

locations = {
    ### STARTER ROOMS ###
    "the Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked.", {"right": "Room one", "left": "Room two"}),
    "Room one": Location("Room one", f"From what you can see the room is empty, with black and bare stone walls on all four sides. However, there is a {CYAN}lever{RESET} on your right side.", {"backwards": "the Door room"}),
    "Room one 2": Location("Room one", f"From what you can see the room is empty, with black and cold stone walls on all four sides. However, there is a {CYAN}lever{RESET} on your right side.", {"backwards": "the second Door room"}),
    "Room two": Location("Room two", f"The room is lit up with a torch and there is a table at the middle of the room. On the table, there is a {CYAN}letter{RESET}.", {"backwards": "the Door room"}),
    "Room two 2": Location("Room two", f"The room is lit up with a torch and there is a table at the middle of the room. On the table, there is a {CYAN}letter{RESET}.", {"backwards": "the second Door room"}),
    "the second Door room": Location("the Door room", "In front of you, there are two doors: one on your right side and one on your left side. They look unlocked. You also see something right ahead of you that was not there before: an opening in the wall.", {"right": "Room one 2", "left": "Room two 2", "forwards": "Hidden room"}),
    "Hidden room": Location("the Hidden room", "The room is dark, and you barely see a thing. From what you can tell, the 'room' consists of a corridor of which you cannot see the end of.", {"forwards": "Corridor", "backwards": "the second Door room"}),
    "Corridor": Location("the corridor", "The corridor is barely lit up and you cannot see much. As you continue walking, you reach a point where the corridor splits in two. One way goes left and the other goes right.", {"backwards": "Hidden room", "right": "Puzzle room", "left": "Wizard room"}),
    "Puzzle room": Location("the Puzzle room", f"You turn right and reach a room well lit up with torches on the wall. On the floor, there are tiles in different shapes. The tiles are placed in a six by six grid, and your gut feeling tells you that one step in the wrong direction can lead to death. There is a skeleton at the middle of the room. Right ahead of you is a door, but you need to reach it first. There is also a sheet of {CYAN}paper{RESET} on the floor.", {"forwards": "Correct tile 1", "backwards": "Corridor"}), # SAVE LOCATION
    "Final door": Location("the door", f"You successfully finished the puzzle, and managed to not end up like the unlucky guy at the middle of the room.\n\nThe {CYAN}door{RESET} in front of you is closed.", {"backwards": "Correct tile 16"}),
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
    "Wizard room": Location("the left", f"As you continue to walk in that direction, you eventually reach a small but well lit room. There are vials and papers spread all around the tables that stand alongside the walls, and in the middle stands a tall man with a long gray beard. He is wearing a long purple robe that almost touches the ground and there is a tall, cone shaped hat on his head.\n'Oh great', the man says. 'I've waited for someone new to step into my dungeon... Or I mean, you want to get out of here, don't you?'\n\n{RED}NARRATOR:{RESET} {YELLOW}You have two choices here: yes or no. Type {CYAN}'interact yes'{YELLOW} or {CYAN}'interact no'{YELLOW} in your terminal to continue. If you don't want to encounter this man just yet, you can type {GREEN}'move backwards'{YELLOW} to go back to the crossroad in the corridor.{RESET}", {"backwards": "Corridor"}),
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
            wprint(f"You walk to {next_location.name}")
        else:
            wprint(f"{GREEN}You cannot go that way...{RESET}")
    
    def interact(self, item_name):
        if item_name == "lever":
            while True:
                wprint("You pull the lever and hear a loud thud somewhere else...")
                choice = input(f"{INDENT}{YELLOW}What do you want to do?{RESET} ").lower()
                if choice == "move backwards" or "m b" or "move b" or "m backwards":
                    secret_room()
                else:
                    wprint(f"{GREEN}You cannot do that...{RESET}")
        elif item_name == "letter":
            wprint(f"You pick up the letter and start to read:\n{BOLD}{ITALIC}{PURPLE}It's been days, no weeks, since I last slept. If you read this, you need to leave now. This place is driving me insane. I haven't figured out the way out yet, but I think it has something to do with the lever in the other room...{RESET}")

        elif item_name == "door":
            while True:
                wprint(f"You carefully turn the door knob and the door opens with a squeeking noise. There is now a long stair case in front of you. As you look at the top, you catch a glimpse of {GREEN}green grass.{RESET}")
                choice = input(f"{INDENT}What do you want to do? ").lower()
                if choice == "move forwards" or "m f" or "move f" or "m forwards":
                    good_end()
                else:
                    wprint(f"{GREEN}You cannot do that...{RESET}")
        
        elif item_name == "paper":
            wprint("You pick up the paper, and you see that it seems to contain a map of some sort.")
            wprint(f"""\
                  {PURPLE}
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
                wprint(f"You walk up to the man and say:\n'Yes, I really want to get out of here. Do you know where the exit is?'\nThe man looks at you, and it looks like he is on the verge to laughing.\n'You fool!' he says. 'Did you really think I, the great wizard Magico would let such a precious human escape? No, you came here for a reason, and that reason is to serve me forever!'\n\n{RED}NARRATOR: {YELLOW}Magico initiates a fight! You will need to roll a die and get under a certain number every round. You will play three rounds, so you will have to win two of them to succeed. Losing two rounds will have unwanted consequences...{RESET}")
                combat()

        elif item_name == "no":
            death_end()

        elif item_name == "skeleton":
            wprint("Why did you interact with the skeleton? Silly.")
        
        elif item_name == "cyan":
            wprint(f"{CYAN}This text is written in cyan. Continue to play the game now. Why did you even interact with this thing?")
            
        else:
            wprint(f"{GREEN}You cannot do that...{RESET}")

def good_end():
    wprint(f"You walk thorugh the door and proceed to climb the stairs. As you walk, you start to smell the wonderful smell of grass, and forest, and nature. You are only one step from freedom. One more step. Now you are free.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You completed the game! Did you know there are more than one ending? Play the game again to find out how it could also have ended...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ").lower()
        if end_of_game == "yes":
            restart()
            break
        elif end_of_game == "no":
            quit_game()
            break
        else:
            wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")

def death_end():
    wprint(f"You walk up to the man and say:\n'No, I would like to stay here and explore a little more. This dungeon was actually pretty interesting.'\nThe man looks at you, and he seems happy with your answer. He chuckles.\n'Good. Why don't you stay forever then?'\nBefore you know it, he has cast a spell upon you, and everything after that is incredibly foggy...\n\n{RED}YOU COMPLETED THE GAME!{YELLOW} Good job, {GREEN}{user_name}{YELLOW}. You completed the game, but to what cost? Did you know that there are several endings? Play again to find out what the other ones are...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ").lower()
        if end_of_game == "yes":
            restart()
            break
        elif end_of_game == "no":
            quit_game()
            break
        else:
            wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
    
def secret_room():
    player = Traveller(locations["the second Door room"])
    wprint("You walk to the Door room.")

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}What do you want to do?{RESET} ").lower()

        if command.startswith("move"):
            try:
                direction = command.split()[1]
                direction = alt_directions(direction)
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
        elif command.startswith("interact"):
            try:
                item = command.split()[1]
                player.interact(item)
            except IndexError:
                wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
        elif command.startswith("language") or command.startswith("språk") or command.startswith("sprach"):
            pick_language()
        else:
            wprint(f"{GREEN}You cannot do that...{RESET}")

def starter():
    player = Traveller(locations["the Door room"])

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}What do you want to do?{RESET} ").lower()

        if command.startswith("move") or command.startswith("m"):
            try:
                direction = command.split()[1]
                direction = alt_directions(direction)
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
        elif command.startswith("interact") or command.startswith("i"):
            try:
                item = command.split()[1]
                player.interact(item)
            except IndexError:
                wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
        elif command.startswith("language") or command.startswith("språk") or command.startswith("sprache"):
            pick_language()
        else:
            wprint(f"{GREEN}You cannot do that...{RESET}")

def combat():
    while True:
        sides = 20
        input(f"{INDENT}{RED}NARRATOR: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}15{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}NARRATOR: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 15:
            wprint("You sprint quickly towards the wizard and punch him in the face. He staggers backwards and gives you another oppurtunity to attack.")
            combat_r2win()
        else:
            wprint("The wizard sees you hesitating and casts a spell on you! Watch out, one more fail and you will have little to no chance to get out of here!")
            combat_r2lose()

def combat_r2win():
    while True:
        sides = 20
        input(f"{INDENT}{RED}NARRATOR: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}NARRATOR: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 10:
            wprint(f"You kick Magico in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious {BLUE}blue mist{RESET} rises out from his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in {GREEN}green grass{RESET} and you can feel the hot sun shine on your face.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ").lower()
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")
        else:
            wprint("The wizard sees you hesitating and casts a spell on you! Watch out, one more fail and you will have zero to no chance to get out of here!")
            combat_r3()

def combat_r2lose():
    while True:
        sides = 20
        input(f"{INDENT}{RED}NARRATOR: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}NARRATOR: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 10:
            wprint("You manage to bend his hands backwards and you hear him scream in agony, and then a crackling sound. Magico looks angrily at you. Prepare your next attack!")
            combat_r3()
        else:
            wprint(f"Magico acts fast and casts a spell on you! That's the last thing you remember. Everything else is foggy, and you feel like your body is not really under your command. You have become the wizard's slave.\n\n{RED}YOU COMPLETED THE GAME!{YELLOW}Good job, {GREEN}{user_name}{YELLOW} You completed the game, but to what cost?\nDid you know that there is more than one ending? Play the game again to find out what the others are...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ").lower()
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")

def combat_r3():
    while True:
        sides = 20
        input(f"{INDENT}{RED}NARRATOR: {YELLOW}Press enter to roll the die. You need to roll lower than a {GREEN}5{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}NARRATOR: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 5:
            wprint(f"You kick Magico in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious {BLUE}blue mist{RESET} flows out of his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in {GREEN}green grass{RESET} and you can feel the hot sun shine on your face.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ").lower()
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")

        else:
            wprint(f"The wizard acts fast and casts a spell on you! That's the last thing you remember. Everything else is foggy, and you feel like your body is not really under your command. You have become the wizard's slave.\n\n{RED}YOU COMPLETED THE GAME!{YELLOW}Good job, {GREEN}{user_name}{YELLOW}. You completed the game, but to what cost?\nDid you know that there is more than one ending? Play the game again to find out...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}That is not a valid command. Did you perhaps have a typo?{RESET}")

def restart():
    wprint(f"{GREEN}Restarting game!{RESET}")
    intro()

def quit_game():
    while True:
        confirmation = input(f"{INDENT}{YELLOW}Are you sure you want to quit?\n{INDENT}Type {GREEN}yes{YELLOW} or {GREEN}no{YELLOW}.{RESET} ").lower()
        if confirmation == "yes":
            wprint("Quitting in five seconds...")
            time.sleep(5)
            exit()
        elif confirmation == "no":
            restart()
        else:
            wprint(f"{YELLOW}That is not a valid command. Did you perhaps have a typo?{RESET}")

pick_language()