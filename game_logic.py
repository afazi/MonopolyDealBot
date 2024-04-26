import random
import card_info


# Functions for creating the deck and cards
def create_card(name, card_type, colors_available, active_color, value):
    return {'name': name, 'card_type': card_type, 'colors_available': colors_available, 'active_color': active_color,
            'value': value}


def create_deck():
    new_deck = []
    for card_data in card_info.card_list:
        card_data_shortened = card_data[:5]
        for _ in range(card_data[5]):
            new_deck.append(create_card(*card_data_shortened))
    return new_deck


def shuffle_deck(deck):
    random.shuffle(deck)
    deck.reverse()
    return


def reset_deck(deck, discard_deck):
    deck.extend(discard_deck)
    shuffle_deck(deck)
    return


# Functions for moving cards
def draw_cards(deck, player, cards_number):
    for _ in range(cards_number):
        player['private_hand'].append(deck.pop())


def add_card_to_hand(hand, card):
    hand.append(card)
    return


def remove_card_from_hand(hand, card):
    hand.remove(card)
    return


def display_public_cards(players):
    for player in players:
        print(f"{player['name']}'s public hand:")
        for card in player['public_hand']:
            print(card['name'] + ' ' + card['active_color'])
        print("\n")
    return


def discard_card(player, discard_deck):
    def discard_card_helper(card, player, discard_deck):
        discard_deck.append(card)
        remove_card_from_hand(player['private_hand'], card)

    action_prompt = "Which card would you like to discard? \n"

    for i, card in enumerate(player['private_hand']):
        action_prompt += "Enter '{}': {}\n".format(i, card['name'])

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(player['private_hand']):
            selected_card = player['private_hand'][int(user_input)]
            discard_card_helper(selected_card, player, discard_deck)
            break  # Exit the loop once a valid card is selected and discarded
        else:
            print("Invalid input. Please enter a valid number.")


# Function to prompt the player to choose another player
def prompt_pick_player(player, players_list):
    action_prompt = "{}, pick another player.\n".format(player['name'])
    for i, other_player in enumerate(players_list):
        action_prompt += "Enter '{}': {}\n".format(i, other_player['name'])
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(players_list):
            selected_player = players_list[int(user_input)]
            return selected_player
        else:
            print("Invalid input. Please enter a valid number.")


# Functions for placing properties and money
def get_color_max(color):
    color_entry = next((entry for entry in card_info.rent_table if entry[0] == color), None)
    return len(color_entry[1]) if color_entry else 0


def update_property_count(player, new_card):
    property_sets = player['property_sets']
    new_card_color = new_card['active_color']
    if new_card_color in property_sets:
        property_sets[new_card_color] += 1
    else:
        property_sets[new_card_color] = 1


def check_properties_count(player):
    property_sets = player['property_sets']
    completed_sets = 0
    for color, count in property_sets.items():
        max_properties = get_color_max(color)
        completed_of_a_color = count // max_properties
        completed_sets += completed_of_a_color

    if completed_sets >= 3:
        print(f'Congratulations! {player} has won the game!')
    else:
        return


def place_property(player, property_card):
    if len(property_card['colors_available']) > 1:
        property_card = prompt_property_color_choice(player, property_card)
    add_card_to_hand(player['public_hand'], property_card)
    remove_card_from_hand(player['private_hand'], property_card)
    player['move_count'] += 1
    update_property_count(player, property_card)
    check_properties_count(player)
    return


def prompt_property_color_choice(player, property_card):
    color_choices = []
    if property_card['name'] == 'Wild Property':
        for card in player['public_hand']:
            if card['active_color'] != 'None':
                if card['active_color'] not in color_choices:
                    color_choices.append(card['active_color'])
    else:
        for color in property_card['colors_available']:
            color_choices.append(color)

    action_prompt = "What color would you like to assign to the wild card? \n"
    for i, action in enumerate(color_choices):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
            property_card['active_color'] = selected_color
            return property_card
        else:
            print("Invalid input. Please enter a valid number.")


def place_money(player, money_card):
    remove_card_from_hand(player['private_hand'], money_card)
    money_card['card_type'] = 'Money'
    add_card_to_hand(player['public_hand'], money_card)
    player['move_count'] += 1
    return


def prompt_house_color_choice(player, house_card):
    property_sets = player['property_sets']
    color_choices = []
    for card in player['public_hand']:
        active_color = card['active_color']
        if active_color not in ['None', 'black', 'Electric', 'Water']:
            max_properties = get_color_max(active_color)
            if property_sets.get(active_color, 0) >= max_properties:
                if active_color not in color_choices:
                    color_choices.append(active_color)
    for card in player['public_hand']:
        if card['card_type'] == 'House':
            color_choices.remove(card['active_color'])

    if not color_choices:
        print('No available sets for placing down a house!')
        return house_card

    action_prompt = "What color would you like to assign to the house? \n"
    for i, action in enumerate(color_choices):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
            house_card['active_color'] = selected_color
            return house_card
        else:
            print("Invalid input. Please enter a valid number.")


def place_house(player, house_card):
    house_card = prompt_house_color_choice(player, house_card)
    if house_card['active_color'] == ['None']:
        return
    else:
        add_card_to_hand(player['public_hand'], house_card)
        remove_card_from_hand(player['private_hand'], house_card)
        player['move_count'] += 1
        return


def prompt_hotel_color_choice(player, hotel_card):
    color_choices = []
    for card in player['public_hand']:
        if card['card_type'] == 'House':
            if card['active_color'] not in color_choices:
                color_choices.append(card['active_color'])
    for card in player['public_hand']:
        if card['card_type'] == 'Hotel':
            color_choices.remove(card['active_color'])

    if not color_choices:
        print('No available sets for placing down a hotel!')
        return hotel_card

    action_prompt = "What color would you like to assign to the hotel? \n"
    for i, action in enumerate(color_choices):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
            hotel_card['active_color'] = selected_color
            return hotel_card
        else:
            print("Invalid input. Please enter a valid number.")


def place_hotel(player, hotel_card):
    hotel_card = prompt_hotel_color_choice(player, hotel_card)
    if hotel_card['active_color'] == ['None']:
        return
    else:
        add_card_to_hand(player['public_hand'], hotel_card)
        remove_card_from_hand(player['private_hand'], hotel_card)
        player['move_count'] += 1
        return


def charge_rent(receiver, payers, dollars):
    for payer in payers:
        payment_sum = 0
        while payment_sum < dollars:
            if not payer['public_hand']:
                print("{} has no cards left! \n".format(payer['name']))
                break
            action_prompt = "{}, you have been charged ${} in rent! You have paid ${} so far." \
                            "Select which cards you want to pay with.\n".format(payer, dollars, payment_sum)
            actions = []
            for card in payer['public_hand']:
                actions.append(card)
            for i, action in enumerate(actions):
                action_prompt += "Enter '{}': {}\n".format(i, action)
            while True:  # Keep prompting until valid input is provided
                user_input = input(action_prompt)
                if user_input.isdigit() and 0 <= int(user_input) < len(actions):
                    selected_card = actions[int(user_input)]
                    payment_sum += int(selected_card['value'])
                    add_card_to_hand(receiver['public_hand'], selected_card)
                    remove_card_from_hand(payer['public_hand'], selected_card)
                    break  # Exit the loop once a valid card is selected
                else:
                    print("Invalid input. Please enter a valid number.")
    receiver['move_count'] += 1
    return


def prompt_rent_color_choice(player, rent_card):
    public_hand_colors = []
    for card in player['public_hand']:
        if card['active_color'] != 'None':
            if card['active_color'] not in public_hand_colors:
                public_hand_colors.append(card['active_color'])

    color_choices = []
    for color in public_hand_colors:
        if color in rent_card['colors_available']:
            color_choices.append(color)

    if not color_choices:
        print("You can't charge rent with this color so it is played as money")
        return rent_card

    action_prompt = "What color would you like to charge rent on? \n"
    for i, action in enumerate(color_choices):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
            rent_card['active_color'] = selected_color
            return rent_card
        else:
            print("Invalid input. Please enter a valid number.")


def check_rent(player, rent_card):
    rent_charge = 0
    active_color = rent_card['active_color']
    property_sets = player['property_sets']
    property_count = property_sets[active_color]
    for row in card_info.rent_table:
        if row[0] == active_color:
            for rent_row in row[1]:
                if rent_row[0] == property_count:
                    rent_charge = rent_row[1]
    # Check for houses
    for card in player['public_hand']:
        if card['card_type'] == 'House':
            if card['active_color'] == active_color:
                rent_charge += 3
    # Check for hotels
    for card in player['public_hand']:
        if card['card_type'] == 'Hotel':
            if card['active_color'] == active_color:
                rent_charge += 4
    return rent_charge


def play_rent_card(player, rent_card, players, discard_deck):
    rent_card = prompt_rent_color_choice(player, rent_card)
    if rent_card['active_color'] == 'None':
        place_money(player, rent_card)
    else:
        payers = [x for x in players if x != player]
        if rent_card['name'] == 'Rent - Wild':
            payers = [prompt_pick_player(player, payers)]

        rent_charge = check_rent(player, rent_card)
        charge_rent(player, payers, rent_charge)
        remove_card_from_hand(player['private_hand'], rent_card)
        add_card_to_hand(discard_deck, rent_card)


# More Action Functions
def pass_go(player, pass_go_card, deck, discard_deck):
    action_prompt = "Would you like to pass go or play this card as money?\n" \
                    "1: Pass go\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            draw_cards(deck, player, 2)
            remove_card_from_hand(player['private_hand'], pass_go_card)
            add_card_to_hand(discard_deck, pass_go_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, pass_go_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


def birthday(player, players, birthday_card, discard_deck):
    action_prompt = "Would you like to collect your birthday money or play this card as money?\n" \
                    "1: Collect your birthday money!\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            payers = [x for x in players if x != player]
            charge_rent(player, payers, 2)
            remove_card_from_hand(player['private_hand'], birthday_card)
            add_card_to_hand(discard_deck, birthday_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, birthday_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


def debt_collector(player, players, debt_collector_card, discard_deck):
    action_prompt = "Would you like to collect your debt or play this card as money?\n" \
                    "1: Collect your debt\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            payers = [x for x in players if x != player]
            payers = [prompt_pick_player(player, payers)]
            charge_rent(player, payers, 5)
            remove_card_from_hand(player['private_hand'], debt_collector_card)
            add_card_to_hand(discard_deck, debt_collector_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, debt_collector_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


# Function for prompting the player for a decision
def player_decision(player):
    actions = ['End Turn', 'Discard Card']
    for card in player['private_hand']:
        actions.append(card)

    action_prompt = "What would you like to do {}? You've taken {} moves.\n".format(player['name'],
                                                                                    player['move_count'])

    for i, action in enumerate(actions):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(actions):
            selected_action = actions[int(user_input)]
            return selected_action
        else:
            print("Invalid input. Please enter a valid number.")


# Function for setting up a new game
def game_setup():
    print('Welcome to Monopoly Deal! Complete three property sets to win.\n')

    # Continuously prompt for the number of players until a valid response is given
    while True:
        try:
            number_of_players = int(input("How many players? Pick between 2 and 5: "))
            if 2 <= number_of_players <= 5:
                break  # Exit the loop if a valid number of players is provided
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

    players = []  # List to store player objects
    for i in range(1, number_of_players + 1):
        name = f"Player {i}"
        player = {
            'name': name,
            'public_hand': [],
            'private_hand': [],
            'move_count': 0,
            'property_sets': {}
        }
        players.append(player)

    # Create & shuffle the deck, deal 5 cards to each player
    deck = create_deck()
    shuffle_deck(deck)
    discard_deck = []

    for player in players:
        draw_cards(deck, player, 5)

    return players, deck, discard_deck


# Loop to run actual gameplay
def run_game():
    players, deck, discard_deck = game_setup()

    while True:
        for player in players:
            display_public_cards(players)
            draw_cards(deck, player, 2)
            player['move_count'] = 0

            while True:
                if player['move_count'] == 3:
                    break
                else:
                    decision = player_decision(player)

                if decision == 'End Turn':
                    card_count = len(player['private_hand'])
                    while card_count > 7:
                        print(f"You are holding {card_count} cards. You can only hold 7. Choose which card to discard ")
                        discard_card(player, discard_deck)
                        card_count = len(player['private_hand'])
                    else:
                        break

                elif decision == 'Discard Card':
                    discard_card(player, discard_deck)

                elif decision['card_type'] == 'Property':
                    place_property(player, decision)

                elif decision['card_type'] == 'Money':
                    place_money(player, decision)

                elif decision['card_type'] == 'House':
                    place_house(player, decision)

                elif decision['card_type'] == 'Hotel':
                    place_hotel(player, decision)

                elif decision['card_type'] == 'Rent':
                    play_rent_card(player, decision, players, discard_deck)

                elif decision['name'] == 'Pass Go':
                    pass_go(player, decision, deck, discard_deck)

                elif decision['name'] == 'Birthday!':
                    birthday(player, players, decision, discard_deck)

                elif decision['name'] == 'Debt Collector':
                    debt_collector(player, players, decision, discard_deck)

                else:
                    print("Invalid action:", decision)


if __name__ == "__main__":
    run_game()
