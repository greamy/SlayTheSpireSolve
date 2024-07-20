import copy
import os


def clean_input(full_file):
    cards = copy.deepcopy(full_file)
    for idx, line in enumerate(full_file):
        if ".png" in line:
            cards.remove(line)

    for idx, line in enumerate(cards):
        cards[idx] = line[1:]

    return cards


def parse(clean_file):
    template = """from Entities.Player import Player
from Actions.Card import Card\n\n
class Name(Card):
    def __init__(self):
        super().__init__("name", energy, damage, attacks, block, draw, discard, exhaust, status, stance)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # DESCRIPTION"""

    classes = {}

    cur_idx = 0
    while cur_idx < len(clean_file):
        line = clean_file[cur_idx]
        if "-" in line:
            cur_idx += 1
            line = (clean_file[cur_idx])[2:]
            card_name_end_index = line.index("|")
            line = line[:card_name_end_index] + "\n"
            clean_file[cur_idx] = line
            card_name = line.replace(" ", "")[:-1]
            card_name = card_name.replace("-", "")

            cur_idx += 1
            clean_file.pop(cur_idx)
            card_type = clean_file[cur_idx]

            cur_idx += 1
            line = clean_file[cur_idx]
            # TODO: Also parse upgraded energy cost
            card_energy = line[0]

            cur_idx += 1

            card_description = clean_file[cur_idx]
            card_description = card_description.replace("KW|", "")
            clean_file[cur_idx] = card_description

            card_class = template.replace("Name", card_name)
            card_class = card_class.replace("name", card_name)
            card_class = card_class.replace("energy", card_energy)

            deal_index = card_description.find("Deal")
            if deal_index == -1:
                card_class = card_class.replace("damage", "0")
                card_class = card_class.replace("attacks", "0")
            elif card_description[deal_index:].find("(") != -1:
                deal_index += 5
                card_class = card_class.replace("attacks", "1")
                parenthesis_index = card_description[deal_index:].find("(") + deal_index
                card_class = card_class.replace("damage", card_description[deal_index:parenthesis_index])
            else:
                deal_index += 5
                card_class = card_class.replace("attacks", "1")
                d_index = card_description[deal_index:].find("damage") + deal_index
                card_class = card_class.replace("damage", card_description[deal_index:d_index-1])

            gain_index = card_description.find("Gain")
            if gain_index == -1:
                card_class = card_class.replace("block", "0")
            else:
                block_index = card_description[gain_index:].find("{{") + gain_index + 2
                if card_description[block_index:block_index+5] == "Block":
                    if card_description[gain_index:].find("(") != -1:
                        gain_index += 5
                        parenthesis_index = card_description[gain_index:].find("(") + gain_index
                        card_class = card_class.replace("block", card_description[gain_index:parenthesis_index])
                    else:
                        gain_index += 5
                        b_index = card_description[gain_index:].find("{") + gain_index
                        card_class = card_class.replace("block", card_description[gain_index:b_index - 1])
                else:
                    card_class = card_class.replace("block", "0")

            exhaust_index = card_description.find("{{Exhaust}}.")
            if exhaust_index == -1:
                card_class = card_class.replace("exhaust", "False")
            else:
                card_class = card_class.replace("exhaust", "True")

            exit_stance_index = card_description.find("Exit your {{Stance}}")
            if exit_stance_index != -1:
                card_class = card_class.replace("stance", "Player.Stance.NONE")

            enter_stance_index = card_description.find("Enter {{")
            if enter_stance_index != -1:
                enter_stance_index += 8
                end_stance_word_index = card_description[enter_stance_index:].find("}") + enter_stance_index
                card_class = card_class.replace("stance", "Player.Stance." +
                                                card_description[enter_stance_index:end_stance_word_index].upper())

            card_class = card_class.replace("stance", "None")
            card_class = card_class.replace("draw", "0")
            card_class = card_class.replace("discard", "0")
            card_class = card_class.replace("status", "\"\"")
            card_class = card_class.replace("U,", "1000,")
            card_class = card_class.replace("X,", "0,")
            card_class = card_class.replace("DESCRIPTION", card_description)

            classes[card_name] = card_class

        cur_idx += 1

    return classes


def main():
    with open("cards.txt", "r") as file:
        full_file = file.readlines()
    cards = clean_input(full_file)

    classes = parse(cards)
    with open("new_cards.txt", "w") as file:
        file.writelines(cards)

    for class_name, class_string in classes.items():
        path = os.path.join(os.path.curdir, "../Actions/Library_Parse")
        path = os.path.join(path, class_name + ".py")
        with open(path, "w") as file:
            file.write(class_string)


if __name__ == "__main__":
    main()
