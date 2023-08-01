import random
import statistics
import argparse

def create_deck(num_decks=6):
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * num_decks
    random.shuffle(deck)
    return deck

def get_card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def initial_deal(deck):
    return [deck.pop(), deck.pop()]

def is_blackjack(hand):
    return len(hand) == 2 and get_hand_value(hand) == 21

def get_hand_value(hand):
    value = sum(get_card_value(card) for card in hand)
    num_aces = hand.count('A')

    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1

    return value

def play_player_hand(deck, player_hand, dealer_upcard, starting_capital, bet):
    action = basic_strategy_decision(player_hand, dealer_upcard)
    print(player_hand, "against", dealer_upcard, ":", action)

    if action == "Hit":
        player_hand.append(deck.pop())
        player_value = get_hand_value(player_hand)

        if player_value > 21:
            print(player_hand, dealer_upcard)
            print("Player Bust", player_value)
            return -bet
        else:
            return play_player_hand(deck, player_hand, dealer_upcard, starting_capital, bet)

    elif action == "Double Down":
        player_hand.append(deck.pop())
        player_value = get_hand_value(player_hand)

        if player_value > 21:
            return -2 * bet
        else:
            return 2 * play_dealer_hand(deck, player_hand, dealer_upcard, starting_capital, bet)

    elif action == "Stay":
        return play_dealer_hand(deck, player_hand, dealer_upcard, starting_capital, bet)

    elif action == "Split":
        hand1 = [player_hand[0], deck.pop()]
        hand2 = [player_hand[1], deck.pop()]
        return play_player_hand(deck, hand1, dealer_upcard, starting_capital, bet) + play_player_hand(deck, hand2, dealer_upcard, starting_capital, bet)

    elif action == "Surrender":
        return -0.5 * bet 
    

    return None

def play_dealer_hand(deck, player_hand, dealer_upcard, starting_capital, bet):
    dealer_hand = [dealer_upcard, deck.pop()]

    while get_hand_value(dealer_hand) < 17 or (get_hand_value(dealer_hand) == 17 and 'A' in dealer_hand):
        dealer_hand.append(deck.pop())

    dealer_value = get_hand_value(dealer_hand)
    player_value = get_hand_value(player_hand)
    if dealer_value > 21 or dealer_value < player_value:
        print(player_hand, dealer_hand)
        print("Win:", player_value, dealer_value)
        return bet
    elif dealer_value > player_value:
        print(player_hand, dealer_hand)
        print("Lose:", player_value, dealer_value)
        return -bet
    else:
        print(player_hand, dealer_hand)
        print("Tie:", player_value, dealer_value)
        return 0

def basic_strategy_decision(player_hand, dealer_upcard):
    player_value = get_hand_value(player_hand)
    dealer_upcard_value = get_card_value(dealer_upcard)

    # For splits
    if player_hand[0] == player_hand[1]:
        if len(player_hand) == 2:
            if player_hand[0] in ["2", "3"]:
                if "2" <= dealer_upcard[0] <= "7":
                    return "Split"
                else:
                    return "Hit"

            if player_hand[0] == "4":
                if "5" <= dealer_upcard[0] <= "6":
                    return "Split"
                else:
                    return "Hit"

            if player_hand[0] == "6":
                if "2" <= dealer_upcard[0] <= "6":
                    return "Split"
                else:
                    return "Hit"

            if player_hand[0] == "7":
                if "2" <= dealer_upcard[0] <= "7":
                    return "Split"
                else:
                    return "Hit"

            if player_hand[0] in ["8", "A"]:
                return "Split"

            if player_hand[0] == "9":
                if dealer_upcard[0] in ["7", "10", "J", "Q", "K", "A"]:
                    return "Stay"
                else:
                    return "Split"

    # For soft hands
    if "A" in player_hand:
        if 13 <= player_value <= 14:
            if dealer_upcard_value in [5, 6]:
                if len(player_hand) == 2:
                    return "Double Down"
                else:
                    return "Hit"
            else:
                return "Hit"

        if 15 <= player_value <= 16:
            if dealer_upcard_value in [4, 5, 6]:
                if len(player_hand) == 2:
                    return "Double Down"
                else:
                    return "Hit"
            else:
                return "Hit"

        if player_value == 17:
            if dealer_upcard_value in [3, 4, 5, 6]:
                if len(player_hand) == 2:
                    return "Double Down"
                else:
                    return "Hit"
            else:
                return "Hit"

        if player_value == 18:
            if dealer_upcard_value in [2, 3, 4, 5, 6]:
                if len(player_hand) == 2:
                    return "Double Down"
                else:
                    return "Hit"
            elif dealer_upcard_value in [7, 8]:
                return "Stay"
            else:
                return "Hit"

        if player_value == 19:
            if dealer_upcard_value == 6:
                if len(player_hand) == 2:
                    return "Double Down"
                else:
                    return "Hit"
            else:
                return "Stay"

        if player_value >= 20:
            return "Stay"


    # For hard hands
    if player_value <= 8:
        return "Hit"

    if player_value == 9:
        if len(player_hand) == 2:
            if 3 <= dealer_upcard_value <= 6:
                return "Double Down"
            else:
                return "Hit"
        else:
            return "Hit"

    if player_value == 10:
        if len(player_hand) == 2:
            if 2 <= dealer_upcard_value <= 9:
                return "Double Down"
            else:
                return "Hit"
        else:
            return "Hit"

    if player_value == 11:
        return "Double Down"

    if player_value == 12:
        if 4 <= dealer_upcard_value <= 6:
            return "Stay"
        else:
            return "Hit"

    if 13 <= player_value <= 14:
        if dealer_upcard_value <= 6:
            return "Stay"
        else:
            return "Hit"

    
    if player_value == 15:
        if dealer_upcard_value == 10:
            if len(player_hand) == 2:
                return "Surrender"
            else:
                return "Hit"
        elif 2 <= dealer_upcard_value <= 6:
            return "Stay"
        else:
            return "Hit"

    if player_value == 16:
        if dealer_upcard_value in [9, 10]:
            if len(player_hand) == 2:
                return "Surrender"
            else:
                return "Hit"
        elif 2 <= dealer_upcard_value <= 6:
            return "Stay"
        else:
            return "Hit"

    if player_value >= 17:
        return "Stay"

    return "Stay"


def simulate_blackjack(num_games, starting_capital, bet):
    deck = create_deck() #Continous Shuffler
    profits = []

    for _ in range(num_games):
        print("\nGame", _ + 1)
        deck = create_deck()

        player_hand = initial_deal(deck)
        dealer_upcard = deck.pop()

        if is_blackjack(player_hand) and dealer_upcard != "A":
            print(player_hand, dealer_upcard, "Player Blackjack")
            profit = 1.5 * bet  # Blackjack pays 3 to 2
        else:
            profit = play_player_hand(deck, player_hand, dealer_upcard, starting_capital, bet)

        profits.append(profit)

    total_profit = sum(profits)
    mean_profit = total_profit / num_games
    variance = statistics.variance(profits)
    standard_deviation = statistics.stdev(profits)

    return total_profit, mean_profit, variance, standard_deviation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blackjack Simulator")
    parser.add_argument("--num-games", type=int, default=10000, help="Number of games to simulate (default: 10000)")
    parser.add_argument("--starting-capital", type=int, default=1000, help="Starting capital (default: 1000)")
    parser.add_argument("--bet-amount", type=int, default=25, help="Bet amount (default: 25)")
    args = parser.parse_args()

    num_games = args.num_games
    starting_capital = args.starting_capital
    bet = args.bet_amount

    total_profit, mean_profit, variance, standard_deviation = simulate_blackjack(num_games, starting_capital, bet)

    print(f"\n----------------------------------------")
    print(f"Total: ${total_profit + starting_capital}")
    print(f"Total Profit: ${total_profit}")
    print(f"Mean Profit: ${mean_profit}")
    print(f"Variance: {variance}")
    print(f"Standard Deviation: {standard_deviation}")

