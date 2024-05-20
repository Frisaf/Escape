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
    user_name = input(f"{INDENT}{RED}ERZÄHLER{YELLOW} Willkommen bei 'Escape!'! Fangen wir mit deinem Namen an, Reisender\n{INDENT}Wie heißen Sie?{RESET} ")
    wprint(f"{RED}ERZÄHLER: {RESET}{YELLOW}Toll! Willkommen, {GREEN}{user_name}{YELLOW}! Bevor wir mit dem Spiel beginnen, gibt es einige Dinge, die Sie wissen müssen.\nZunächst einmal gibt es zwei Arten von Befehlen: {GREEN}gebraucht{YELLOW} und {GREEN}gehen{YELLOW}. Mit dem Befehl gebraucht können Sie mit verschiedenen Dingen im Raum interagieren. Wenn Sie zum Beispiel mit dem Apfel interagieren wollen, würden Sie {GREEN}'gebraucht Apfel'{YELLOW} oder {GREEN}'gb apfel'{YELLOW} im Terminal ein und wenn Sie nach rechts gehen wollen, geben Sie {GREEN}'gehen rechts'{YELLOW} oder {GREEN}'ge r'{YELLOW} im Terminal (andere Kombinationen von Aliasen sind ebenfalls möglich). Wenn Sie rückwärts gehen, kehren Sie immer in den vorherigen Raum zurück, sofern nicht anders angegeben. Verfügbare Richtungen:{GREEN} rechts/r, links/l, rückwärts/rw, vorwärts/v{YELLOW}\nObjekte, mit denen Sie interagieren können, werden mit {CYAN}cyan{YELLOW}.\nAber jetzt lasst uns das Spiel beginnen!{RESET}")
    wprint("")
    wprint("Sie wachen in einem staubigen Zimmer auf. Du kannst dich nicht erinnern, was letzte Nacht passiert ist. Wie sind Sie überhaupt hierher gekommen? Alles, was du im Moment weißt, ist, dass du von hier verschwinden musst, und zwar schnell.")
    starter()

class Location:
    def __init__(self, name, description, directions):
        self.name = name
        self.description = description
        self.directions = directions

dir_aliases = {
    "rechts": "r",
    "links": "l",
    "vorwärts": "v",
    "rückwärts": "rw"
}

def alt_directions(direction):
    for main_dir, aliases in dir_aliases.items():
        if direction in aliases:
            return main_dir
    return None

locations = {
    ### STARTER ROOMS ###
    "Der Türzimmer": Location("zum Türzimmer", "Vor Ihnen sehen Sie zwei Türen: eine auf der rechten und eine auf der linken Seite. Sie sehen unverschlossen aus.", {"rechts": "Zimmer eins", "links": "Zimmer zwei"}),
    "Zimmer eins": Location("zu Zimmer eins", f"Soweit Sie sehen können, ist der Raum leer. An einer der kahlen Wände des Raums befindet sich jedoch ein {CYAN}Hebel{RESET}.", {"rückwärts": "Der Türzimmer"}),
    "Zimmer eins 2": Location("zu Zimmer eins", f"Soweit Sie sehen können, ist der Raum leer. An einer der kahlen Wände des Raums befindet sich jedoch ein {CYAN}Hebel{RESET}.", {"rückwärts": "Der andere Türzimmer"}),
    "Zimmer zwei": Location("zu Zimmer zwei", f"Der Raum wird von einer Fackel an einer Wand beleuchtet. In der Mitte des Raumes steht ein Tisch, auf dem ein {CYAN}Brief{RESET} liegt.", {"rückwärts": "Der Türzimmer"}),
    "Zimmer zwei 2": Location("zu Zimmer zwei", f"Der Raum wird von einer Fackel an einer Wand beleuchtet. In der Mitte des Raumes steht ein Tisch, auf dem ein {CYAN}Brief{RESET} liegt.", {"rückwärts": "Der andere Türzimmer"}),
    "Der andere Türzimmer": Location("zum Türzimmer", "Vor Ihnen sehen Sie zwei Türen: eine auf der rechten und eine auf der linken Seite. Sie sehen unverschlossen aus. Sie werden auch etwas sehen, das vorher nicht da war: eine Öffnung in der Wand direkt vor Ihnen.", {"rechts": "Zimmer eins 2", "links": "Zimmer zwei 2", "vorwärts": "Der geheime Zimmer"}),
    "Der geheime Zimmer": Location("zum geheimen Zimmer", "Der Raum ist dunkel und man kann kaum etwas sehen. Von dem Wenigen, das Sie sehen können, besteht der 'Raum' aus einem Korridor, dessen Ende Sie nicht sehen können.", {"vorwärts": "Die Korridore", "rückwärts": "Der andere Türzimmer"}),
    "Die Korridore": Location("zur Korridore", "Der Korridor ist schwach beleuchtet, und Sie können nicht viel sehen. Wenn du weitergehst, kommst du schließlich an eine Stelle, an der sich der Gang in zwei Teile teilt. Ein Weg führt nach links und der andere nach rechts.", {"rückwärts": "Der geheime Zimmer", "rechts": "Das Puzzlezimmer", "links": "Das Zimmer des Zauberers"}),
    "Das Puzzlezimmer": Location("zum Puzzlezimmer", f"Sie wenden sich nach rechts und gelangen in einen gut beleuchteten Raum mit Fackeln an den Wänden. Auf dem Boden liegen Fliesen in verschiedenen Formen in einem Raster von sechs mal sechs. Ihr Gefühl sagt Ihnen, dass ein Schritt in die falsche Richtung zum sicheren Tod führt. In der Mitte des Raumes steht ein Skelett und direkt vor dir ist auch eine Tür, die du aber erst erreichen musst. Auf dem Boden liegt auch ein {CYAN}Papier{RESET}.", {"vorwärts": "Correct tile 1", "rückwärts": "Die Korridore"}), # SAVE LOCATION
    "Letzte Tür": Location("zur Tür", f"Du schaffst es, das Rätsel zu lösen, ohne als die unglückliche Person in der Mitte des Raumes zu enden.\n\nDie {CYAN}Tür{RESET} vor Ihnen ist geschlossen.", {"rückwärts": "Correct tile 16"}),
    "Correct tile 1": Location("einer neuen Fliese", "", {"vorwärts": "Correct tile 2", "rechts": "Death", "links": "Death", "rückwärts": "Puzzle room"}),
    "Correct tile 2": Location("zu einer neuen Fliese", "Das Skelett liegt direkt vor Ihnen.", {"vorwärts": "Death", "rechts": "Death", "links": "Correct tile 3", "rückwärts": "Correct tile 1"}),
    "Correct tile 3": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Correct tile 4", "links": "Death", "rückwärts": "Correct tile 2"}),
    "Correct tile 4": Location("zu einer neuen Fliese", "Das Skelett befindet sich zu Ihrer Rechten.", {"vorwärts": "Correct tile 5", "rechts": "Death", "links": "Death", "rückwärts": "Correct tile 3"}),
    "Correct tile 5": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Correct tile 6", "links": "Death", "rückwärts": "Correct tile 4"}),
    "Correct tile 6": Location("zu einer neuen Fliese", "Das Skelett befindet sich zu Ihrer Rechten.", {"vorwärts": "Correct tile 7", "rechts": "Death", "links": "Death", "rückwärts": "Correct tile 5"}),
    "Correct tile 7": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Correct tile 8", "links": "Death", "rückwärts": "Correct tile 6"}),
    "Correct tile 8": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Death", "links": "Correct tile 9", "rückwärts": "Correct tile 7"}),
    "Correct tile 9": Location("zu einer neuen Fliese", "", {"vorwärts": "Correct tile 10", "rechts": "Death", "links": "Death", "rückwärts": "Correct tile 8"}),
    "Correct tile 10": Location("zu einer neuen Fliese", "", {"rechts": "Death", "links": "Correct tile 11", "rückwärts": "Correct tile 9"}),
    "Correct tile 11": Location("zu einer neuen Fliese", "", {"vorwärts": "Correct tile 12", "links": "Death", "rückwärts": "Correct tile 10"}),
    "Correct tile 12": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "links": "Correct tile 13", "rückwärts": "Correct tile 11"}),
    "Correct tile 13": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Correct tile 14", "links": "Death", "rückwärts": "Correct tile 12"}),
    "Correct tile 14": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "links": "Correct tile 15", "rückwärts": "Correct tile 13"}),
    "Correct tile 15": Location("zu einer neuen Fliese", "", {"vorwärts": "Correct tile 16", "links": "Death", "rückwärts": "Correct tile 14"}),
    "Correct tile 16": Location("zu einer neuen Fliese", "", {"vorwärts": "Death", "rechts": "Letzte Tür", "links": "Death", "rückwärts": "Correct tile 15"}),
    ### WIZARD ROOM ITEMS ###
    "Das Zimmer des Zauberers": Location("links", f"Du gehst weiter in diese Richtung und kommst bald darauf in einen kleinen, aber gut beleuchteten Raum. An den Wänden stehen Tische, auf denen Flaschen und Papiere ausgebreitet sind, und in der Mitte des Raumes steht ein großer Mann mit einem langen grauen Bart. Er trägt einen langen violetten Mantel, der fast den Boden berührt, und auf dem Kopf einen langen kegelförmigen Hut.\n'Oh, gut', sagt er. 'Ich habe darauf gewartet, dass jemand Neues in meine Den kommt... Oder ich meine, du willst doch hier raus, oder?\n\n{RED}ERZÄHLER:{RESET} {YELLOW}Sie haben hier zwei Möglichkeiten: ja oder nein. Schreiben Sie {CYAN}'gebraucht ja'{YELLOW} oder {CYAN}'gebraucht nein'{YELLOW} in das Terminal ein, um fortzufahren. Wenn Sie diesen Mann noch nicht treffen willst, können Sie {GREEN}'gehen rückwärts'{YELLOW} um zur Kreuzung im Korridor zurückzukehren.{RESET}", {"rückwärts": "Die Korridore"}),
    ### DEATH ###
    "Death": Location("zu einer neuen Fliese", f"Sie hören ein Klicken und dann eine laute Explosion. Alles wird schwarz...\n{YELLOW}GAME OVER! Schreiben Sie 'gehen rückwärts' um von Ihren letzten Speicherort neu zu beginnen.{RESET}", {"rückwärts": "Das Puzzlezimmer"})
}

class Traveller:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, direction):
        if direction in self.current_location.directions:
            next_location_name = self.current_location.directions[direction]
            next_location = locations[next_location_name]
            self.current_location = next_location
            wprint(f"Sie gehen {next_location.name}")
        else:
            wprint(f"{GREEN}Sie können es nicht tun...{RESET}")
    
    def gebraucht(self, item_name):
        if item_name == "hebel":
            while True:
                wprint("Sie ziehen den Hebel und hören irgendwo anders einen lauten Knall...")
                choice = input(f"{INDENT}{YELLOW}Was wollen Sie tun?{RESET} ").lower()
                if choice == "gehen rückwärts" or "ge rw" or "gehen rw" or "ge rückwärts":
                    secret_room()
                else:
                    wprint(f"{GREEN}Sie können es nicht tun...{RESET}")

        elif item_name == "brief":
            wprint(f"Sie heben den Brief auf und lesen ihn:\n{BOLD}{ITALIC}{PURPLE}Es ist schon einige Tage, nein Wochen, her, dass ich das letzte Mal geschlafen habe. Wenn Sie dies lesen, müssen Sie jetzt gehen. Dieser Ort macht mich wahnsinnig. Ich habe noch nicht herausgefunden, wie ich hier rauskomme, aber ich glaube, es hat etwas mit dem Hebel im anderen Raum zu tun{RESET}")

        elif item_name == "tür":
            while True:
                wprint(f"Du drehst vorsichtig den Türgriff und die Tür öffnet sich mit einem Quietschen. Sie sehen eine lange Treppe vor sich, und als Sie nach oben blicken, sehen Sie {GREEN} grünes Gras{RESET}.")
                choice = input(f"{INDENT}Was wollen Sie tun? ").lower()
                if choice == "gehen vorwärts" or "ge v" or "gehen v" or "ge vorwärts":
                    good_end()
                else:
                    wprint(f"{GREEN}Sie können es nicht tun...{RESET}")
        
        elif item_name == "papier":
            wprint("Du hebst das Papier auf. Es sieht aus, als hätte jemand eine Art Karte darauf geschrieben.")
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
            
        elif item_name == "ja":
            while True:
                wprint(f"Sie gehen auf den Mann zu und sagen:\n'Ja, ich möchte von hier verschwinden. Wissen Sie, wo der Ausgang ist?'\nDer Mann sieht Sie an und es sieht so aus, als würde er gleich lachen.\n'Narr!' sagt er. 'Glaubst du wirklich, dass ich, der große Zauberer Magico, einen so wertvollen Menschen entkommen lassen würde? Nein, du bist aus einem bestimmten Grund hierher gekommen, und dieser Grund ist, mir für immer zu dienen!'\n\n{RED}ERZÄHLER: {YELLOW}Magico will kämpfen! Du musst würfeln und in jeder Runde unter eine bestimmte Zahl würfeln. Der Beste von drei gewinnt, du musst also drei gewinnen, um zu gewinnen. Wenn du hingegen zwei verlierst, hat das unerwünschte Folgen{RESET}")
                combat()

        elif item_name == "nein":
            death_end()

        elif item_name == "skelett":
            wprint("Warum interagieren Sie mit dem Skelett? Dummheit.")
        
        elif item_name == "cyan":
            wprint(f"{CYAN}Dieser Text ist in Cyan geschrieben. Spielen Sie das Spiel jetzt weiter. Warum haben Sie überhaupt mit diesem Ding interagiert?")
            
        else:
            wprint(f"{GREEN}Sie können es nicht tun...{RESET}")

def good_end():
    wprint(f"Du gehst aus der Tür und die Treppe hinauf. Je weiter du nach oben kommst, desto mehr riechst du das Gras, den Wald und die Natur. Endlich bist du frei.\n\n{RED}Herzlichen Glückwunsch! {GREEN}{user_name}{YELLOW}! Du hast es durch das Spiel geschafft! Wusstest du, dass es mehr als ein Ende gibt? Spiel noch einmal, um zu sehen, wie es auch hätte enden können...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder Spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
        if end_of_game == "ja":
            restart()
            break
        elif end_of_game == "nein":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")

def death_end():
    wprint(f"Sie gehen auf den Mann zu und sagen:\n'Nein, ich würde gerne hier bleiben und noch etwas erkunden. Diese Müllhalde war eigentlich ganz interessant.'\nDer Mann sieht Sie an und scheint sich über Ihre Antwort zu freuen. Er lacht.\n'Es geht mir gut. Warum bleibst du dann nicht für immer?'\nEhe man sich versieht, hat er einen Fluch über einen verhängt, und alles, was danach kommt, ist äußerst unklar...\n\n{RED}SIE HABEN DAS SPIEL BESTANDEN!{YELLOW} Gut gemacht, {GREEN}{user_name}{YELLOW}. Sie haben das Spiel bestanden, aber zu welchem Preis? Wussten Sie, dass es mehr als ein Ende gibt? Spiel noch einmal, um zu sehen, wie es auch hätte enden können...{RESET}")
    while True:
        end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
        if end_of_game == "ja":
            restart()
            break
        elif end_of_game == "nein":
            quit_game()
            break
        else:
            wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
    
def secret_room():
    player = Traveller(locations["Der andere Türzimmer"])
    wprint("Sie gehen zum Türzimmer")

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Was wollen Sie tun?{RESET} ").lower()

        if command.startswith("gehen") or command.startswith("ge"):
            try:
                direction = command.split()[1]
                direction = alt_directions(direction)
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
        elif command.startswith("gebraucht") or command.startswith("gb"):
            try:
                item = command.split()[1]
                player.gebraucht(item)
            except IndexError:
                wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
        elif command.startswith("language") or command.startswith("språk") or command.startswith("sprachen"):
                import escape
                escape.pick_language()
        else:
            wprint(f"{GREEN}Sie können es nicht tun...{RESET}")

def starter():
    player = Traveller(locations["Der Türzimmer"])

    while True:
        wprint(player.current_location.description)
        command = input(f"{INDENT}{YELLOW}Was wollen Sie tun?{RESET} ").lower()

        if command.startswith("gehen") or command.startswith("ge"):
            try:
                direction = command.split()[1]
                direction = alt_directions(direction)
                player.move(direction)
            except IndexError:
                wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
        elif command.startswith("gebraucht") or command.startswith("gb"):
            try:
                item = command.split()[1]
                player.gebraucht(item)
            except IndexError:
                wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
        elif command.startswith("language") or command.startswith("språk") or command.startswith("sprachen"):
            import escape
            escape.pick_language()
        else:
            wprint(f"{GREEN}Sie können es nicht tun...{RESET}")

def combat():
    while True:
        sides = 20
        input(f"{INDENT}{RED}ERZÄHLER: {YELLOW}Drücken Sie die Eingabetaste, um zu würfeln. Sie müssen weniger als {GREEN}15{YELLOW} würfeln (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}ERZÄHLER: {YELLOW}Sie haben {GREEN}{result}{YELLOW} gewürfelt.{RESET}")
        if result <= 15:
            wprint("Du rennst schnell auf den Zauberer zu und schlägst ihm ins Gesicht. Er taumelt nach hinten und gibt dir die Gelegenheit zu einem weiteren Angriff.")
            combat_r2win()
        else:
            wprint("Der Zauberer sieht dein Zögern und belegt dich mit einem Zauberspruch! Pass auf, nach einem weiteren misslungenen Würfelwurf kommst du hier nicht mehr raus!")
            combat_r2lose()

def combat_r2win():
    while True:
        sides = 20
        input(f"{INDENT}{RED}ERZÄHLER: {YELLOW}Drücken Sie die Eingabetaste, um zu würfeln. Sie müssen weniger als {GREEN}10{YELLOW} würfeln (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}ERZÄHLER: {YELLOW}Sie haben {GREEN}{result}{YELLOW} gewürfelt.{RESET}")
        if result <= 10:
            wprint(f"Sie tritten Magico in den Magen. Er fällt zu Boden und es sieht so aus, als ob er bewusstlos ist. Ein mystischer {BLUE}blauer Rauch{RESET} steigt von seinem Körper in die Luft auf. Plötzlich sind Sie nicht mehr in dem dunkeln Loch, in dem Sie vorher waren, sondern Sie stehen auf einem Feld mit {GREEN}grünem Gras{RESET} und Sie können die warmen Sonnenstrahlen auf deinem Gesicht spüren.\n\n{RED}HERZLICHEN GLÜCKWUNSCH! {GREEN}{user_name}{YELLOW}! Sie haben es durch das Spiel geschafft! Wussten Sie, dass es mehr als ein Ende gibt? Spiel noch einmal, um herauszufinden, wie es auch hätte enden können...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nein":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")
        else:
            wprint("Der Zauberer sieht dein Zögern und belegt dich mit einem Zauberspruch! Pass auf, nach einem weiteren misslungenen Würfelwurf kommst du hier nicht mehr raus!")
            combat_r3()

def combat_r2lose():
    while True:
        sides = 20
        input(f"{INDENT}{RED}ERZÄHLER: {YELLOW}Drücken Sie die Eingabetaste, um zu würfeln. Sie müssen weniger als {GREEN}10{YELLOW} würfeln (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}ERZÄHLER: {YELLOW}Sie haben {GREEN}{result}{YELLOW} gewürfelt.{RESET}")
        if result <= 10:
            wprint("Sie schaffen es, seine Hände nach hinten zu biegen. Der Magier schreit vor Schmerz auf und Sie hören die Knochen in seinen Handgelenken knarren. Magico sieht dich mit Zorn in seinen Augen an. Bereite Ihrem nächsten Angriff vor!")
            combat_r3()
        else:
            wprint(f"Magico handelt schnell und belegt dich mit einem Fluch. Das ist das letzte, woran Sie sich erinnern. Alles andere ist verschwommen und es fühlt sich an, als würde dein Körper dir nicht wirklich gehorchen. Du wurdest ein Sklave des Magiers\n\n{RED}SIE HABEN DAS SPIEL BESTANDEN! {YELLOW}Gut gemacht, {GREEN}{user_name}{YELLOW} Du hast das Spiel bestanden, aber zu welchem Preis?\nWussten Sie, dass es mehr als ein Ende gibt? Spielen Sie das Spiel noch einmal, um herauszufinden, wer die anderen sind...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nein":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")

def combat_r3():
    while True:
        sides = 20
        input(f"{INDENT}{RED}ERZÄHLER: {YELLOW}Drücken Sie die Eingabetaste, um zu würfeln. Sie müssen weniger als {GREEN}5{YELLOW} würfeln (d20).{RESET}")
        result = random.randint(1, sides)
        wprint(f"{RED}ERZÄHLER: {YELLOW}You rolled a {GREEN}{result}{RESET}")
        if result <= 5:
            wprint(f"Du trittst Magico in den Magen. Er fällt zu Boden und es sieht so aus, als ob er bewusstlos ist. Ein mystischer{BLUE} blauer Rauch{RESET} steigt von seinem Körper in die Luft. Plötzlich bist du nicht mehr in dem dunklen Loch, in dem du vorher warst, sondern du stehst auf einer Wiese mit {GREEN} grünem Gras {RESET}und spürst die warmen Strahlen der Sonne auf deinem Gesicht.\n\n{RED}Herzlichen Glückwunsch! {GREEN}{user_name}{YELLOW}! Sie haben es durch das Spiel geschafft! Wussten Sie, dass es mehr als ein Ende gibt? Spiel noch einmal, um herauszufinden, wie es auch hätte enden können...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nein":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Det är inget tillgängligt kommando. Skrev du fel?{RESET}")

        else:
            wprint(f"Magico handelt schnell und belegt dich mit einem Fluch.Das ist das letzte, woran Sie sich erinnern. Alles andere ist verschwommen und es fühlt sich an, als würde dein Körper dir nicht wirklich gehorchen. Sie wurden ein Sklave des Magiers\n\n{RED}DU KLARADE SPELET!{YELLOW}Gut gemacht, {GREEN}{user_name}{YELLOW} Du hast das Spiel bestanden, aber zu welchem Preis?\nWussten Sie, dass es mehr als ein Ende gibt? Spielen Sie das Spiel noch einmal, um herauszufinden, wer die anderen sind...{RESET}")
            while True:
                end_of_game = input(f"{INDENT}{YELLOW}Möchten Sie wieder spielen?\n{INDENT}Schreib{GREEN} ja{YELLOW} oder{GREEN} nein{YELLOW}.{RESET} ").lower()
                if end_of_game == "ja":
                    restart()
                    break
                elif end_of_game == "nein":
                    quit_game()
                    break
                else:
                    wprint(f"{GREEN}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")

def restart():
    wprint(f"{GREEN}Starten Sie das Spiel neu!{RESET}")
    intro()

def quit_game():
    while True:
        confirmation = input(f"{INDENT}{YELLOW}Sind Sie sicher, dass Sie es beenden wollen?\n{INDENT}Schreib {GREEN}ja{YELLOW} oder {GREEN}nein{YELLOW}.{RESET} ").lower()
        if confirmation == "ja":
            wprint("Ausschalten des Spiels in fünf Sekunden...")
            time.sleep(5)
            exit()
        elif confirmation == "nein":
            restart()
        else:
            wprint(f"{YELLOW}Dieser Befehl ist nicht verfügbar. Haben Sie ihn falsch geschrieben?{RESET}")