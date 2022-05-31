"""
Blackjack Game

* Player VS automated-dealer
* Player should stand or hit
* Player should pick the betting amount
* Keep track of the player's money
* Alert player of wins, lose, etc.
"""
import random

suits = ("Hearts", "Clubs", "Spades", "Diamonds")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
          'Jack': 10, 'Queen': 10, 'King': 10, "Ace": [1, 11]}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


def Ace():
    while True:
        try:
            choice = int(
                input("Would you like your Ace to count as 1 or 11.\nEnter one of the two numbers.-->"))
            if choice == 1:
                return 0
            elif choice == 11:
                return 1
            else:
                print("You did not enter a correct value!")
                continue
        except ValueError:
            print("I only accept integers!")
            continue


class Player:

    def __init__(self, name):
        self.name = name
        self.all_cards = []
        self.value = 0
        self.n = 0
        self.decision = None

    def __str__(self):
        return f"Player named {self.name}."

    def remove_one(self):
        return self.all_cards.pop(0)

    def add_cards(self, new_cards):
        if isinstance(new_cards, list):
            return self.all_cards.extend(new_cards)
        return self.all_cards.append(new_cards)

    def calc_value(self):
        for card in self.all_cards[self.n::]:
            if card.rank != "Ace":
                self.value += card.value
            else:
                self.value += card.value[Ace()]
            self.n += 1
        return self.value


def plr_cr():
    global dic_plrs
    while True:
        try:
            num_of_players = int(input("How many players will like to play?\n-->"))

            if num_of_players <= 0:
                print("I only accept numbers bigger than zero!")
                continue
            break

        except ValueError:
            print("I only accept integers!")
            continue

    for k in range(1, num_of_players + 1):
        key = "Plr_" + f"{k}"
        dic_plrs[key] = Player(input(f"Enter the name of the {k}st/nd/th player:\n-->"))


# def reset():
    # for player in dic_plrs:
        # dic_plrs[player].all_cards = []
        # dic_plrs[player].value = 0
        # dic_plrs[player].n = 0
        # dic_plrs[player].decision = None


class BankAccount:

    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: amount should be positive.")
            return
        if amount > self.balance:
            amount = self.balance
        self.balance -= amount
        return amount

    def deposit(self, amount):
        if amount <= 0:
            print("Error: amount should be positive.")
            return
        self.balance += amount

    def betting(self):
        while True:
            try:
                bet_amount = int(input("How much would you like to bet?\n-->"))
                if bet_amount <= 0:
                    raise ValueError("Please enter a number greater than zero!")
                elif bet_amount > self.balance:
                    print(f"Your current balance is not enough({self.balance})!")
                    continue
                else:
                    return bet_amount
            except ValueError:
                print("I only accept integers!")
                continue


def replay():
    while True:
        choice = input("Do you want to play again?(Y/N)\n-->").upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("I only accept the letter 'Y' and 'N'!")
            continue


# Create a dealer
dlr = Player("Dealer")

while True:
    # Create players
    dic_plrs = {}
    plr_cr()
    # Dealer Initialization Stuff
    dlr.all_cards = []
    dlr.n = 0
    dlr.value = 0
    # Players' Initialization Stuff
    # reset()
    while True:
        # Create and shuffle a deck
        deck = Deck()
        deck.shuffle()

        # Deal two cards to the dealer
        dlr.add_cards(deck.deal_one())
        dlr.add_cards(deck.deal_one())
        # Display one of the dealer's cards
        print("This is one of the dealer's cards: ", dlr.all_cards[0], "(", dlr.all_cards[1], ")")

        # Deal cards to the players and display them
        for player in dic_plrs:
            dic_plrs[player].add_cards(deck.deal_one())
            dic_plrs[player].add_cards(deck.deal_one())
            print(
                f"Your cards {dic_plrs[player].name} are: {dic_plrs[player].all_cards[0]},"
                f" {dic_plrs[player].all_cards[1]}")
            print(f"({dic_plrs[player].calc_value()})")

        # player's turn
        for player in dic_plrs:
            while dic_plrs[player].calc_value() < 21 and dic_plrs[player].decision != "S":
                while True:
                    dic_plrs[player].decision = input(f"{dic_plrs[player].name} would you like to hit or stand?\n-->")[
                        0].upper()
                    if dic_plrs[player].decision == "H":
                        dic_plrs[player].add_cards(deck.deal_one())
                        print(f"{dic_plrs[player].name} you got {dic_plrs[player].all_cards[-1]}.({dic_plrs[player].calc_value()})")
                        break
                    elif dic_plrs[player].decision == "S":
                        break
                    else:
                        print("I only accept one of the two words: 'Hit'/ 'Stand'")
                        continue
                continue

        for player in list(dic_plrs):
            if dic_plrs[player].value > 21:
                print(f"{dic_plrs[player].name} you lost!({dic_plrs[player].value})")
                del dic_plrs[player]

        # Dealer's Turn
        while dlr.calc_value() < 17:
            dlr.add_cards(deck.deal_one())
            # Helps with keeping track of the dealer's cards: print(dlr.all_cards[-1])

        if dlr.value > 21:
            for player in dic_plrs:
                print(f"{dic_plrs[player].name} you Won({dic_plrs[player].value}) and the Dealer({dlr.value}) lost!")
            break

        for player in dic_plrs:
            if dic_plrs[player].value > dlr.value:
                print(
                    f"{dic_plrs[player].name} you Won({dic_plrs[player].value}) and the Dealer({dlr.value}) lost!")
            else:
                print(
                    f"{dic_plrs[player].name} you Lost({dic_plrs[player].value}) and the Dealer({dlr.value}) Won!")
        break
    if not replay():
        break
