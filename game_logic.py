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
    # random.shuffle(deck)
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

    user_input = input(action_prompt)
    if user_input.isdigit() and 0 <= int(user_input) < len(player['private_hand']):
        selected_card = player['private_hand'][int(user_input)]
        discard_card_helper(selected_card, player, discard_deck)
    else:
        return "Invalid input. Please enter a valid number."


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
    user_input = input(action_prompt)
    if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
        selected_color = color_choices[int(user_input)]
    property_card['active_color'] = selected_color
    return property_card


def place_money(player, money_card):
    add_card_to_hand(player['public_hand'], money_card)
    remove_card_from_hand(player['private_hand'], money_card)
    player['move_count'] += 1
    return


# Functions for placing a house and a hotel
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
    else:
        action_prompt = "What color would you like to assign to the house? \n"
        for i, action in enumerate(color_choices):
            action_prompt += "Enter '{}': {}\n".format(i, action)
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
        house_card['active_color'] = selected_color
        return house_card


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
    else:
        action_prompt = "What color would you like to assign to the hotel? \n"
        for i, action in enumerate(color_choices):
            action_prompt += "Enter '{}': {}\n".format(i, action)
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(color_choices):
            selected_color = color_choices[int(user_input)]
        hotel_card['active_color'] = selected_color
        return hotel_card


def place_hotel(player, hotel_card):
    hotel_card = prompt_hotel_color_choice(player, hotel_card)
    if hotel_card['active_color'] == ['None']:
        return
    else:
        add_card_to_hand(player['public_hand'], hotel_card)
        remove_card_from_hand(player['private_hand'], hotel_card)
        player['move_count'] += 1
        return


# Functions for rent
def charge_rent(receiver, payers, dollars):
    for payer in payers:
        payment_sum = 0
        while payment_sum < dollars:
            if not payer['public_hand']:
                break
            action_prompt = "You have been charged ${} in rent! You have paid ${} so far." \
                            "Select which cards you want to pay with.\n".format(dollars, payment_sum)
            actions = []
            for card in payer['public_hand']:
                actions.append(card)
            for i, action in enumerate(actions):
                action_prompt += "Enter '{}': {}\n".format(i, action)
            user_input = input(action_prompt)
            selected_card = actions[int(user_input)]
            payment_sum += int(selected_card['value'])
            add_card_to_hand(receiver['public_hand'], selected_card)
            remove_card_from_hand(payer['public_hand'], selected_card)
    receiver['move_count'] += 1
    return

def check_rent(player, rent_card):
    pass


# Function for prompting the player for a decision
def player_decision(player):
    actions = ['End Turn', 'Discard Card']
    for card in player['private_hand']:
        actions.append(card)

    action_prompt = "What would you like to do {}? You've taken {} moves.\n".format(player['name'],
                                                                                    player['move_count'])

    for i, action in enumerate(actions):
        action_prompt += "Enter '{}': {}\n".format(i, action)

    user_input = input(action_prompt)
    if user_input.isdigit() and 0 <= int(user_input) < len(actions):
        selected_action = actions[int(user_input)]
        return selected_action
    else:
        return "Invalid input. Please enter a valid number."


# Function for setting up a new game
def game_setup():
    print('Welcome to Monopoly Deal! Complete three property sets to win.\n')
    number_of_players = int(input("How many players? "))
    players = []  # List to store player objects
    for i in range(1, number_of_players + 1):
        name = f"Player{i}"
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

                elif decision['name'] == 'Pass Go':
                    draw_cards(deck, player, 2)
                    player['move_count'] += 1

                else:
                    print("Invalid action:", decision)


if __name__ == "__main__":
    run_game()
