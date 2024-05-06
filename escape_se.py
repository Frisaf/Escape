import random
import time
import textwrap
import ctypes

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
    user_name = input(f"{INDENT}{RED}UPPLÄSARE:{YELLOW} Välkommen till 'Escape!'! Vi börjar med namn.\n{INDENT}Vad heter du?{RESET} ")
    wprint(f"{RED}UPPLÄSARE: {RESET}{YELLOW}Fantastiskt! Välkommen, {GREEN}{user_name}{YELLOW}! Före vi börjar spelet så finns det några saker som du behöver veta.\nFörst och främst så finns det två typer av kommandon: {GREEN}använd{YELLOW} och {GREEN}move{YELLOW}. Kommandot använd gör så att du interagerar med olika saker i rummet, så om du till exempel vill interagera med äpplet så skulle du skriva {GREEN}'använd äpple'{YELLOW} i terminalen och om du vill flytta dig till höger så skriver du {GREEN}'gå höger'{YELLOW} i terminalen. Om du går bakåt kommer du alltid att gå tillbaka till det föregående rummet om ingenting annat sägs. Föremål som du kan interagera med är skrivet med {CYAN}cyan{YELLOW}.\nMed låt oss nu start spelet!{RESET}")
    wprint("")
    wprint("Du vaknar i ett dammigt rum. Du kommer inte ihåg vad som hände förra natten. Hur kom du ens hit? Allt du vet just nu är att du måste ta dig ut härifrån, snabt.")
    starter()

class Location:
    def __init__(self, name, description, directions):
        self.name = name
        self.description = description
        self.directions = directions

locations = {
    ### STARTER ROOMS ###
    "Dörrummet": Location("dörrummet", "Framför dig ser du två dörrar: en till höger och en till vänster. De ser olåsta ut.", {"höger": "Rum ett", "vänster": "Rum två"}),
    "Rum ett": Location("rum ett", f"Utifrån vad du kan se så är rummet tomt. På en av rummets kala väggar sitter det dock en {CYAN}spak{RESET}.", {"bakåt": "Dörrummet"}),
    "Rum ett 2": Location("rum ett", f"Utifrån vad du kan se så är rummet tomt. På en av rummets kala väggar sitter det dock en {CYAN}spak{RESET}.", {"bakåt": "Det andra dörrummet"}),
    "Rum två": Location("Rum två", f"Rummet är upplyst av en fackla som sitter på ena väggen. I mitten av rummet finns det ett bord, och på bordet ligger det ett {CYAN}brev{RESET}.", {"bakåt": "Dörrummet"}),
    "Rum två 2": Location("Rum två", f"Rummet är upplyst av en fackla som sitter på ena väggen. I mitten av rummet finns det ett bord, och på bordet ligger det ett {CYAN}brev{RESET}.", {"bakåt": "Det andra dörrummet"}),
    "Det andra dörrummet": Location("Dörrummet", "Framför dig ser du två dörrar: en till höger och en till vänster. De ser olåsta ut. Du ser även något som inte var där tidigare, nämligen en öppning i väggen rakt framför dig.", {"höger": "Rum ett 2", "vänster": "Rum två 2", "framåt": "Det hemliga rummet"}),
    "Det hemliga rummet": Location("det hemliga rummet", "Rummet är mörkt och du ser knappt någonting. Av det lilla du kan se så består 'rummet' av en korridor som du inte kan se slutet av.", {"framåt": "Korridoren", "bakåt": "Det andra dörrummet"}),
    "Korridoren": Location("korridoren", "Korridoren är svagt upplyst och du kan inte se mycket. När du fortsätter att gå kommer du så småning om till en punkt där korridoren delar sig i två. En väg går vänster och den andra går höger.", {"bakåt": "Det hemliga rummet", "höger": "Pusselrummet", "vänster": "Trollkarlsrummet"}),
    "Pusselrummet": Location("pusselrummet", f"Du svängar höger och kommer fram till ett väl upplyst rum med facklor på väggarna. På golvet ligger det kakelplattor i olika former i ett rutnät som är sex gånger sex plattor stort. Din magkänsla säger dig att ett steg i fel riktning kommer leda till en säker död. Det är ett skelett i mitten av rummet och rakt framför dig finns det även en dörr, men du måste nå den först. Det ligger även ett {CYAN}papper{RESET} på marken.", {"framåt": "Correct tile 1", "bakåt": "Korridoren"}), # SAVE LOCATION
    "Sista dörren": Location("dörren", f"Du lyckas med att ta dig igenom pusslet utan att sluta upp som den olyckliga personen i mitten av rummet.\n\n{CYAN}Dörren{RESET} framför dig är stängd", {"bakåt": "Correct tile 16"}),
    "Correct tile 1": Location("en ny platta", "", {"framåt": "Correct tile 2", "höger": "Death", "vänster": "Death", "bakåt": "Puzzle room"}),
    "Correct tile 2": Location("en ny platta", "Skelettet är rakt framför dig.", {"framåt": "Death", "höger": "Death", "vänster": "Correct tile 3", "bakåt": "Correct tile 1"}),
    "Correct tile 3": Location("en ny platta", "", {"framåt": "Death", "höger": "Correct tile 4", "vänster": "Death", "bakåt": "Correct tile 2"}),
    "Correct tile 4": Location("en ny platta", "Skelettet är till höger om dig.", {"framåt": "Correct tile 5", "höger": "Death", "vänster": "Death", "bakåt": "Correct tile 3"}),
    "Correct tile 5": Location("en ny platta", "", {"framåt": "Death", "höger": "Correct tile 6", "vänster": "Death", "bakåt": "Correct tile 4"}),
    "Correct tile 6": Location("en ny platta", "Skelettet är till höger om dig.", {"framåt": "Correct tile 7", "höger": "Death", "vänster": "Death", "bakåt": "Correct tile 5"}),
    "Correct tile 7": Location("en ny platta", "", {"framåt": "Death", "höger": "Correct tile 8", "vänster": "Death", "bakåt": "Correct tile 6"}),
    "Correct tile 8": Location("en ny platta", "", {"framåt": "Death", "höger": "Death", "vänster": "Correct tile 9", "bakåt": "Correct tile 7"}),
    "Correct tile 9": Location("en ny platta", "", {"framåt": "Correct tile 10", "höger": "Death", "vänster": "Death", "bakåt": "Correct tile 8"}),
    "Correct tile 10": Location("en ny platta", "", {"höger": "Death", "vänster": "Correct tile 11", "bakåt": "Correct tile 9"}),
    "Correct tile 11": Location("en ny platta", "", {"framåt": "Correct tile 12", "vänster": "Death", "bakåt": "Correct tile 10"}),
    "Correct tile 12": Location("en ny platta", "", {"framåt": "Death", "vänster": "Correct tile 13", "bakåt": "Correct tile 11"}),
    "Correct tile 13": Location("en ny platta", "", {"framåt": "Death", "höger": "Correct tile 14", "vänster": "Death", "bakåt": "Correct tile 12"}),
    "Correct tile 14": Location("en ny platta", "", {"framåt": "Death", "vänster": "Correct tile 15", "bakåt": "Correct tile 13"}),
    "Correct tile 15": Location("en ny platta", "", {"framåt": "Correct tile 16", "vänster": "Death", "bakåt": "Correct tile 14"}),
    "Correct tile 16": Location("en ny platta", "", {"framåt": "Death", "höger": "Final door", "vänster": "Death", "bakåt": "Correct tile 15"}),
    ### WIZARD ROOM ITEMS ###
    "Wizard room": Location("vänster", f"Du fortsätter att gå åt det hållet och snart nog kommer du till ett litet men väl upplyst rum. Längs väggarna står det bord med utpsridda flaskor och papper, och i mitten av rummet står det en lång man med ett långt grått skägg. Han har på sig en lång lila rock som nästan nuddar marken och på huvudet har han på sig en lång, konformad hatt.\n'Åh vad bra', säger han. 'Jag har väntat på att någon ny ska ta sig in i min håla.... Eller jag menar, du vill väl ta dig ut härifrån?\n\n{RED}UPPLÄSARE:{RESET} {YELLOW}Du har två val här: ja eller nej. Skriv {CYAN}'använd ja'{YELLOW} or {CYAN}'använd nej'{YELLOW} i terminalen för att fortsätta. Om du inte vill möta denna man riktigt än så kan du skriva {GREEN}'gå bakåt'{YELLOW} för att gå tillbaka till vägskälet i korridoren.{RESET}", {"ja": "Answer yes", "nej": "Answer no", "bakåt": "Korridoren"}),
    ### DEATH ###
    "Death": Location("en ny platta", f"Du hör ett klick och sedan en högljudd explosion. Allting blir svart...\n{YELLOW}GAME OVER! Skriv 'gå bakåt' för att starta om från din senaste sparplats.{RESET}", {"bakåt": "Pusselrummet"})
}

class Traveller:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, direction):
        if direction in self.current_location.directions:
            next_location_name = self.current_location.directions[direction]
            next_location = locations[next_location_name]
            self.current_location = next_location
            wprint(f"Du går till {next_location.name}")
        else:
            wprint(f"{GREEN}Du kan inte gå dit...{RESET}")
    
    def använd(self, item_name):
        if item_name == "spak":
            while True:
                wprint("Du drar i spaken och hör en högljudd duns någon annan stans...")
                choice = input(f"{INDENT}{YELLOW}Vad vill du göra?{RESET} ")
                if choice == "gå bakåt":
                    secret_room()
                else:
                    wprint(f"{GREEN}Du kan inte göra det...{RESET}")
        elif item_name == "brev":
            wprint(f"You pick up the letter and start to read:\n{BOLD}{ITALIC}{PURPLE}It's been weeks, no ages, since I last slept. If you read this, you need to leave now. This place is driving me insane. I haven't figured out the way out yet, but I think it has something to do with the lever in the other room...{RESET}")

        elif item_name == "door":
            while True:
                wprint(f"You carefully turn the door knob and the door opens with a squeeking noise. There is now a long stair case in front of you. As you look at the top, you catch a glimpse of {GREEN}green grass.{RESET}")
                choice = input(f"{INDENT}Vad vill du göra? ")
                if choice == "move framåt":
                    good_end()
                else:
                    wprint(f"{GREEN}Du kan inte göra det...{RESET}")
        
        elif item_name == "paper":
            wprint("You pick up the paper, and you see that it seems to contain a map of some sort.")
            wprint(f"""\
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
                wprint(f"You walk up to the man and say:\n'Yes, I really want to get out of here. Do you know where the exit is?'\nThe man looks at you, and it looks like he is on the verge to laughing.\n'You fool!' he says. 'Did you really think I, the great wizard Magico would let such a precious human escape? No, you came here for a reason, and that reason is to serve me forever!'\n\n{RED}UPPLÄSARE: {YELLOW}Magico initiates a fight! You will need to roll a die and get under a certain number every round. You will play three rounds, so you will have to win two of them to succeed. Losing two rounds will have unwanted consequences...{RESET}")
                combat()

        elif item_name == "no":
            death_end()

        elif item_name == "skeleton":
            wprint("Why did you använd with the skeleton? Silly.")
            
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def good_end():
    wprint(f"You walk thorugh the door and proceed to climb the stairs. As you walk, you start to smell the wonderful smell of grass, and forest, and nature. You are only one step from freedom. One more step. Now you are free.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You completed the game! Did you know there are more than one ending? Play the game again to find out how it could also have ended...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
        if end_of_game == "yes":
            restart()
            break
        elif end_of_game == "no":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

def death_end():
    wprint(f"You walk up to Magico and say:\n'No, I would like to stay here and explore a little more. This dungeon was actually pretty interesting.'\nThe wizard looks at you, and he seems happy with your answer. He chuckles.\n'Good. Why don't you stay forever then?'\nBefore you know it, he has cast a spell upon you, and everything after that is incredibly foggy...\n\n{RED}YOU COMPLETED THE GAME!{YELLOW} Good job, {GREEN}{user_name}{YELLOW}. You completed the game, but to what cost? Did you know that there are several endings. Play again to find out what the other ones are...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
        if end_of_game == "yes":
            restart()
            break
        elif end_of_game == "no":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
    
def secret_room():
    player = Traveller(locations["the second Door room"])
    wprint("Du går till the Door room.")

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Vad vill du göra?{RESET} ")

        if command.startswith("move"):
            try:
                direction = command.split()[1]
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        elif command.startswith("använd"):
            try:
                item = command.split()[1]
                player.använd(item)
            except IndexError:
                wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def starter():
    player = Traveller(locations["the Door room"])

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Vad vill du göra?{RESET} ")

        if command.startswith("move"):
            try:
                direction = command.split()[1]
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        elif command.startswith("använd"):
            try:
                item = command.split()[1]
                player.använd(item)
            except IndexError:
                wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def combat():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}15{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 15:
            wprint("You sprint quickly towards the wizard and punch him in the face. He staggers bakåt and gives you another oppurtunity to attack.")
            combat_r2win()
        else:
            wprint("The wizard sees you hesitating and casts a spell on you! Watch out, one more fail and you will have zero to no chance to get out of here!")
            combat_r2lose()

def combat_r2win():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 10:
            wprint(f"You kick Magico in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious {BLUE}blue mist{RESET} flows out of his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in {GREEN}green grass{RESET} and you can feel the hot sun shine on your face.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        else:
            wprint("The wizard sees you hesitating and casts a spell on you! Watch out, one more fail and you will have zero to no chance to get out of here!")
            combat_r3()

def combat_r2lose():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Press enter to roll the die. You need to roll lower than {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 10:
            wprint("You manage to bend his hands bakåt and you hear him scream in agony, and then a crackling sound. The man, who you assume is a wizard, looks angrily at you. Prepare your next attack!")
            combat_r3()
        else:
            wprint(f"Magico acts fast and casts a spell on you! That's the last thing you remember. Everything else is foggy, and you feel like your body is not really under your command. You have become the wizard's slave.\n\n{RED}YOU COMPLETED THE GAME!{YELLOW}Good job, {GREEN}{user_name}{YELLOW} You completed the game, but to what cost?\nDid you know that there is more than one ending? Play the game again to find out...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

def combat_r3():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Press enter to roll the die. You need to roll lower than a {GREEN}5{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 5:
            wprint(f"You kick Magico in his stomach and he falls to the ground. It seems like he is uncouncious. A mysterious {BLUE}blue mist{RESET} flows out of his body and out in the air, and suddenly you are no longer in the dark dungeon you were in before. No, you are standing on a field covered in {GREEN}green grass{RESET} and you can feel the hot sun shine on your face.\n\n{RED}CONGRATULATIONS {GREEN}{user_name}{YELLOW}! You finished the game! Did you know that there are more than one ending? Play the game again to find out what could have happened...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Play again?\n{INDENT}Type{GREEN} yes{YELLOW} or{GREEN} no{YELLOW}.{RESET} ")
                if end_of_game == "yes":
                    restart()
                    break
                elif end_of_game == "no":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

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
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

def restart():
    wprint(f"{GREEN}Restarting game!{RESET}")
    intro()

def quit_game():
    while True:
        confirmation = input(f"{INDENT}{YELLOW}Are you sure you want to quit?\n{INDENT}Type {GREEN}yes{YELLOW} or {GREEN}no{YELLOW}.{RESET} ")
        if confirmation == "yes":
            wprint("Quitting in five seconds...")
            time.sleep(5)
            exit()
        elif confirmation == "no":
            restart()
        else:
            wprint(f"{YELLOW}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")