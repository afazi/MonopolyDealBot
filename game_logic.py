import random
import card_info


# Functions for creating the deck and cards
def create_card(name, card_type, colors_available, active_color, value):
    return {'name': name, 'card_type': card_type, 'colors_available': colors_available, 'active_color': active_color,
            'value': value}


def create_deck():
    new_deck = []
    for card_data in card_info.test_card_list:
        card_data_shortened = card_data[:5]
        for _ in range(card_data[5]):
            new_deck.append(create_card(*card_data_shortened))
    return new_deck


def shuffle_deck(deck):
    #random.shuffle(deck)
    deck.reverse()


def reset_deck(deck, discard_deck):
    deck.extend(discard_deck)
    shuffle_deck(deck)
    discard_deck.clear()


# Functions for moving cards
def draw_cards(deck, player, cards_number):
    for _ in range(cards_number):
        player['private_hand'].append(deck.pop())


def display_public_cards(players):
    for player in players:
        print(f"{player['name']}'s public hand:")
        for card in player['public_hand']:
            print(card['name'] + ' ' + card['active_color'])
        print("\n")


def discard_card(player, discard_deck):
    def discard_card_helper(card, player, discard_deck):
        discard_deck.append(card)
        player['private_hand'].remove(card)

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


def update_property_count(players):
    for player in players:
        completed_sets = 0
        player_property_sets = player['property_sets']
        player_public_hand = player['public_hand']
        for value in player_property_sets.values():
            value[0] = 0
            value[1] = 0
        for card in player_public_hand:
            if card['card_type'] == 'Property':
                player_property_sets[card['active_color']][0] += 1
        for value in player_property_sets.values():
            value[1] = value[0] // value[2]
            completed_sets += value[1]
        if completed_sets >= 3:
            print(f'Congratulations! {player} has won the game!')
    return


def place_property(player, property_card):
    if len(property_card['colors_available']) > 1:
        property_card = prompt_property_color_choice(player, property_card)
    player['public_hand'].append(property_card)
    player['private_hand'].remove(property_card)
    player['move_count'] += 1
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
    player['private_hand'].remove(money_card)
    money_card['card_type'] = 'Money'
    player['public_hand'].append(money_card)
    player['move_count'] += 1
    return


def prompt_house_color_choice(player, house_card):
    property_sets = player['property_sets']
    color_choices = []
    for card in player['public_hand']:
        active_color = card['active_color']
        if active_color not in ['None', 'black', 'Electric', 'Water']:
            if property_sets[active_color][1] >= 1:
                if active_color not in color_choices:
                    color_choices.append(active_color)
    for card in player['public_hand']:
        if card['card_type'] == 'House':
            color_choices.remove(card['active_color'])

    if not color_choices:
        print('No available sets for placing down a house. It is played as money')
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
    player['public_hand'].append(house_card)
    player['private_hand'].remove(house_card)
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
        player['public_hand'].append(hotel_card)
        player['private_hand'].remove(hotel_card)
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
                            "Select which cards you want to pay with.\n".format(payer['name'], dollars, payment_sum)
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
                    receiver['public_hand'].append(selected_card)
                    payer['public_hand'].remove(selected_card)
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
    property_count = property_sets[active_color][0]
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
        double_rent_answer = prompt_double_rent(player, discard_deck)
        for payer in payers:
            if prompt_say_no(player, payer, discard_deck, rent_card):
                player['move_count'] += 1
                player['private_hand'].remove(rent_card)
                discard_deck.append(rent_card)
                return
        rent_charge = check_rent(player, rent_card)
        if double_rent_answer:
            double_rent_charge = rent_charge * 2
            charge_rent(player, payers, double_rent_charge)
        else:
            charge_rent(player, payers, rent_charge)
        player['private_hand'].remove(rent_card)
        discard_deck.append(rent_card)
        player['move_count'] += 1


def prompt_double_rent(player, discard_deck):
    for card in player['private_hand']:
        if card['name'] == 'Double the Rent':
            if player['move_count'] < 2:
                user_input = input('Would you like to use your Double The Rent Card on top of this rent?\n'
                                   '1: Yes \n'
                                   '2: No \n')
                if user_input == 1:
                    player['private_hand'].remove(card)
                    discard_deck.append(card)
                    player['move_count'] += 1
                    return True
                else:
                    return False




# Pass go, birthday, and debt collector action functions
def pass_go(player, pass_go_card, deck, discard_deck):
    action_prompt = "Would you like to pass go or play this card as money?\n" \
                    "1: Pass go\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            draw_cards(deck, player, 2)
            player['private_hand'].remove(pass_go_card)
            discard_deck.append(pass_go_card)
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
            for payer in payers:
                if prompt_say_no(player, payer, discard_deck, birthday_card):
                    player['move_count'] += 1
                    player['private_hand'].remove(birthday_card)
                    discard_deck.append(birthday_card)
                    return
            charge_rent(player, payers, 2)
            player['private_hand'].remove(birthday_card)
            discard_deck.append(birthday_card)
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
            for payer in payers:
                if prompt_say_no(player, payer, discard_deck, debt_collector_card):
                    player['move_count'] += 1
                    player['private_hand'].remove(debt_collector_card)
                    discard_deck.append(debt_collector_card)
                    return
            charge_rent(player, payers, 5)
            player['private_hand'].remove(debt_collector_card)
            discard_deck.append(debt_collector_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, debt_collector_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


# Sly deal, forced deal, deal breaker
def prompt_pick_property_from_hand(player):
    hand = player['public_hand']
    action_prompt = "Pick a property card from {}'s hand.\n".format(player['name'])
    property_list = []
    set_colors_exclude = []
    for color_index, color_list in player['property_sets'].items():
        if color_list[0] == color_list[2]:
            set_colors_exclude.append(color_index)
    for i, property_card in enumerate(hand):
        if property_card['card_type'] == 'Property':
            if property_card['active_color'] not in set_colors_exclude:
                action_prompt += "Enter '{}': {}\n".format(i, property_card['name'])
                property_list.append(property_card)
    if not property_list:
        return
    else:
        while True:  # Keep prompting until valid input is provided
            user_input = input(action_prompt)
            if user_input.isdigit() and 0 <= int(user_input) < len(action_prompt):
                selected_card = property_list[int(user_input)]
                return selected_card
            else:
                print("Invalid input. Please enter a valid number.")


def prompt_pick_set_from_hand(player):
    hand = player['public_hand']
    action_prompt = "Pick a property set from {}'s hand.\n".format(player['name'])
    set_list = []
    card_list = []
    for color_index, color_list in player['property_sets'].items():
        if color_list[1] > 0:
            set_list.append(color_index)
    if not set_list:
        return
    for i, property_card in enumerate(set_list):
        action_prompt += "Enter '{}': {}\n".format(i, set_list)

    else:
        while True:  # Keep prompting until valid input is provided
            user_input = input(action_prompt)
            if user_input.isdigit() and 0 <= int(user_input) < len(set_list):
                selected_set_color = set_list[int(user_input)]
                remaining_properties_to_take = player['property_sets'][selected_set_color][1]
                while remaining_properties_to_take > 0:
                    for card in hand:
                        if card['card_type'] == 'Property' and card['active_color'] == selected_set_color:
                            card_list.append(card)
                            remaining_properties_to_take -= 1
                for card in hand:
                    if card['card_type'] == 'House' and card['active_color'] == selected_set_color:
                        card_list.append(card)
                        break
                for card in hand:
                    if card['card_type'] == 'Hotel' and card['active_color'] == selected_set_color:
                        card_list.append(card)
                        break
                return card_list
            else:
                print("Invalid input. Please enter a valid number.")


# Amend so you can't steal properties that are part of sets
def sly_deal(player, players, sly_deal_card, discard_deck):
    action_prompt = "Would you like to sly deal or play this card as money?\n" \
                    "1: Sly deal\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            other_players = [x for x in players if x != player]
            selected_player = [prompt_pick_player(player, other_players)][0]
            if prompt_say_no(player, selected_player, discard_deck, sly_deal_card):
                player['move_count'] += 1
                player['private_hand'].remove(sly_deal_card)
                discard_deck.append(sly_deal_card)
                return
            selected_card = prompt_pick_property_from_hand(selected_player)
            selected_player['public_hand'].remove(selected_card)
            player['public_hand'].append(selected_card)
            player['private_hand'].remove(sly_deal_card)
            discard_deck.append(sly_deal_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, sly_deal_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


# Amend so you can't steal properties that are part of sets
def forced_deal(player, players, forced_deal_card, discard_deck):
    action_prompt = "Would you like to force a deal or play this card as money?\n" \
                    "1: Forced deal\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            other_players = [x for x in players if x != player]
            selected_player = [prompt_pick_player(player, other_players)][0]
            if prompt_say_no(player, selected_player, discard_deck, forced_deal_card):
                player['move_count'] += 1
                player['private_hand'].remove(forced_deal_card)
                discard_deck.append(forced_deal_card)
                return
            selected_card_receive = prompt_pick_property_from_hand(selected_player)
            selected_card_give = prompt_pick_property_from_hand(player)

            selected_player['public_hand'].remove(selected_card_receive)
            player['public_hand'].append(selected_card_receive)

            selected_player['public_hand'].append(selected_card_give)
            player['public_hand'].remove(selected_card_give)

            player['private_hand'].remove(forced_deal_card)
            discard_deck.append(forced_deal_card)

            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, forced_deal_card)
            return
        else:
            print("Invalid input. Please enter a valid number.")


def deal_breaker(player, players, deal_breaker_card, discard_deck):
    action_prompt = "Would you like to steal a set or play this as money?\n" \
                    "1: Steal a set\n" \
                    "2: Play this card as money\n"
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input == '1':
            other_players = [x for x in players if x != player]
            other_players_with_sets = []
            for other_player in other_players:
                for color_set in other_player['property_sets'].values():
                    if color_set[1] > 0:
                        other_players_with_sets.append(other_player)
                        break
            selected_player = [prompt_pick_player(player, other_players_with_sets)][0]
            if prompt_say_no(player, selected_player, discard_deck, deal_breaker_card):
                player['private_hand'].remove(deal_breaker_card)
                discard_deck.append(deal_breaker_card)
                player['move_count'] += 1
                return
            card_set = prompt_pick_set_from_hand(selected_player)
            for card in card_set:
                selected_player['public_hand'].remove(card)
                player['public_hand'].append(card)
            player['private_hand'].remove(deal_breaker_card)
            discard_deck.append(deal_breaker_card)
            player['move_count'] += 1
            return
        elif user_input == '2':
            place_money(player, deal_breaker_card)
            return
    else:
        print("Invalid input. Please enter a valid number.")


# Just say no function
def prompt_say_no(action_taker, action_receiver, discard_deck, action_card):
    for card in action_receiver['private_hand']:
        if card['name'] == 'Just Say No':
            action_prompt = "{}, would you like to use your Just Say No card?\n" \
                            "1: Yes\n" \
                            "2: No\n".format(action_receiver['name'])
            while True:  # Keep prompting until valid input is provided
                user_input = input(action_prompt)
                if user_input == '1':
                    print("{} uses a Just Say No card!".format(action_receiver['name']))
                    action_receiver['private_hand'].remove(card)
                    discard_deck.append(card)
                    if prompt_say_no(action_receiver, action_taker, discard_deck, card):
                        return False
                    return True
                else:
                    return False


# Function to switch a publicly played, 2-sided wild card
def switch_wild_card(player):
    wild_cards = []
    for card in player['public_hand']:
        if len(card['colors_available']) == 2:
            wild_cards.append(card)
    action_prompt = "Which wild card would you like to flip?.\n"
    for i, action in enumerate(wild_cards):
        action_prompt += "Enter '{}': {}\n".format(i, action)
    while True:  # Keep prompting until valid input is provided
        user_input = input(action_prompt)
        if user_input.isdigit() and 0 <= int(user_input) < len(wild_cards):
            selected_wild_card = wild_cards[int(user_input)]
            selected_wild_card['active_color'] = next(color for color in selected_wild_card['colors_available'] if
                                                      color != selected_wild_card['active_color'])
            player['move_count'] += 1
            return


# Function for prompting the player for a decision
def player_decision(player):
    actions = ['End Turn', 'Discard Card']
    for card in player['public_hand']:
        if len(card['colors_available']) == 2:
            actions.append('Switch a wild card')
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
            # Property sets structured as color: [properties, sets, set_requirement]
            'property_sets': {
                'Red': [0, 0, 3],
                'Yellow': [0, 0, 3],
                'Light Blue': [0, 0, 3],
                'Black': [0, 0, 4],
                'Brown': [0, 0, 1],
                'Green': [0, 0, 3],
                'Purple': [0, 0, 3],
                'Orange': [0, 0, 3],
                'Dark Blue': [0, 0, 2],
                'Electric': [0, 0, 2],
                'Water': [0, 0, 2]
            }
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
                update_property_count(players)
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

                elif decision == 'Switch a wild card':
                    switch_wild_card(player)

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

                elif decision['name'] == 'Sly Deal':
                    sly_deal(player, players, decision, discard_deck)

                elif decision['name'] == 'Forced Deal':
                    forced_deal(player, players, decision, discard_deck)

                elif decision['name'] == 'Deal Breaker':
                    deal_breaker(player, players, decision, discard_deck)

                else:
                    print("Invalid action:", decision)


if __name__ == "__main__":
    run_game()
