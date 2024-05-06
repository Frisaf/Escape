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
    wprint(f"{RED}UPPLÄSARE: {RESET}{YELLOW}Fantastiskt! Välkommen, {GREEN}{user_name}{YELLOW}! Före vi startar spelet så finns det några saker som du behöver veta.\nFörst och främst så finns det två typer av kommandon: {GREEN}använd{YELLOW} och {GREEN}gå{YELLOW}. Kommandot använd gör så att du interagerar med olika saker i rummet, så om du till exempel vill interagera med äpplet så skulle du skriva {GREEN}'använd äpple'{YELLOW} i terminalen och om du vill flytta dig till höger så skriver du {GREEN}'gå höger'{YELLOW} i terminalen. Om du går bakåt kommer du alltid att gå tillbaka till det föregående rummet om ingenting annat sägs. Föremål som du kan interagera med är skrivet med {CYAN}cyan{YELLOW}.\nMed låt oss nu start spelet!{RESET}")
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
    "Correct tile 16": Location("en ny platta", "", {"framåt": "Death", "höger": "Sista dörren", "vänster": "Death", "bakåt": "Correct tile 15"}),
    ### WIZARD ROOM ITEMS ###
    "Trollkarlsrummet": Location("vänster", f"Du fortsätter att gå åt det hållet och snart nog kommer du till ett litet men väl upplyst rum. Längs väggarna står det bord med utpsridda flaskor och papper, och i mitten av rummet står det en lång man med ett långt grått skägg. Han har på sig en lång lila rock som nästan nuddar marken och på huvudet har han på sig en lång, konformad hatt.\n'Åh vad bra', säger han. 'Jag har väntat på att någon ny ska ta sig in i min håla.... Eller jag menar, du vill väl ta dig ut härifrån?\n\n{RED}UPPLÄSARE:{RESET} {YELLOW}Du har två val här: ja eller nej. Skriv {CYAN}'använd ja'{YELLOW} or {CYAN}'använd nej'{YELLOW} i terminalen för att fortsätta. Om du inte vill möta denna man riktigt än så kan du skriva {GREEN}'gå bakåt'{YELLOW} för att gå tillbaka till vägskälet i korridoren.{RESET}", {"ja": "Answer yes", "nej": "Answer no", "bakåt": "Korridoren"}),
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
            wprint(f"Du plockar upp brevet och läser:\n{BOLD}{ITALIC}{PURPLE}Det har gått flera dagar, nej veckor, sedan jag senast sov. Om du läser detta måste du lämna nu. Det här stället driver mig till vansinne. Jag har inte listat ut vägen ut än, men jag tror att det har något att göra med spaken i det andra rummet...{RESET}")

        elif item_name == "dörr":
            while True:
                wprint(f"Du vrider försiktigt på dörrhandtaget och dörren öppnas med ett gnisslande läte. Du ser en lång trappa framför dig, och när du tittar mot toppen skymtar du {GREEN}grönt gräs.{RESET}")
                choice = input(f"{INDENT}Vad vill du göra? ")
                if choice == "gå framåt":
                    good_end()
                else:
                    wprint(f"{GREEN}Du kan inte göra det...{RESET}")
        
        elif item_name == "papper":
            wprint("Du plockar upp pappret. Det ser ut som om någon skrivit ned någon sorts karta på den.")
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
            
        elif item_name == "ja":
            while True:
                wprint(f"Du går fram till mannen och säger:\n'Ja, jag vill gärna ta mig ut härifrån. Vet du var utgången är?'\nMannen tittar på dig och det ser ut som om han är på väg att skratta.\n'Dåre!' säger han. 'Tror du verkligen att jag, den stora trollkarlen Magico, skulle låta en så värdeful människa fly? Nej, du kom hit av en anledning, och den anledningen är att tjäna mig för evigt!'\n\n{RED}UPPLÄSARE: {YELLOW}Magico vill slåss! Du behöver rulla tärning och rulla under ett visst nummer varje runda. Bäst av tre vinner, så du behöver vinna tre för att vinna. Om du å andra sidan förlorar två kommer det att få oönskade konsekvenser...{RESET}")
                combat()

        elif item_name == "nej":
            death_end()

        elif item_name == "skelett":
            wprint("Varför interagerar du med skelettet? Fåntratt.")
            
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def good_end():
    wprint(f"Du går ut genom dörren och går uppför trapporna. Allt eftersom du kommer längre och längre upp börjar du känna lukten av gräs, och skog, och natur. Till sist är du äntligen fri.\n\n{RED}GRATTIS {GREEN}{user_name}{YELLOW}! Du klarade av spelet! Visste du att det finns mer än ett slut? Spela igen för att se hur det också kunde ha slutat...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Spela igen?\n{INDENT}Skriv{GREEN} ja{YELLOW} eller{GREEN} nej{YELLOW}.{RESET} ")
        if end_of_game == "ja":
            restart()
            break
        elif end_of_game == "nej":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

def death_end():
    wprint(f"Du går fram till mannen och säger:\n'Nej, jag skulle vilja stanna här och utforska lite till. Den här hålan var faktiskt ganska intressant.'\nMannen ser på dig och ser ut att vara glad över ditt svar. Han skrattar.\n'Bra. Varför stannar du inte för evigt isåfall?'\nInnan du vet ordet av har han kastat en förbannelse över dig och allting efter det är extremt otydligt...\n\n{RED}DU KLARADE SPELET!{YELLOW} Bra jobbat, {GREEN}{user_name}{YELLOW}. DU klarade spelet, men till vilket pris? Visste du att det finns mer än ett slut? Spela igen för att se hur det också kunde ha slutat...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Spela igen?\n{INDENT}Skriv{GREEN} ja{YELLOW} eller{GREEN} nej{YELLOW}.{RESET} ")
        if end_of_game == "ja":
            restart()
            break
        elif end_of_game == "nej":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
    
def secret_room():
    player = Traveller(locations["Det andra dörrummet"])
    wprint("Du går till dörrummet")

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Vad vill du göra?{RESET} ")

        if command.startswith("gå"):
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
        elif command.startswith("language") or command.startswith("språk"):
                import escape
                escape.pick_language()
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def starter():
    player = Traveller(locations["Dörrummet"])

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Vad vill du göra?{RESET} ")

        if command.startswith("gå"):
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
        elif command.startswith("language") or command.startswith("språk"):
            import escape
            escape.pick_language()
        else:
            wprint(f"{GREEN}Du kan inte göra det...{RESET}")

def combat():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Tryck enter för att kasta tärningen. Du behöver rulla lägre än {GREEN}15{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}Du rullade {GREEN}{result}{RESET}")
        if result <= 15:
            wprint("Du springer fort mot trollkarlen och slår honom i ansiktet. Han stapplar bakåt och ger dig ett tillfälle för ytterligare en attack.")
            combat_r2win()
        else:
            wprint("Trollkarlen ser att du tvekar och kastar en trollformel mot dig! Se upp, efter ett till misslyckat tärningskast kommer du inte kunna ta dig ut härifrån!")
            combat_r2lose()

def combat_r2win():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Tryck enter för att kasta tärningen. Du behöver rulla lägre än {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}Du rullade {GREEN}{result}{RESET}")
        if result <= 10:
            wprint(f"Du sparkar Magico i magen. Han faller till marken och det ser ut som att han är medvetslös. En mysyisk {BLUE}blå rök{RESET} stiger från hans kropp och ut i luften. Plötsligt är du inte längre i den mörka hålan du var i förut, utan du står istället på ett fält täckt av {GREEN}grönt gräs{RESET} och du kan känna solens varma strålar skina på ditt ansikte.\n\n{RED}GRATTIS {GREEN}{user_name}{YELLOW}! Du klarade av spelet! Visste du att det finns mer än ett slut? Spela igen för att ta reda på hur det också kunde ha slutat...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Spela igen?\n{INDENT}Skriv{GREEN} ja{YELLOW} eller{GREEN} nej{YELLOW}.{RESET} ")
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nej":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")
        else:
            wprint("Trollkarlen ser att du tvekar och kastar en trollformel mot dig! Se upp, efter ett till misslyckat tärningskast kommer du inte kunna ta dig ut härifrån!")
            combat_r3()

def combat_r2lose():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Tryck enter för att kasta tärningen. Du behöver rulla lägre än {GREEN}10{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}Du rullade {GREEN}{result}{RESET}")
        if result <= 10:
            wprint("Du lyckas böja hans händer baklänges. Trollkarlen skriker av smärta och du hör hur benen i hans handleder knakar. Magico ser på dig med ursinne i blicken. Förbered din nästa attack!")
            combat_r3()
        else:
            wprint(f"Magico agerar snabbt och kastar en förbannelse på dig. Det är det sista du kommer ihåg. Allt annat är otydligt och det känns som om din kropp inte riktigt lyder dig. Du blev trollkarlens slav\n\n{RED}DU KLARADE SPELET! {YELLOW}Bra jobbat, {GREEN}{user_name}{YELLOW} Du klarade spelet, men till vilket pris?\nVisste du att det finns mer än ett slut? Spela spelet igen för att ta reda på vilka de andra är...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Spela igen?\n{INDENT}Skriv{GREEN} ja{YELLOW} eller{GREEN} nej{YELLOW}.{RESET} ")
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nej":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

def combat_r3():
    while True:
        sides = 20
        input(f"{INDENT}{RED}UPPLÄSARE: {YELLOW}Tryck enter för att kasta tärningen. Du behöver rulla lägre än {GREEN}5{YELLOW} (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}UPPLÄSARE: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 5:
            wprint(f"Du sparkar Magico i magen. Han faller till marken och det ser ut som att han är medvetslös. En mysyisk {BLUE}blå rök{RESET} stiger från hans kropp och ut i luften. Plötsligt är du inte längre i den mörka hålan du var i förut, utan du står istället på ett fält täckt av {GREEN}grönt gräs{RESET} och du kan känna solens varma strålar skina på ditt ansikte.\n\n{RED}GRATTIS {GREEN}{user_name}{YELLOW}! Du klarade av spelet! Visste du att det finns mer än ett slut? Spela igen för att ta reda på hur det också kunde ha slutat...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Spela igen?\n{INDENT}Skriv{GREEN} ja{YELLOW} eller{GREEN} nej{YELLOW}.{RESET} ")
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nej":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

        else:
            wprint(f"Magico agerar snabbt och kastar en förbannelse på dig. Det är det sista du kommer ihåg. Allt annat är otydligt och det känns som om din kropp inte riktigt lyder dig. Du blev trollkarlens slav\n\n{RED}DU KLARADE SPELET!{YELLOW}Bra jobbat, {GREEN}{user_name}{YELLOW} Du klarade spelet, men till vilket pris?\nVisste du att det finns mer än ett slut? Spela spelet igen för att ta reda på vilka de andra är...{RESET}")
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
    wprint(f"{GREEN}Startar om spelet!{RESET}")
    intro()

def quit_game():
    while True:
        confirmation = input(f"{INDENT}{YELLOW}Är du säker på att du vill avsluta?\n{INDENT}Skriv {GREEN}ja{YELLOW} eller {GREEN}nej{YELLOW}.{RESET} ")
        if confirmation == "ja":
            wprint("Stänger av spelet om fem sekunder...")
            time.sleep(5)
            exit()
        elif confirmation == "nej":
            restart()
        else:
            wprint(f"{YELLOW}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")